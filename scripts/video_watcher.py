#!/usr/bin/env python3
"""
Video ingestion watcher for the LLM Wiki.

Watches /srv/projects/Media for new video files. When a video appears:
1. Copies it to wiki raw/video/ (immutable storage)
2. Extracts a lightweight audio track via ffmpeg → raw/audio/
3. Sends the video to an OpenRouter multimodal model for full video understanding
   (speech transcription + visual descriptions + on-screen text)
4. Saves the rich transcript to raw/transcripts/
5. Appends to log.md

Usage:
  python3 video_watcher.py                    # Watch mode (foreground)
  python3 video_watcher.py --process /path    # Process a single file and exit
  python3 video_watcher.py --once             # Process all unprocessed files and exit

Config via environment or /root/.hermes/.env:
  OPENROUTER_API_KEY  - Required for video understanding API calls
  WIKI_PATH           - Wiki root (default: /srv/projects/llm-wiki)
  MEDIA_DROP_DIR      - Drop folder to watch (default: /srv/projects/Media)
  VIDEO_MODEL         - OpenRouter model to use (default: google/gemini-2.5-flash)
"""

import os
import sys
import time
import json
import base64
import hashlib
import argparse
import subprocess
import shutil
from datetime import datetime
from pathlib import Path

# --- Config ---

def load_env():
    """Load env vars from /root/.hermes/.env if not already set."""
    env_path = os.path.expanduser("~/.hermes/.env")
    if not os.path.exists(env_path):
        # Try alternate path
        env_path = "/root/.hermes/.env"
    if not os.path.exists(env_path):
        return
    with open(env_path, "r") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, val = line.split("=", 1)
                key = key.strip()
                val = val.strip().strip('"').strip("'")
                if key and key not in os.environ:
                    os.environ[key] = val

load_env()

WIKI_PATH = os.environ.get("WIKI_PATH", "/srv/projects/llm-wiki")
MEDIA_DROP_DIR = os.environ.get("MEDIA_DROP_DIR", "/srv/projects/Media")
VIDEO_MODEL = os.environ.get("VIDEO_MODEL", "google/gemini-2.5-flash")
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")

RAW_VIDEO_DIR = os.path.join(WIKI_PATH, "raw", "video")
RAW_AUDIO_DIR = os.path.join(WIKI_PATH, "raw", "audio")
RAW_TRANSCRIPTS_DIR = os.path.join(WIKI_PATH, "raw", "transcripts")
LOG_PATH = os.path.join(WIKI_PATH, "log.md")
PROCESSED_MARKER = os.path.join(MEDIA_DROP_DIR, ".processed")

VIDEO_EXTENSIONS = {".mp4", ".mkv", ".mov", ".webm", ".avi", ".m4v"}
MAX_VIDEO_SIZE_MB = 500  # OpenRouter base64 payload limit ~ this
CHUNK_OVERLAP_SECONDS = 0  # For very long videos, could split into chunks


def get_file_sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()


def get_video_duration(path):
    try:
        result = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", path],
            capture_output=True, text=True, check=True
        )
        sec = float(result.stdout.strip())
        m, s = divmod(int(sec), 60)
        h, m = divmod(m, 60)
        return f"{h:02d}:{m:02d}:{s:02d}"
    except Exception:
        return "00:00:00"


def extract_audio(video_path, output_path):
    """Extract mono 16kHz MP3 audio from video."""
    cmd = [
        "ffmpeg", "-y", "-i", video_path,
        "-vn", "-acodec", "libmp3lame", "-ar", "16000", "-ac", "1",
        output_path
    ]
    result = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return result.returncode == 0


def send_video_to_openrouter(video_path, title):
    """
    Send video to OpenRouter multimodal model for full video understanding.
    Returns the transcript text with visual descriptions.
    """
    import urllib.request

    file_size_mb = os.path.getsize(video_path) / (1024 * 1024)
    if file_size_mb > MAX_VIDEO_SIZE_MB:
        print(f"  ⚠️  Video is {file_size_mb:.1f}MB — may exceed API limits. Trying anyway...")

    print(f"  📦 Encoding video to base64 ({file_size_mb:.1f}MB)...")
    with open(video_path, "rb") as f:
        video_b64 = base64.b64encode(f.read()).decode()

    # Determine MIME type
    ext = Path(video_path).suffix.lower()
    mime_map = {
        ".mp4": "video/mp4",
        ".mkv": "video/x-matroska",
        ".mov": "video/quicktime",
        ".webm": "video/webm",
        ".avi": "video/x-msvideo",
        ".m4v": "video/x-m4v",
    }
    mime_type = mime_map.get(ext, "video/mp4")

    prompt = (
        f"You are analyzing a video titled \"{title}\" for a knowledge base wiki.\n\n"
        "Please provide a comprehensive analysis:\n\n"
        "## Transcript\n"
        "Transcribe all spoken content verbatim with timestamps (e.g. [00:15]) and speaker labels "
        "(Speaker 1, Speaker 2, etc.) where possible.\n\n"
        "## Visual Description\n"
        "Describe key visual elements: scenes, on-screen text, charts, diagrams, body language, "
        "UI elements, and significant visual changes. Include approximate timestamps.\n\n"
        "## Summary\n"
        "A 2-3 paragraph summary of the video's main content and purpose.\n\n"
        "## Key Entities\n"
        "List any people, organizations, products, or concepts mentioned (with brief context).\n\n"
        "Format everything in clean markdown."
    )

    payload = {
        "model": VIDEO_MODEL,
        "messages": [{
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:{mime_type};base64,{video_b64}"}
                }
            ]
        }]
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=data,
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        }
    )

    print(f"  🚀 Sending to {VIDEO_MODEL} via OpenRouter...")
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            result = json.loads(resp.read().decode())
            content = result["choices"][0]["message"]["content"]
            model_used = result.get("model", VIDEO_MODEL)
            print(f"  ✅ Got response from {model_used}")
            return content, model_used
    except Exception as e:
        print(f"  ❌ OpenRouter API error: {e}")
        # If video upload fails, try fallback: audio-only transcription
        return None, None


