# torch.compile Explained - 3Blue1Brown Style Video

A comprehensive, ~5-minute educational video explaining PyTorch's `torch.compile` feature with professional animations and human narration.

## Overview

This video covers everything you need to know about `torch.compile`:
- What it is and why it matters
- The 4-stage compilation pipeline
- API parameters and their effects
- Code examples (inference, training, DDP)
- Dynamic shapes and trade-offs
- Graph breaks and how to fix them
- Performance optimization strategies

## Video Specifications

- **Duration**: ~5 minutes (300 seconds)
- **Resolution**: 1080p (configurable up to 4K)
- **Voice**: en-US-AndrewNeural (professional male voice)
- **Style**: 3Blue1Brown-inspired animations
- **Audio**: Synchronized human narration via edge-tts

## Prerequisites

Before generating the video, install dependencies:

```bash
# System dependencies (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install -y \
    python3-pip \
    ffmpeg \
    libcairo2-dev \
    libpango1.0-dev \
    texlive-full

# Python packages
pip install manim edge-tts pydub
```

For detailed installation instructions, see `.claude/skills/INSTALL.md`.

## Quick Start

### Option 1: Automatic (Recommended)

```bash
cd .claude/skills

# Generate the complete video
python helpers/video_generator.py \
    --project torch_compile_explained \
    --full-pipeline \
    --quality h
```

This will:
1. Generate audio from `script.txt` using edge-tts
2. Render Manim animations from `scenes/main_scene.py`
3. Combine audio and video
4. Save to `videos/torch_compile_explained/output/final_video.mp4`

**Estimated time**: 5-15 minutes depending on your hardware

### Option 2: Step-by-Step

```bash
cd videos/torch_compile_explained

# 1. Generate audio (human narration)
python ../../.claude/skills/helpers/video_generator.py \
    --audio "$(cat script.txt)" \
    --output audio/narration.mp3 \
    --voice en-US-AndrewNeural

# 2. Render Manim animation
manim -qh scenes/main_scene.py TorchCompileExplained

# 3. Find the rendered video (Manim outputs to media/)
# Usually in: media/videos/main_scene/1080p60/TorchCompileExplained.mp4

# 4. Combine audio and video
ffmpeg -i media/videos/main_scene/1080p60/TorchCompileExplained.mp4 \
       -i audio/narration.mp3 \
       -c:v copy -c:a aac -shortest \
       output/final_video.mp4
```

## Project Structure

```
torch_compile_explained/
├── scenes/
│   └── main_scene.py           # Manim animation code (~600 lines)
├── audio/
│   └── narration.mp3           # Generated audio (auto)
├── output/
│   └── final_video.mp4         # Final combined video (auto)
├── script.txt                  # Narration script with timing
└── README.md                   # This file
```

## Video Sections

| Section | Duration | Topics Covered |
|---------|----------|----------------|
| Introduction | 0-15s | Overview of torch.compile |
| What is it? | 15-45s | Core concept, transformation visualization |
| Pipeline | 45-90s | 4 stages: Dynamo, AOTAutograd, Lowering, Inductor |
| API | 90-150s | Parameters: fullgraph, dynamic, mode, backend |
| Code Examples | 150-195s | Inference, Training, DDP patterns |
| Dynamic Shapes | 195-225s | Shape flexibility vs performance trade-offs |
| Graph Breaks | 225-260s | What causes them, how to fix them |
| Performance | 260-285s | Optimization playbook |
| Conclusion | 285-300s | Summary and key takeaways |

## Animations Included

### Conceptual Visualizations
- **Compilation transformation**: Before/after code comparison
- **Pipeline overview**: 4-stage flow diagram
- **TorchDynamo**: Python bytecode → computation graph
- **AOTAutograd**: Forward/backward graph generation
- **Lowering**: Many ops → canonical ops reduction
- **TorchInductor**: Graph → GPU (Triton) and CPU (C++) kernels

### Code Examples
- Inference example with MLP
- Training loop with optimizer and backward pass
- DDP setup with correct ordering

### Technical Concepts
- Dynamic vs static shapes comparison
- Graph breaks visualization
- Performance optimization ladder

## Customization

### Change Voice

Use a different TTS voice:

```bash
# List available voices
edge-tts --list-voices

# Generate with British female voice
python ../../.claude/skills/helpers/video_generator.py \
    --project torch_compile_explained \
    --full-pipeline \
    --voice en-GB-SoniaNeural
```

