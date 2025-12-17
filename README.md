# 🎬 Video Translation Tool

> **AI-powered tool that translates English videos to Vietnamese with dubbed audio and subtitles.**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Cost](https://img.shields.io/badge/Cost-$0%20Free-brightgreen.svg)](#cost)

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🎤 **Speech-to-Text** | Transcribe English audio using Whisper |
| 🌐 **AI Translation** | Translate to Vietnamese using Llama 3.3 70B |
| 🔊 **Text-to-Speech** | Generate natural Vietnamese voice |
| 📝 **Auto Subtitles** | Create synchronized SRT subtitle files |
| 🎬 **Video Merge** | Combine everything into final video |
| 💰 **100% Free** | Uses free-tier APIs only |

---

## 🚀 Quick Start

```bash
# Clone the repo
git clone https://github.com/BuccKyy/Video-Translation-Tool.git
cd Video-Translation-Tool

# Install dependencies
pip install -r requirements.txt

# Add your API key (free)
echo "GROQ_API_KEY=your_key" > .env

# Run translation
python main.py input/video.mp4 -o output -l Vietnamese
```

> 🔑 Get free API key at: [console.groq.com/keys](https://console.groq.com/keys)

---

## 📋 Requirements

- **Python** 3.8+
- **FFmpeg** - Install via `brew install ffmpeg` (macOS) or `apt install ffmpeg` (Linux)
- **Groq API Key** - Free tier available

---

## 💻 Usage

### Basic Translation
```bash
python main.py input/video.mp4 -o output
```

### Specify Target Language
```bash
python main.py input/video.mp4 -o output -l Vietnamese
python main.py input/video.mp4 -o output -l Chinese
python main.py input/video.mp4 -o output -l Japanese
```

---

## 📁 Output

For each video, the tool generates:

```
output/
├── video_Vietnamese.mp4   # 🎬 Dubbed video with Vietnamese audio
├── video_Vietnamese.srt   # 📝 Subtitle file
└── video_result.json      # 📊 Processing details
```

---

## 🔧 How It Works

```
┌─────────────────┐
│  Input Video    │ (English)
└────────┬────────┘
         ▼
┌─────────────────┐
│  Extract Audio  │ FFmpeg
└────────┬────────┘
         ▼
┌─────────────────┐
│   Transcribe    │ Whisper (Groq)
└────────┬────────┘
         ▼
┌─────────────────┐
│    Translate    │ Llama 3.3 (Groq)
└────────┬────────┘
         ▼
┌─────────────────┐
│  Generate TTS   │ Edge TTS (Microsoft)
└────────┬────────┘
         ▼
┌─────────────────┐
│  Merge Video    │ FFmpeg
└────────┬────────┘
         ▼
┌─────────────────┐
│  Output Video   │ (Vietnamese)
└─────────────────┘
```

---

## 💰 Cost

| Mode | Cost |
|------|------|
| **Current (Free Tier)** | **$0** ✅ |
| Production (OpenAI) | ~$0.015/video |

This tool uses **Groq** (free) and **Edge TTS** (free), making it completely free to use!

---

## ⚠️ Limitations

- Works best with **clear speech, single speaker**
- Audio timing may not be perfect (no lip-sync)
- Background music gets replaced
- Rate limits on free tier (30 req/min)

---

## 📄 Documentation

See [PROCESS_DOCUMENTATION.md](PROCESS_DOCUMENTATION.md) for:
- Tool selection reasoning
- Prompt engineering details
- Technical decisions
- Performance analysis

---

## 🛠️ Tech Stack

| Component | Tool |
|-----------|------|
| STT | Whisper (via Groq) |
| LLM | Llama 3.3 70B (via Groq) |
| TTS | Edge TTS (Microsoft) |
| Video | FFmpeg |
| Language | Python |

---

## 📝 License

MIT License - feel free to use and modify!

---

<p align="center">
  <b>Built with ❤️ for AI Engineering Case Study</b>
</p>
