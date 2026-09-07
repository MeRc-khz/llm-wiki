#!/usr/bin/env python3
"""
Audio transcription watcher using MuScriptor.

Watches /srv/projects/Media for new audio files. When audio appears:
1. Runs MuScriptor transcribe (audio-to-MIDI) via uvx
2. Saves MIDI output to processed/ alongside the original
3. Appends to wiki log.md
4. Marks as processed with .processed/<filename>.done

Usage:
  python3 audio_watcher.py                    # Watch mode (foreground)
  python3 audio_watcher.py --process /path     # Process a single file and exit
  python3 audio_watcher.py --once              # Process all unprocessed files and exit

Config via environment or /root/.hermes/.env:
  WIKI_PATH           - Wiki root (default: /srv/projects/llm-wiki)
  MEDIA_DROP_DIR      - Drop folder to watch (default: /srv/projects/Media)
"""

import os
import sys
import time
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
LOG_PATH = os.path.join(WIKI_PATH, "log.md")
PROCESSED_MARKER = os.path.join(MEDIA_DROP_DIR, ".processed")
PROCESSED_OUTPUT_DIR = os.path.join(MEDIA_DROP_DIR, "processed")

AUDIO_EXTENSIONS = {".wav", ".mp3", ".flac", ".ogg", ".m4a", ".aac", ".aiff", ".aif"}


def get_file_sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()


def get_audio_duration(path):
    """Get duration as HH:MM:SS via ffprobe."""
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


def run_muscriptor(filepath, output_path):
    """Run MuScriptor transcribe on an audio file, producing a MIDI file."""
    cmd = [
        "uvx", "muscriptor", "transcribe",
        filepath,
        "--output", output_path,
        "--format", "midi",
        "--detect-tempo", "best-effort",
    ]
    env = os.environ.copy()
    env["TMPDIR"] = os.environ.get("TMPDIR", "/root/.tmp")
    result = subprocess.run(cmd, capture_output=True, text=True, env=env, timeout=600)
    if result.returncode != 0:
        print(f"  MuScriptor stderr: {result.stderr[:500]}")
        return False
    return os.path.exists(output_path)


def process_audio(filepath):
    """Process a single audio file through the MuScriptor pipeline."""
    filepath = os.path.abspath(filepath)
    filename = os.path.basename(filepath)
    base_name, ext = os.path.splitext(filename)
    ext = ext.lower()

    if ext not in AUDIO_EXTENSIONS:
        print(f"  Skipping {filename} (not audio)")
        return False

    print(f"\n{'='*60}")
    print(f"🎵 Processing: {filename}")
    print(f"{'='*60}")

    sha256 = get_file_sha256(filepath)
    duration = get_audio_duration(filepath)
    title = base_name.replace("-", " ").replace("_", " ").replace(".", " ").strip()
    print(f"  Duration: {duration} | SHA256: {sha256[:16]}...")

    # Run MuScriptor
    os.makedirs(PROCESSED_OUTPUT_DIR, exist_ok=True)
    midi_filename = f"{base_name}.mid"
    midi_path = os.path.join(PROCESSED_OUTPUT_DIR, midi_filename)

    print(f"  Running MuScriptor transcribe...")
    if not run_muscriptor(filepath, midi_path):
        print(f"  MuScriptor failed on {filename}")
        # Mark as attempted so we don't retry endlessly
        os.makedirs(PROCESSED_MARKER, exist_ok=True)
        marker = os.path.join(PROCESSED_MARKER, f"{filename}.done")
        with open(marker, "w") as f:
            f.write(f"{datetime.now().isoformat()}\nFAILED\n")
        return False

    midi_size = os.path.getsize(midi_path) if os.path.exists(midi_path) else 0
    print(f"  MIDI output: {midi_filename} ({midi_size} bytes)")

    # Log to wiki log.md
    log_entry = f"\n## [{datetime.now().strftime('%Y-%m-%d')}] muscriptor | {title}\n"
    log_entry += f"- Source: {filename}\n"
    log_entry += f"- MIDI: processed/{midi_filename}\n"
    log_entry += f"- Duration: {duration}\n"
    log_entry += f"- SHA256: {sha256}\n"
    log_entry += f"- Type: audio-to-MIDI\n"

    with open(LOG_PATH, "a") as f:
        f.write(log_entry)

    print(f"  Logged to log.md")

    # Mark as processed
    os.makedirs(PROCESSED_MARKER, exist_ok=True)
    marker = os.path.join(PROCESSED_MARKER, f"{filename}.done")
    with open(marker, "w") as f:
        f.write(datetime.now().isoformat())

    print(f"  Done: {filename}")
    return True


def get_unprocessed_audio():
    """Find audio files in drop dir that haven't been processed yet."""
    audio_files = []
    if not os.path.exists(MEDIA_DROP_DIR):
        return audio_files
    for f in os.listdir(MEDIA_DROP_DIR):
        filepath = os.path.join(MEDIA_DROP_DIR, f)
        if not os.path.isfile(filepath):
            continue
        ext = os.path.splitext(f)[1].lower()
        if ext not in AUDIO_EXTENSIONS:
            continue
        marker = os.path.join(PROCESSED_MARKER, f"{f}.done")
        if os.path.exists(marker):
            continue
        audio_files.append(filepath)
    return audio_files


def watch_loop(poll_interval=10):
    """Watch the drop directory for new audio files."""
    os.makedirs(MEDIA_DROP_DIR, exist_ok=True)
    print(f"👁️  Watching {MEDIA_DROP_DIR} for audio files...")
    print(f"   Wiki: {WIKI_PATH}")
    print(f"   Poll interval: {poll_interval}s")
    print(f"   Press Ctrl+C to stop.\n")

    while True:
        try:
            files = get_unprocessed_audio()
            for f in files:
                # Wait a moment to ensure file is fully written
                size1 = os.path.getsize(f)
                time.sleep(3)
                size2 = os.path.getsize(f)
                if size1 != size2:
                    continue  # File still being written, skip for now
                process_audio(f)
        except KeyboardInterrupt:
            print("\n👋 Stopping watcher.")
            break
        except Exception as e:
            print(f"⚠️  Error in watch loop: {e}")
        time.sleep(poll_interval)


def main():
    parser = argparse.ArgumentParser(
        description="MuScriptor audio transcription watcher"
    )
    parser.add_argument(
        "--process", metavar="PATH",
        help="Process a single audio file and exit"
    )
    parser.add_argument(
        "--once", action="store_true",
        help="Process all unprocessed audio in drop dir and exit"
    )
    parser.add_argument(
        "--watch", action="store_true",
        help="Watch the drop directory continuously (default)"
    )
    args = parser.parse_args()

    os.makedirs(PROCESSED_MARKER, exist_ok=True)
    os.makedirs(PROCESSED_OUTPUT_DIR, exist_ok=True)

    if args.process:
        if not os.path.exists(args.process):
            print(f"❌ File not found: {args.process}")
            sys.exit(1)
        process_audio(args.process)
    elif args.once:
        files = get_unprocessed_audio()
        if not files:
            print("No unprocessed audio files found.")
        for f in files:
            process_audio(f)
    else:
        watch_loop()


if __name__ == "__main__":
    main()