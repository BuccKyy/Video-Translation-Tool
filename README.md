# Video Translation Tool

Translates English videos to Vietnamese (or other languages) with dubbed audio and subtitles.

## Features
- Speech-to-text using Whisper
- Translation using Llama 3.3
- Text-to-speech (Vietnamese voice)
- Auto-generated subtitles
- Works with any video format (mp4, mov, etc.)

## Requirements
- Python 3.8+
- FFmpeg
- Groq API key (free)

## Setup

```bash
# Install FFmpeg
brew install ffmpeg  # macOS

# Install Python packages
pip install -r requirements.txt

# Add your API key
echo "GROQ_API_KEY=your_key" > .env
```

Get free Groq API key: https://console.groq.com/keys

## Usage

```bash
# Basic usage
python main.py input/video.mp4 -o output

# Specify language
python main.py input/video.mp4 -o output -l Vietnamese
python main.py input/video.mp4 -o output -l Chinese
```

## Output

For each video, the tool generates:
- `video_Vietnamese.mp4` - dubbed video
- `video_Vietnamese.srt` - subtitles
- `video_result.json` - processing details

## Limitations
- Works best with clear speech, single speaker
- Audio timing may not be perfect
- Background music gets replaced

## Cost
Free! Uses Groq (free tier) and Edge TTS (Microsoft, free).
