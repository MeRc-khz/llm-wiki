#!/usr/bin/env python3
import os
import sys
import time
import hashlib
from datetime import datetime
import google.generativeai as genai

WIKI_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_TRANSCRIPTS_DIR = os.path.join(WIKI_DIR, "raw", "transcripts")
RAW_AUDIO_DIR = os.path.join(WIKI_DIR, "raw", "audio")

def load_env():
    env_path = os.path.join("/root/.hermes/.env")
    if not os.path.exists(env_path):
        return
    with open(env_path, "r") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, val = line.split("=", 1)
                os.environ[key.strip()] = val.strip().strip('"').strip("'")

def get_file_sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def main():
    load_env()
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("Error: GOOGLE_API_KEY not found in environment or /root/.hermes/.env", file=sys.stderr)
        sys.exit(1)

    audio_path = "/root/ntrafx_pod_feb13_2006_5min_clip.wav"
    if not os.path.exists(audio_path):
        print(f"Error: Source audio file not found at {audio_path}", file=sys.stderr)
        sys.exit(1)

    print(f"🚀 Copying raw audio to wiki repository...")
    dest_path = os.path.join(RAW_AUDIO_DIR, "ntrafx_pod_feb13_2006_5min_clip.wav")
    import shutil
    shutil.copy2(audio_path, dest_path)

    sha256 = get_file_sha256(dest_path)

    print(f"🎙️ Connecting to Gemini API & uploading {os.path.basename(dest_path)} (this may take a few moments)...")
    genai.configure(api_key=api_key)
    
    try:
        # Upload using Files API
        audio_file = genai.upload_file(path=dest_path)
        print(f"⏳ File uploaded. Waiting for processing to complete...")
        
        # Wait for processing
        while audio_file.state.name == "PROCESSING":
            time.sleep(2)
            audio_file = genai.get_file(audio_file.name)
            
        if audio_file.state.name == "FAILED":
            raise Exception("File processing failed on Gemini servers.")
            
        print(f"✨ Processing complete! Generating transcription...")
        
        # Fallback model list
        models_to_try = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-pro-latest", "gemini-1.5-flash-latest", "gemini-1.5-flash"]
        response = None
        for model_name in models_to_try:
            try:
                print(f"尝试使用 model: {model_name} ...")
                model = genai.GenerativeModel(model_name)
                prompt = (
                    "You are an expert audio transcriptionist. Please transcribe this audio file verbatim. "
                    "Organize the transcription logically and provide timestamps (e.g. [00:15]) for every "
                    "few sentences or logical breaks. Capture speaker turns if possible (e.g. Speaker 1, Speaker 2)."
                )
                response = model.generate_content([prompt, audio_file])
                print(f"✅ Success with model {model_name}!")
                break
            except Exception as e_model:
                print(f"⚠️ Failed with model {model_name}: {e_model}")
                continue
                
        if not response:
            raise Exception("All models failed to transcribe.")
            
        transcript_text = response.text
        
        # Clean up file from Google Cloud
        genai.delete_file(audio_file.name)
        print("🗑️ Cleaned up uploaded file from Gemini servers.")
        
    except Exception as e:
        print(f"❌ Gemini transcription failed: {e}", file=sys.stderr)
        sys.exit(1)

    # Compute hash of the generated transcript body
    transcript_sha256 = hashlib.sha256(transcript_text.encode('utf-8')).hexdigest()

    # Save to raw/transcripts/
    output_filename = "ntrafx_pod_feb13_2006_5min_clip.md"
    output_path = os.path.join(RAW_TRANSCRIPTS_DIR, output_filename)

    content = f"""---
title: "Ntrafx Podcast Clip (Feb 13, 2006)"
source_file: "raw/audio/ntrafx_pod_feb13_2006_5min_clip.wav"
ingested: {datetime.now().strftime('%Y-%m-%d')}
sha256: {transcript_sha256}
media_type: audio
duration: "00:05:00"
---

# Ntrafx Podcast Clip (Feb 13, 2006)

## Metadata
- **Source File:** raw/audio/ntrafx_pod_feb13_2006_5min_clip.wav
- **SHA256 of Source File:** {sha256}
- **Ingestion Date:** {datetime.now().strftime('%Y-%m-%d')}
- **Duration:** 5 minutes (Clip)

## Transcript
{transcript_text}
"""

    with open(output_path, "w") as f:
        f.write(content)

    print(f"🎉 Success! Ingested and transcribed: raw/transcripts/{output_filename}")

if __name__ == "__main__":
    main()
