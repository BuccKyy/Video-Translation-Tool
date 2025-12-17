"""
Video Translation Tool - Translates English videos to other languages
Author: AI Engineer Candidate
"""

import os
import subprocess
import json
import asyncio
from pathlib import Path
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

# Config
TARGET_LANG = "Vietnamese"
VOICE_VI = "vi-VN-HoaiMyNeural"
GROQ_KEY = os.getenv("GROQ_API_KEY", "")


def get_groq():
    from groq import Groq
    return Groq(api_key=GROQ_KEY)


def extract_audio(video, audio_out):
    """Extract audio track from video"""
    print("📤 Extracting audio...")
    cmd = ["ffmpeg", "-i", video, "-vn", "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1", "-y", audio_out]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"Error: {r.stderr}")
        return False
    print(f"✓ Audio: {audio_out}")
    return True


def transcribe(audio_path):
    """Transcribe using Whisper via Groq"""
    print("🎤 Transcribing...")
    client = get_groq()
    with open(audio_path, "rb") as f:
        result = client.audio.transcriptions.create(
            model="whisper-large-v3",
            file=f,
            response_format="verbose_json"
        )
    print("✓ Transcription done")
    return result


def translate(text, lang):
    """Translate text using LLM"""
    print(f"🌐 Translating to {lang}...")
    client = get_groq()
    
    resp = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": f"Translate to {lang}. Keep it natural and concise. Return only the translation."},
            {"role": "user", "content": text}
        ],
        temperature=0.3
    )
    return resp.choices[0].message.content.strip()


def parse_segments(transcript):
    """Parse transcript segments"""
    segments = []
    if hasattr(transcript, 'segments') and transcript.segments:
        for s in transcript.segments:
            if isinstance(s, dict):
                segments.append({"text": s.get('text', ''), "start": s.get('start', 0), "end": s.get('end', 0)})
            else:
                segments.append({"text": s.text, "start": s.start, "end": s.end})
    else:
        segments.append({"text": transcript.text, "start": 0.0, "end": 30.0})
    return segments


def translate_segments(segments, lang):
    """Translate all segments"""
    print(f"🌐 Translating {len(segments)} segments...")
    result = []
    for i, seg in enumerate(segments):
        translated = translate(seg["text"], lang)
        result.append({
            "start": seg["start"],
            "end": seg["end"],
            "original": seg["text"],
            "translated": translated
        })
        print(f"  [{i+1}/{len(segments)}] done")
    return result


async def generate_tts(text, output):
    """Generate speech using Edge TTS"""
    import edge_tts
    print("🔊 Generating speech...")
    comm = edge_tts.Communicate(text, VOICE_VI)
    await comm.save(output)
    print(f"✓ Audio: {output}")


def to_srt_time(seconds):
    """Convert seconds to SRT format"""
    td = timedelta(seconds=seconds)
    h, rem = divmod(td.seconds, 3600)
    m, s = divmod(rem, 60)
    ms = int(td.microseconds / 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def create_srt(segments, output):
    """Create SRT subtitle file"""
    print("📝 Creating subtitles...")
    lines = []
    for i, seg in enumerate(segments, 1):
        lines.append(str(i))
        lines.append(f"{to_srt_time(seg['start'])} --> {to_srt_time(seg['end'])}")
        lines.append(seg["translated"])
        lines.append("")
    
    with open(output, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✓ Subtitles: {output}")


def merge_video(video, audio, srt, output):
    """Merge video with new audio"""
    print("🎬 Merging...")
    
    # Replace audio
    temp = output.replace(".mp4", "_temp.mp4")
    cmd = ["ffmpeg", "-i", video, "-i", audio, "-c:v", "copy", "-map", "0:v:0", "-map", "1:a:0", "-shortest", "-y", temp]
    subprocess.run(cmd, capture_output=True)
    
    # Burn subtitles (optional, may fail on some systems)
    cmd2 = ["ffmpeg", "-i", temp, "-vf", f"subtitles={srt}", "-c:a", "copy", "-y", output]
    r = subprocess.run(cmd2, capture_output=True)
    
    if r.returncode != 0:
        os.rename(temp, output)
    elif os.path.exists(temp):
        os.remove(temp)
    
    print(f"✓ Output: {output}")


async def process(input_video, output_dir, lang=TARGET_LANG):
    """Main processing pipeline"""
    print(f"\n{'='*50}")
    print(f"Processing: {input_video}")
    print(f"Language: {lang}")
    print(f"{'='*50}\n")
    
    name = Path(input_video).stem
    temp = os.path.join(output_dir, "temp")
    os.makedirs(temp, exist_ok=True)
    
    audio = os.path.join(temp, f"{name}.wav")
    tts_audio = os.path.join(temp, f"{name}_tts.mp3")
    srt = os.path.join(output_dir, f"{name}_{lang}.srt")
    out_video = os.path.join(output_dir, f"{name}_{lang}.mp4")
    
    try:
        # Pipeline
        extract_audio(input_video, audio)
        transcript = transcribe(audio)
        segments = parse_segments(transcript)
        translated = translate_segments(segments, lang)
        create_srt(translated, srt)
        
        full_text = " ".join([s["translated"] for s in translated])
        await generate_tts(full_text, tts_audio)
        
        merge_video(input_video, tts_audio, srt, out_video)
        
        # Save result
        result = {
            "input": input_video,
            "output": out_video,
            "subtitle": srt,
            "original": transcript.text,
            "translated": full_text,
            "segments": len(segments)
        }
        with open(os.path.join(output_dir, f"{name}_result.json"), "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        print(f"\n✓ Done! Output: {out_video}\n")
        return result
        
    except Exception as e:
        print(f"\n✗ Error: {e}\n")
        return {"error": str(e)}


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Video Translation Tool")
    parser.add_argument("input", help="Input video")
    parser.add_argument("-o", "--output", default="output", help="Output dir")
    parser.add_argument("-l", "--lang", default="Vietnamese", help="Target language")
    args = parser.parse_args()
    
    if not GROQ_KEY:
        print("Error: Set GROQ_API_KEY in .env file")
        print("Get free key: https://console.groq.com/keys")
        return
    
    os.makedirs(args.output, exist_ok=True)
    asyncio.run(process(args.input, args.output, args.lang))


if __name__ == "__main__":
    main()
