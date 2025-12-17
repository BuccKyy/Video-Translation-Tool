# Process Documentation

## Video Translation Tool

**Time spent:** ~2.5 hours

---

## 1. Tool Selection

### What I used:

| Tool | Purpose | Why |
|------|---------|-----|
| **Groq API** | Whisper STT + Llama translation | Free tier, fast, good quality |
| **Edge TTS** | Text-to-Speech | Free (Microsoft), supports Vietnamese |
| **FFmpeg** | Video/audio processing | Industry standard, reliable |

### Alternatives considered:

- **OpenAI API**: Great quality but costs money, my free credits ran out
- **Google Cloud STT**: More complex setup, requires billing account
- **ElevenLabs**: Better voices but expensive ($5/month minimum)
- **Local Whisper**: Would be slow on my laptop

I chose Groq because it's free and quality is surprisingly good. Edge TTS was obvious choice for free Vietnamese TTS.

---

## 2. Prompt Engineering

### Translation prompt (what worked):

```
Translate to {language}. Keep it natural and concise. Return only the translation.
```

Simple works best. Tried longer prompts but they made output verbose.

### What didn't work:

1. **First attempt**: "You are a professional translator..." - output was too formal
2. **Second attempt**: Added rules about tone/emotion - model started adding explanations  
3. **Third attempt**: Kept it simple - much better results

### Key learning:
For translation, less is more. The model understands context well enough without detailed instructions.

---

## 3. Workflow

```
Input Video (English)
    ↓
[FFmpeg] Extract audio (.wav)
    ↓
[Whisper/Groq] Transcribe with timestamps
    ↓
[Llama/Groq] Translate each segment
    ↓
[Python] Generate SRT subtitles
    ↓
[Edge TTS] Generate Vietnamese audio
    ↓
[FFmpeg] Merge video + audio + subtitles
    ↓
Output Video (Vietnamese)
```

### Time breakdown:
- Research & setup: 30 min
- Core implementation: 1 hour
- Testing & debugging: 45 min
- Documentation: 15 min

---

## 4. Technical Decisions

### Why process segments individually?
- Better subtitle timing
- Easier to debug issues
- Can parallelize later if needed

### Why not use OpenAI TTS?
- Costs $15/1M characters
- Edge TTS is free and Vietnamese voice quality is decent

### Why single audio file instead of per-segment?
- Simpler implementation
- More natural flow (no awkward pauses)
- Trade-off: less precise lip sync

### What I'd do differently with more time:
1. Add audio speed adjustment to match original duration
2. Implement proper error handling and retries
3. Add progress bar for long videos
4. Support multiple speakers detection

---

## 5. Results

### Quality:
- **Transcription**: 9/10 - Whisper is very accurate for clear English
- **Translation**: 8/10 - Natural Vietnamese, occasionally misses idioms
- **TTS**: 7/10 - Clear but sounds a bit robotic
- **Sync**: 6/10 - Audio length doesn't match original perfectly

### Sample output:
- Input: 45-second BBC English tutorial
- Output: Vietnamese dubbed video with subtitles
- Processing time: ~30 seconds

### When it works well:
- Clear speech, single speaker
- Tutorial/educational content
- Moderate speaking pace

### When it doesn't work well:
- Heavy background music
- Multiple overlapping speakers
- Fast speech or strong accents
- Singing (not designed for music)

---

## 6. Cost Analysis

### Current (Free tier):
- Groq: Free (30 req/min limit)
- Edge TTS: Free
- **Total: $0**

### If using paid APIs:
| Service | Cost per 30s video |
|---------|-------------------|
| OpenAI Whisper | $0.003 |
| GPT-4o-mini | $0.001 |
| OpenAI TTS | $0.01 |
| **Total** | ~$0.015 |

For production, I'd probably use OpenAI for better quality, but Groq works great for prototyping.

---

## 7. Limitations & Future Improvements

### Current limitations:
1. Audio sync not perfect
2. Single voice for all content
3. No background music preservation
4. Rate limits on free tier

### Ideas for improvement:
1. Use voice cloning for better matching
2. Separate background audio and speech
3. Add speed adjustment for better sync
4. Batch processing with queue system