def fallback_audio_transcription(audio_path, title):
    """Fallback: use Gemini direct API for audio-only transcription."""
    import urllib.request

    google_key = os.environ.get("GOOGLE_API_KEY", "")
    if not google_key:
        return "[Transcription failed: no API keys available]"

    print(f"  🎙️ Falling back to audio-only Gemini transcription...")

    with open(audio_path, "rb") as f:
        audio_b64 = base64.b64encode(f.read()).decode()

    prompt = (
        f"You are an expert audio transcriptionist. Transcribe this audio from \"{title}\" verbatim. "
        "Include timestamps (e.g. [00:15]) for every few sentences. "
        "Capture speaker turns if possible (Speaker 1, Speaker 2).\n\n"
        "Also provide a brief summary at the end."
    )

    payload = {
        "model": "gemini-2.5-flash",
        "messages": [{
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:audio/mp3;base64,{audio_b64}"}
                }
            ]
        }]
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions",
        data=data,
        headers={
            "Authorization": f"Bearer {google_key}",
            "Content-Type": "application/json",
        }
    )

    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            result = json.loads(resp.read().decode())
            return result["choices"][0]["message"]["content"]
    except Exception as e:
        return f"[Transcription failed: {e}]"


def process_video(filepath):
    """Process a single video file through the full pipeline."""
    filepath = os.path.abspath(filepath)
    filename = os.path.basename(filepath)
    base_name, ext = os.path.splitext(filename)
    ext = ext.lower()

    if ext not in VIDEO_EXTENSIONS:
        print(f"  ⏭️  Skipping {filename} (not a video)")
        return False

    print(f"\n{'='*60}")
    print(f"🎬 Processing: {filename}")
    print(f"{'='*60}")

    # 1. Copy to wiki raw/video/
    dest_video = os.path.join(RAW_VIDEO_DIR, filename)
    if os.path.abspath(filepath) != os.path.abspath(dest_video):
        print(f"  💾 Copying to {dest_video}...")
        os.makedirs(RAW_VIDEO_DIR, exist_ok=True)
        shutil.copy2(filepath, dest_video)
    else:
        os.makedirs(RAW_VIDEO_DIR, exist_ok=True)

    sha256 = get_file_sha256(dest_video)
    duration = get_video_duration(dest_video)
    title = base_name.replace("-", " ").replace("_", " ").replace(".", " ").strip()
    print(f"  📊 Duration: {duration} | SHA256: {sha256[:16]}...")

    # 2. Extract audio
    audio_filename = f"{base_name}-extracted.mp3"
    audio_path = os.path.join(RAW_AUDIO_DIR, audio_filename)
    os.makedirs(RAW_AUDIO_DIR, exist_ok=True)
    print(f"  🎵 Extracting audio...")
    if not extract_audio(dest_video, audio_path):
        print(f"  ⚠️  Audio extraction failed, continuing without audio fallback")
        audio_path = None

    # 3. Send to OpenRouter for video understanding
    transcript_content = None
    model_used = None
    if OPENROUTER_API_KEY:
        transcript_content, model_used = send_video_to_openrouter(dest_video, title)

    # 4. Fallback to audio-only if video upload failed
    if not transcript_content and audio_path:
        transcript_content = fallback_audio_transcription(audio_path, title)
        model_used = "gemini-2.5-flash (audio-only fallback)"

    if not transcript_content:
        transcript_content = "[Transcription failed: no API keys or all methods failed]"
        model_used = "none"

    # 5. Save transcript
    os.makedirs(RAW_TRANSCRIPTS_DIR, exist_ok=True)
    transcript_filename = f"{base_name}.md"
    transcript_path = os.path.join(RAW_TRANSCRIPTS_DIR, transcript_filename)
    transcript_sha = hashlib.sha256(transcript_content.encode("utf-8")).hexdigest()

    transcript_md = f"""---
title: "{title}"
source_file: "raw/video/{filename}"
ingested: {datetime.now().strftime('%Y-%m-%d')}
sha256: {transcript_sha}
media_type: video
duration: "{duration}"
model: "{model_used}"
has_extracted_audio: {"true" if audio_path else "false"}
---

# {title}

## Metadata
- **Source File:** raw/video/{filename}
- **SHA256 (source):** {sha256}
- **Ingestion Date:** {datetime.now().strftime('%Y-%m-%d')}
- **Duration:** {duration}
- **Model:** {model_used}
{f'- **Extracted Audio:** raw/audio/{audio_filename}' if audio_path else ''}

## Analysis

{transcript_content}
"""

    with open(transcript_path, "w") as f:
        f.write(transcript_md)

    print(f"  🎉 Transcript saved: raw/transcripts/{transcript_filename}")

    # 6. Log to wiki log.md
    log_entry = f"\n## [{datetime.now().strftime('%Y-%m-%d')}] ingest | {title}\n"
    log_entry += f"- Source: raw/video/{filename}\n"
    log_entry += f"- Transcript: raw/transcripts/{transcript_filename}\n"
    log_entry += f"- Duration: {duration}\n"
    log_entry += f"- Model: {model_used}\n"
    if audio_path:
        log_entry += f"- Extracted audio: raw/audio/{audio_filename}\n"

    with open(LOG_PATH, "a") as f:
        f.write(log_entry)

    print(f"  📝 Logged to log.md")

    # 7. Mark as processed
    os.makedirs(PROCESSED_MARKER, exist_ok=True)
    marker = os.path.join(PROCESSED_MARKER, f"{filename}.done")
    with open(marker, "w") as f:
        f.write(datetime.now().isoformat())

    # 8. Move original to processed subfolder (optional, keeps drop dir clean)
    processed_dir = os.path.join(MEDIA_DROP_DIR, "processed")
    os.makedirs(processed_dir, exist_ok=True)
    if os.path.abspath(filepath) != os.path.abspath(dest_video):
        shutil.move(filepath, os.path.join(processed_dir, filename))
        print(f"  📁 Moved original to processed/")

    print(f"  ✅ Done: {filename}")
    return True


