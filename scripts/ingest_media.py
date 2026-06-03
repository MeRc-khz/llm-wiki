#!/usr/bin/env python3
import argparse
import os
import subprocess
import json
import hashlib
from datetime import datetime

WIKI_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_TRANSCRIPTS_DIR = os.path.join(WIKI_DIR, "raw", "transcripts")
RAW_AUDIO_DIR = os.path.join(WIKI_DIR, "raw", "audio")
RAW_VIDEO_DIR = os.path.join(WIKI_DIR, "raw", "video")
FETCH_TRANSCRIPT_SCRIPT = os.path.join(WIKI_DIR, "scripts", "fetch_transcript.py")

def get_file_sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def extract_audio(video_path, output_audio_path):
    print(f"🎬 Video detected. Extracting audio using ffmpeg...")
    cmd = [
        "ffmpeg", "-y", "-i", video_path,
        "-vn", "-acodec", "libmp3lame", "-ar", "16000", "-ac", "1",
        output_audio_path
    ]
    result = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if result.returncode == 0:
        print(f"✅ Audio extracted successfully: {output_audio_path}")
        return True
    else:
        print("❌ Failed to extract audio using ffmpeg.")
        return False

def ingest_youtube(url, title=None):
    print(f"🌐 Processing YouTube media: {url}")
    
    # Run fetch_transcript.py
    cmd = ["python3", FETCH_TRANSCRIPT_SCRIPT, url, "--timestamps"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print("❌ Failed to fetch transcript from YouTube.")
        try:
            err = json.loads(result.stdout)
            print(f"Reason: {err.get('error')}")
        except:
            print(result.stderr)
        return False
        
    try:
        data = json.loads(result.stdout)
    except Exception as e:
        print(f"❌ Failed to parse transcript output: {e}")
        return False
        
    video_id = data.get("video_id")
    full_text = data.get("full_text")
    timestamped_text = data.get("timestamped_text", "")
    duration = data.get("duration", "0:00")
    
    resolved_title = title or f"YouTube Video {video_id}"
    
    # Compute SHA256 of the transcript body
    sha256 = hashlib.sha256(timestamped_text.encode('utf-8')).hexdigest()
    
    filename = f"youtube-{video_id}.md"
    output_path = os.path.join(RAW_TRANSCRIPTS_DIR, filename)
    
    content = f"""---
title: "{resolved_title}"
source_url: "{url}"
video_id: "{video_id}"
duration: "{duration}"
ingested: {datetime.now().strftime('%Y-%m-%d')}
sha256: {sha256}
media_type: video
---

# {resolved_title}

## Metadata
- **URL:** {url}
- **Video ID:** {video_id}
- **Duration:** {duration}
- **Ingestion Date:** {datetime.now().strftime('%Y-%m-%d')}

## Transcript
{timestamped_text}
"""
    
    with open(output_path, 'w') as f:
        f.write(content)
        
    print(f"🎉 Ingested YouTube transcript: raw/transcripts/{filename}")
    return filename

def ingest_local_file(file_path, title=None, transcription_api_key=None):
    print(f"📁 Processing local media file: {file_path}")
    if not os.path.exists(file_path):
        print("❌ File does not exist.")
        return False
        
    filename = os.path.basename(file_path)
    base_name, ext = os.path.splitext(filename)
    ext = ext.lower()
    
    is_video = ext in ['.mp4', '.mkv', '.avi', '.mov', '.webm']
    is_audio = ext in ['.mp3', '.wav', '.ogg', '.m4a', '.flac']
    
    if not is_video and not is_audio:
        print("❌ Unsupported media format.")
        return False
        
    # Copy file to appropriate raw folder
    dest_dir = RAW_VIDEO_DIR if is_video else RAW_AUDIO_DIR
    dest_path = os.path.join(dest_dir, filename)
    
    # If it's already in the raw directory, skip copying
    if os.path.abspath(file_path) != os.path.abspath(dest_path):
        print(f"💾 Copying source to {dest_dir}...")
        import shutil
        shutil.copy2(file_path, dest_path)
        
    sha256 = get_file_sha256(dest_path)
    resolved_title = title or base_name.replace("-", " ").replace("_", " ").title()
    
    # If it's a video, extract a lightweight audio track for transcription
    extracted_audio_path = None
    if is_video:
        audio_filename = f"{base_name}-extracted.mp3"
        extracted_audio_path = os.path.join(RAW_AUDIO_DIR, audio_filename)
        extract_audio(dest_path, extracted_audio_path)
        
    # Transcript placeholder
    transcript_filename = f"{base_name}.md"
    transcript_path = os.path.join(RAW_TRANSCRIPTS_DIR, transcript_filename)
    
    # Optional Transcription API execution (e.g. OpenAI/Groq Whisper)
    transcript_content = "[Pending Transcription]"
    if transcription_api_key:
        print("🎙️ API Key found. Attempting Whisper transcription...")
        # Placeholder for API transcription execution
        # (e.g. calling openai.audio.transcriptions.create or a curl script)
        transcript_content = "[Transcribing automatically via API is not yet wired up - placeholder content]"
    
    content = f"""---
title: "{resolved_title}"
source_file: "raw/{'video' if is_video else 'audio'}/{filename}"
ingested: {datetime.now().strftime('%Y-%m-%d')}
sha256: {sha256}
media_type: {'video' if is_video else 'audio'}
has_extracted_audio: {str(is_video).lower()}
---

# {resolved_title}

## Metadata
- **Source File:** raw/{'video' if is_video else 'audio'}/{filename}
- **SHA256:** {sha256}
- **Ingestion Date:** {datetime.now().strftime('%Y-%m-%d')}
{f'- **Extracted Audio Track:** raw/audio/{base_name}-extracted.mp3' if is_video else ''}

## Transcript
{transcript_content}
"""

    with open(transcript_path, 'w') as f:
        f.write(content)
        
    print(f"🎉 Ingested local media resource: raw/transcripts/{transcript_filename}")
    return transcript_filename

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest audio, video, podcast, and music files/links into LLM Wiki")
    parser.add_argument("source", help="YouTube URL or local file path")
    parser.add_argument("--title", "-t", default=None, help="Descriptive title of the media")
    parser.add_argument("--api-key", "-k", default=None, help="OpenAI/Groq API key for automated transcription")
    args = parser.parse_args()
    
    if "youtube.com" in args.source or "youtu.be" in args.source:
        ingest_youtube(args.source, args.title)
    else:
        ingest_local_file(args.source, args.title, args.api_key)