Popular options:
- `en-US-AndrewNeural` - Male, professional (default)
- `en-US-AriaNeural` - Female, clear
- `en-GB-RyanNeural` - British male
- `en-GB-SoniaNeural` - British female

### Change Quality

```bash
# Low quality (480p) - fast preview
python helpers/video_generator.py \
    --project torch_compile_explained \
    --full-pipeline \
    --quality l

# Medium quality (720p)
--quality m

# High quality (1080p) - recommended
--quality h

# 4K quality - slow but highest quality
--quality k
```

### Modify Script

Edit `script.txt` to change narration:
- Adjust technical depth
- Add/remove sections
- Change pacing

**Important**: If you change the script, you may need to adjust timing in `scenes/main_scene.py` to match new audio duration.

### Modify Animations

Edit `scenes/main_scene.py` to:
- Change colors (currently using 3Blue1Brown scheme)
- Adjust animation speeds (`run_time` parameters)
- Add/remove visual elements
- Modify text sizes and positions

**Tip**: Use `manim -ql` (low quality) for fast preview while developing animations.

## Timing Synchronization

The script and animations are carefully synchronized:

1. **Script timing comments** (in `script.txt`) match `self.wait()` calls in Manim
2. Each section has allocated time (e.g., "45-90s" = 45 seconds)
3. `self.wait()` durations account for narration length

To verify synchronization:
```bash
# Check audio duration
ffprobe -i audio/narration.mp3 -show_entries format=duration -v quiet -of csv="p=0"

# Should be ~300 seconds (5 minutes)
```

## Troubleshooting

### Manim rendering fails

**LaTeX errors**:
```bash
sudo apt-get install -y texlive-full
```

**Import errors**:
```bash
pip install --upgrade manim
```

### Audio generation fails

**edge-tts connection issues**:
```bash
pip install --upgrade edge-tts
# Check internet connection
```

### Audio/video out of sync

1. Check audio duration matches expected ~300s
2. Verify `self.wait()` times in `main_scene.py`
3. Regenerate with `--shortest` flag in ffmpeg

### Preview is slow

Use low-quality mode for development:
```bash
manim -ql scenes/main_scene.py TorchCompileExplained
```

## Performance Tips

### Rendering
- **First render**: Can take 10-15 minutes (Manim compiles animations)
- **Subsequent renders**: Faster due to caching
- **Low quality**: 2-3 minutes
- **4K quality**: 30+ minutes

### Optimization
1. Start with `-ql` for quick previews
2. Use `-qm` (720p) for testing
3. Final render with `-qh` (1080p)
4. Only use `-qk` (4K) for production

## Advanced Usage

### Debug specific sections

Render only one section:
```python
# In main_scene.py, comment out sections you don't need:
def construct(self):
    self.intro_section()
    # self.what_is_compile_section()
    # self.pipeline_section()
    # ... etc
```

### Custom backend

Try different Manim rendering backends:
```bash
# Cairo backend (default)
manim -qh scenes/main_scene.py TorchCompileExplained

# OpenGL backend (faster, experimental)
manim -qh --renderer=opengl scenes/main_scene.py TorchCompileExplained
```

### Export frames

Extract individual frames:
```bash
manim -qh --format=png scenes/main_scene.py TorchCompileExplained
```

## Resources

### Learning More
- **Manim documentation**: https://docs.manim.community/
- **3Blue1Brown channel**: https://www.youtube.com/c/3blue1brown
- **edge-tts**: https://github.com/rany2/edge-tts
- **PyTorch compile docs**: https://pytorch.org/tutorials/intermediate/torch_compile_tutorial.html

### Related Skills
- Main skill documentation: `.claude/skills/3b1b-video.md`
- Installation guide: `.claude/skills/INSTALL.md`
- Quick start: `.claude/skills/QUICKSTART.md`

## Credits

- **Manim**: Mathematics Animation Engine by 3Blue1Brown community
- **edge-tts**: Microsoft Edge TTS by rany2
- **Content**: PyTorch documentation and community resources

## License

- Code: MIT License
- Content: Educational use

---

## Next Steps

1. ✅ Install dependencies (see Prerequisites)
2. ✅ Run the generation command
3. ✅ Review `output/final_video.mp4`
4. 🔧 Customize as needed
5. 📤 Share your educational content!

**Need help?** Check `.claude/skills/README.md` or open an issue.

---

**Generated with**: Claude Code + 3Blue1Brown Video Generator Skill
