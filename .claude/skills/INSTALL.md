# Installation Guide - 3Blue1Brown Video Generator

Complete installation guide for the 3Blue1Brown-style video generator skill.

## Prerequisites

- Python 3.8 or higher
- Ubuntu/Debian Linux (or similar)
- At least 2GB free disk space (for LaTeX packages)
- Internet connection (for package downloads)

## Step-by-Step Installation

### 1. Update System

```bash
sudo apt-get update
sudo apt-get upgrade -y
```

### 2. Install System Dependencies

```bash
# Core dependencies
sudo apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    build-essential

# FFmpeg for video processing
sudo apt-get install -y ffmpeg

# Cairo and Pango for graphics
sudo apt-get install -y \
    libcairo2-dev \
    libpango1.0-dev \
    libpangocairo-1.0-0 \
    pkg-config

# LaTeX for mathematical typesetting
# Note: This is a large download (~3GB)
sudo apt-get install -y \
    texlive \
    texlive-latex-extra \
    texlive-fonts-extra \
    texlive-latex-recommended \
    texlive-science \
    texlive-formats-extra \
    texlive-luatex \
    cm-super \
    dvipng
```

**For minimal LaTeX installation (faster, but may have missing fonts):**
```bash
sudo apt-get install -y \
    texlive-base \
    texlive-latex-base \
    texlive-latex-recommended
```

### 3. Install Python Packages

```bash
# Upgrade pip
pip install --upgrade pip

# Install Manim Community Edition
pip install manim

# Install audio processing
pip install edge-tts pydub

# Optional: Additional TTS options
pip install gtts              # Google TTS (simpler, lower quality)
# pip install openai          # OpenAI TTS (requires API key)
# pip install elevenlabs      # ElevenLabs (requires API key)
```

### 4. Verify Installation

```bash
# Navigate to skills directory
cd .claude/skills

# Run check command
python helpers/video_generator.py --check
```

You should see: ✅ All dependencies installed correctly

### 5. Test Installation

Create a test video:

```bash
# Create test project
python helpers/video_generator.py --new test_video

# Generate a simple audio file
python helpers/video_generator.py \
    --audio "Hello, this is a test of the video generator" \
    --output test.mp3

# Test Manim rendering
echo 'from manim import *
class Test(Scene):
    def construct(self):
        text = Text("Test")
        self.play(Write(text))
' > test_scene.py

manim -ql test_scene.py Test

# Clean up
rm test.mp3 test_scene.py
```

## Troubleshooting

### Issue: "manim: command not found"

**Solution 1**: Install in user directory
```bash
pip install --user manim
export PATH="$HOME/.local/bin:$PATH"
```

**Solution 2**: Use virtual environment
```bash
python -m venv manim_env
source manim_env/bin/activate
pip install manim edge-tts pydub
```

### Issue: LaTeX errors when rendering

**Error**: `LaTeX Error: File 'standalone.cls' not found`

**Solution**: Install additional LaTeX packages
```bash
sudo apt-get install -y texlive-latex-extra
```

**Error**: Font warnings or missing symbols

**Solution**: Install full TeX distribution
```bash
sudo apt-get install -y texlive-full
```

### Issue: Cairo or Pango errors

**Error**: `cairo.h: No such file or directory`

**Solution**: Install development headers
```bash
sudo apt-get install -y libcairo2-dev libpango1.0-dev
pip install --upgrade --force-reinstall pycairo
```

### Issue: edge-tts connection errors

**Error**: `ConnectionError` or `Timeout`

**Solution 1**: Check internet connection
```bash
ping microsoft.com
```

**Solution 2**: Use alternative TTS
```bash
# Google TTS (offline after initial download)
pip install gtts
```

**Solution 3**: Update edge-tts
```bash
pip install --upgrade edge-tts
```

### Issue: FFmpeg not found

**Solution**: Install from package manager
```bash
# Ubuntu/Debian
sudo apt-get install -y ffmpeg

# Check installation
ffmpeg -version
```

### Issue: Slow rendering

**Tips**:
1. Use lower quality for previews: `manim -ql` instead of `manim -qh`
2. Reduce frame rate: `manim -r 30` (instead of default 60fps)
3. Disable preview: Remove `-p` flag
4. Use fewer objects in complex scenes
5. Cache partial renders

### Issue: Out of disk space

LaTeX packages require ~3GB. Free up space:
```bash
# Check disk usage
df -h

# Clean apt cache
sudo apt-get clean
sudo apt-get autoclean

# Remove old packages
sudo apt-get autoremove
```

## Platform-Specific Notes

### macOS

```bash
# Install Homebrew first (if not already installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install dependencies
brew install python3 ffmpeg cairo pango pkg-config
brew install --cask mactex  # For LaTeX

# Install Python packages
pip3 install manim edge-tts pydub
```

### Windows (WSL2)

Use Windows Subsystem for Linux and follow the Ubuntu instructions above.

**Alternative (Native Windows)**:
1. Install Python from python.org
2. Install FFmpeg from ffmpeg.org
3. Install MiKTeX for LaTeX
4. Install Cairo binaries
5. Use pip to install Python packages

Note: WSL2 is recommended for easier setup.

### Docker (Any Platform)

```dockerfile
FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libcairo2-dev \
    libpango1.0-dev \
    texlive-latex-base \
    texlive-latex-extra \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
RUN pip install manim edge-tts pydub

WORKDIR /workspace
```

Build and run:
```bash
docker build -t 3b1b-generator .
docker run -it -v $(pwd):/workspace 3b1b-generator bash
```

## Verification Checklist

After installation, verify:

- [ ] `python3 --version` shows Python 3.8+
- [ ] `pip --version` works
- [ ] `ffmpeg -version` shows FFmpeg installed
- [ ] `manim --version` shows Manim version
- [ ] `edge-tts --list-voices` lists available voices
- [ ] `pdflatex --version` shows LaTeX installed
- [ ] Can create a simple Manim scene
- [ ] Can generate audio with edge-tts
- [ ] Helper script runs: `python helpers/video_generator.py --check`

## Minimal Installation (Quick Start)

For quick testing without full LaTeX:

```bash
# Minimal system packages
sudo apt-get install -y python3-pip ffmpeg libcairo2-dev libpango1.0-dev

# Python packages only
pip install manim edge-tts pydub

# Use text instead of LaTeX in scenes
from manim import Text  # Instead of MathTex
```

**Limitation**: Cannot render mathematical equations, only plain text.

## Updating

Keep packages up to date:

```bash
# Update system packages
sudo apt-get update && sudo apt-get upgrade -y

# Update Python packages
pip install --upgrade manim edge-tts pydub

# Update Manim to latest
pip install --upgrade manim
```

## Uninstalling

To remove everything:

```bash
# Remove Python packages
pip uninstall manim edge-tts pydub -y

# Remove system packages (be careful with this)
sudo apt-get remove texlive* -y
sudo apt-get autoremove -y
```

## Getting Help

If you encounter issues:

1. Check Manim documentation: https://docs.manim.community/
2. Manim Discord: https://discord.gg/manim
3. GitHub issues: https://github.com/ManimCommunity/manim/issues
4. edge-tts issues: https://github.com/rany2/edge-tts/issues

## Next Steps

After installation:

1. Read the main README: `.claude/skills/README.md`
2. Try the Euler's formula example: `.claude/skills/examples/eulers_formula/`
3. Create your first video: `python helpers/video_generator.py --new my_first_video`
4. Read the skill documentation: `.claude/skills/3b1b-video.md`

Happy animating! 🎬