def get_unprocessed_videos():
    """Find video files in drop dir that haven't been processed yet."""
    processed_dir = os.path.join(MEDIA_DROP_DIR, "processed")
    videos = []
    if not os.path.exists(MEDIA_DROP_DIR):
        return videos
    for f in os.listdir(MEDIA_DROP_DIR):
        filepath = os.path.join(MEDIA_DROP_DIR, f)
        if not os.path.isfile(filepath):
            continue
        ext = os.path.splitext(f)[1].lower()
        if ext not in VIDEO_EXTENSIONS:
            continue
        # Check if already processed
        marker = os.path.join(PROCESSED_MARKER, f"{f}.done")
        if os.path.exists(marker):
            continue
        videos.append(filepath)
    return videos


def watch_loop(poll_interval=5):
    """Watch the drop directory for new video files."""
    os.makedirs(MEDIA_DROP_DIR, exist_ok=True)
    print(f"👁️  Watching {MEDIA_DROP_DIR} for video files...")
    print(f"   Wiki: {WIKI_PATH}")
    print(f"   Model: {VIDEO_MODEL}")
    print(f"   Poll interval: {poll_interval}s")
    print(f"   Press Ctrl+C to stop.\n")

    while True:
        try:
            videos = get_unprocessed_videos()
            for v in videos:
                # Wait a moment to ensure file is fully written
                size1 = os.path.getsize(v)
                time.sleep(2)
                size2 = os.path.getsize(v)
                if size1 != size2:
                    continue  # File still being written, skip for now
                process_video(v)
        except KeyboardInterrupt:
            print("\n👋 Stopping watcher.")
            break
        except Exception as e:
            print(f"⚠️  Error in watch loop: {e}")
        time.sleep(poll_interval)


def main():
    parser = argparse.ArgumentParser(
        description="Video ingestion watcher for the LLM Wiki"
    )
    parser.add_argument(
        "--process", metavar="PATH",
        help="Process a single video file and exit"
    )
    parser.add_argument(
        "--once", action="store_true",
        help="Process all unprocessed videos in drop dir and exit"
    )
    parser.add_argument(
        "--watch", action="store_true",
        help="Watch the drop directory continuously (default)"
    )
    parser.add_argument(
        "--model", default=None,
        help=f"OpenRouter model to use (default: {VIDEO_MODEL})"
    )
    args = parser.parse_args()

    if args.model:
        os.environ["VIDEO_MODEL"] = args.model

    # Ensure dirs exist
    os.makedirs(RAW_VIDEO_DIR, exist_ok=True)
    os.makedirs(RAW_AUDIO_DIR, exist_ok=True)
    os.makedirs(RAW_TRANSCRIPTS_DIR, exist_ok=True)
    os.makedirs(PROCESSED_MARKER, exist_ok=True)

    if args.process:
        if not os.path.exists(args.process):
            print(f"❌ File not found: {args.process}")
            sys.exit(1)
        process_video(args.process)
    elif args.once:
        videos = get_unprocessed_videos()
        if not videos:
            print("No unprocessed videos found.")
        for v in videos:
            process_video(v)
    else:
        # Default: watch mode
        watch_loop()


if __name__ == "__main__":
    main()
