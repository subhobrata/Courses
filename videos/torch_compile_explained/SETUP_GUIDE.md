# Complete Setup Guide - Generate the torch.compile Video

## 🎯 What You Have

All the source files needed to generate a professional 5-minute video:

✅ **script.txt** - Complete narration script (6,302 characters, ~300 seconds)
✅ **scenes/main_scene.py** - Full Manim animation code (600+ lines)
✅ **GENERATE.sh** - Automated generation script
✅ **README.md** - Comprehensive documentation

## 🚀 Quick Start (On Your Local Machine)

### Step 1: Install System Dependencies

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install -y \
    python3-pip \
    ffmpeg \
    libcairo2-dev \
    libpango1.0-dev \
    pkg-config \
    texlive-latex-base \
    texlive-latex-extra
```

**macOS (with Homebrew):**
```bash
brew install python3 ffmpeg cairo pango pkg-config
brew install --cask mactex
```

**Windows (WSL2 recommended):**
Use Ubuntu instructions in WSL2, or install:
- Python from python.org
- FFmpeg from ffmpeg.org
- MiKTeX for LaTeX
- Cairo binaries

### Step 2: Install Python Packages

```bash
pip install manim edge-tts pydub
```

### Step 3: Generate the Video

```bash
cd videos/torch_compile_explained
./GENERATE.sh
```

**That's it!** The video will be in `output/final_video.mp4`

## ⏱️ Expected Timeline

- **Audio generation**: ~10 seconds
- **Manim rendering**: 5-15 minutes (depending on hardware)
- **Combining**: ~5 seconds
- **Total**: ~10-20 minutes

## 📊 What Gets Generated

### Audio File
- **File**: `audio/narration.mp3`
- **Duration**: ~300 seconds (5 minutes)
- **Voice**: en-US-AndrewNeural (professional male)
- **Quality**: High-quality neural TTS
- **Size**: ~2-3 MB

### Video File
- **File**: `output/final_video.mp4`
- **Resolution**: 1080p (1920x1080)
- **Duration**: ~300 seconds (5 minutes)
- **Codec**: H.264
- **Size**: ~50-100 MB (depending on quality)

### Intermediate Files
- `media/videos/main_scene/*/` - Manim output directory
- Various cache files (automatically managed)

## 🎨 Customization Options

### Change Quality

```bash
./GENERATE.sh --quality l    # 480p - fast preview
./GENERATE.sh --quality m    # 720p
./GENERATE.sh --quality h    # 1080p (default)
./GENERATE.sh --quality k    # 4K
```

### Change Voice

```bash
# List available voices
edge-tts --list-voices | grep "en-"

# Use different voice
./GENERATE.sh --voice en-US-AriaNeural      # Female US
./GENERATE.sh --voice en-GB-RyanNeural      # Male British
./GENERATE.sh --voice en-GB-SoniaNeural     # Female British
```

### Render Specific Sections

Edit `scenes/main_scene.py` and comment out sections:

```python
def construct(self):
    self.intro_section()           # Keep
    # self.what_is_compile_section()  # Skip
    self.pipeline_section()         # Keep
    # ... etc
```

## 🐛 Troubleshooting

### "manim: command not found"

```bash
pip install --user manim
export PATH="$HOME/.local/bin:$PATH"
```

### LaTeX errors

```bash
# Full installation (recommended)
sudo apt-get install texlive-full

# Or minimal (faster but may miss fonts)
sudo apt-get install texlive-latex-base texlive-latex-extra
```

### "pangocairo not found"

```bash
sudo apt-get install libcairo2-dev libpango1.0-dev pkg-config
pip install --upgrade --force-reinstall pycairo
```

### Audio generation fails

```bash
# Check internet connection
ping api.msedgeservices.com

# Update edge-tts
pip install --upgrade edge-tts
```

### Out of memory during rendering

```bash
# Use lower quality for testing
./GENERATE.sh --quality l

# Or render sections separately (edit main_scene.py)
```

### Video/audio out of sync

The script is designed to be perfectly synced. If you modify the script:

1. Check audio duration:
   ```bash
   ffprobe -i audio/narration.mp3 -show_entries format=duration -v quiet -of csv="p=0"
   ```

2. Adjust `self.wait()` times in `main_scene.py` to match

## 📖 Video Content Summary

### Section Breakdown

| Time | Section | Key Animations |
|------|---------|----------------|
| 0-15s | Introduction | Title, PyTorch 2.x badge |
| 15-45s | What is compile? | Code transformation, speedup visualization |
| 45-90s | Pipeline | 4-stage flow: Dynamo, AOTAutograd, Lowering, Inductor |
| 90-150s | API Parameters | fullgraph, dynamic, mode, backend explanations |
| 150-195s | Code Examples | Inference, training, DDP code displays |
| 195-225s | Dynamic Shapes | Shape variations, trade-off visualization |
| 225-260s | Graph Breaks | Problem code, graph splits, solutions |
| 260-285s | Performance | 5-step optimization ladder |
| 285-300s | Conclusion | Summary points, final message |

### Technical Topics Covered

✅ **What torch.compile is** - Graph compiler, JIT compilation
✅ **How it works** - TorchDynamo bytecode tracing
✅ **Pipeline stages** - Complete 4-stage breakdown
✅ **API parameters** - All major options explained
✅ **Code patterns** - Real inference/training/DDP examples
✅ **Dynamic shapes** - When and why to use them
✅ **Graph breaks** - Causes and solutions
✅ **Debugging** - Tools and techniques
✅ **Performance** - Optimization strategies

## 🎬 Preview Without Installing

Want to see what it looks like before installing everything?

### Preview Script
```bash
cat script.txt
```

### Preview Code Structure
```bash
# See animation sections
grep "def.*_section" scenes/main_scene.py

# See timing
grep "self.wait" scenes/main_scene.py
```

### Estimate Rendering Time
```bash
# Quick preview (low quality)
manim -ql --dry_run scenes/main_scene.py TorchCompileExplained

# Shows how long it would take without actually rendering
```

## 💡 Pro Tips

### Speed Up Development

1. **Preview sections individually**:
   ```python
   # In main_scene.py
   def construct(self):
       self.pipeline_section()  # Test just this section
   ```

2. **Use low quality for testing**:
   ```bash
   manim -ql scenes/main_scene.py TorchCompileExplained
   ```

3. **Cache is your friend**:
   - Manim caches animations
   - Second render of same content is much faster

### Improve Quality

1. **Higher resolution**:
   ```bash
   ./GENERATE.sh --quality k  # 4K
   ```

2. **Adjust audio quality in script**:
   ```python
   # In GENERATE.sh, add rate adjustment
   communicate = edge_tts.Communicate(text, voice, rate="+0%")
   # Try rate="-5%" for slower, more clear speech
   ```

3. **Fine-tune timing**:
   - Listen to audio first
   - Adjust `self.wait()` in animations
   - Re-render

## 🔧 Manual Generation (If Script Fails)

### 1. Generate Audio
```bash
python3 << 'EOF'
import asyncio
import edge_tts

async def gen():
    with open('script.txt') as f:
        text = f.read()
    # Remove comments
    text = '\n'.join([l for l in text.split('\n') if not l.startswith('#') and l.strip()])
    comm = edge_tts.Communicate(text, "en-US-AndrewNeural")
    await comm.save("audio/narration.mp3")

asyncio.run(gen())
EOF
```

### 2. Render Animation
```bash
manim -qh scenes/main_scene.py TorchCompileExplained
```

### 3. Find and Combine
```bash
# Find the rendered video
VIDEO=$(find media/videos/main_scene -name "TorchCompileExplained.mp4" | head -1)

# Combine
ffmpeg -i "$VIDEO" -i audio/narration.mp3 \
       -c:v copy -c:a aac -shortest \
       output/final_video.mp4
```

## 📦 Alternative: Docker

If you have Docker installed:

```dockerfile
FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    ffmpeg libcairo2-dev libpango1.0-dev \
    texlive-latex-base texlive-latex-extra \
    && rm -rf /var/lib/apt/lists/*

RUN pip install manim edge-tts pydub

WORKDIR /workspace
```

Then:
```bash
docker build -t torch-compile-video .
docker run -v $(pwd):/workspace torch-compile-video ./GENERATE.sh
```

## ✅ Verification Checklist

Before generating, verify:

- [ ] Python 3.8+ installed: `python3 --version`
- [ ] FFmpeg installed: `ffmpeg -version`
- [ ] Manim installed: `python3 -c "import manim; print(manim.__version__)"`
- [ ] edge-tts installed: `python3 -c "import edge_tts; print('OK')"`
- [ ] Internet connection: `ping api.msedgeservices.com`
- [ ] Enough disk space: `df -h` (need ~500MB free)

## 🎓 Learning Resources

While the video generates, learn more:

- **Manim tutorial**: https://docs.manim.community/en/stable/tutorials.html
- **torch.compile docs**: https://pytorch.org/docs/stable/torch.compiler.html
- **3Blue1Brown**: https://www.youtube.com/c/3blue1brown

## 📝 Next Steps

1. ✅ Install dependencies on your local machine
2. ✅ Run `./GENERATE.sh`
3. ✅ Wait 10-20 minutes
4. ✅ Watch `output/final_video.mp4`
5. ✅ Share with your team/students!

## 🆘 Still Having Issues?

1. Check the README.md for detailed documentation
2. See `.claude/skills/INSTALL.md` for installation help
3. Try the manual generation steps above
4. Use Docker for isolated environment

---

**The video is ready to generate - you just need the dependencies installed!** 🚀
