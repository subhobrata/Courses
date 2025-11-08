# 3Blue1Brown Style Video Generator Skill

Create stunning mathematical and educational animation videos with human audio narration, inspired by the style of 3Blue1Brown.

## Quick Start

### 1. Install Dependencies

```bash
# System dependencies (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install -y python3-pip ffmpeg libcairo2-dev libpango1.0-dev \
    texlive-full texlive-latex-extra texlive-fonts-extra

# Python packages
pip install manim edge-tts pydub
```

### 2. Check Installation

```bash
cd .claude/skills
python helpers/video_generator.py --check
```

### 3. Create Your First Video

```bash
# Create a new project
python helpers/video_generator.py --new my_first_video

# Edit the script and scene files
# - videos/my_first_video/script.txt (your narration)
# - videos/my_first_video/scenes/main_scene.py (your animations)

# Run the full pipeline
python helpers/video_generator.py --project my_first_video --full-pipeline
```

Your video will be saved in `videos/my_first_video/output/final_video.mp4`!

## Features

✨ **3Blue1Brown-style animations** using Manim
🎤 **High-quality human-like audio** using edge-tts (free!)
🎬 **Automatic synchronization** of audio and video
📦 **Complete project templates** to get started quickly
🎨 **Professional quality** output in up to 4K resolution

## Usage Examples

### Example 1: Pythagorean Theorem Video

```bash
# Create project
python helpers/video_generator.py --new pythagorean

# The project structure:
videos/pythagorean/
  ├── scenes/main_scene.py   # Edit this - your Manim code
  ├── script.txt              # Edit this - your narration
  ├── audio/                  # Generated audio goes here
  └── output/                 # Final video goes here
```

Edit `scenes/main_scene.py`:
```python
from manim import *

class MainScene(Scene):
    def construct(self):
        # Title (0-3s)
        title = Text("The Pythagorean Theorem", font_size=60)
        self.play(Write(title))
        self.wait(2)
        self.play(FadeOut(title))

        # Theorem (3-8s)
        theorem = MathTex(r"a^2 + b^2 = c^2", font_size=72)
        self.play(Write(theorem))
        self.wait(3)
        self.play(theorem.animate.shift(UP*2).scale(0.7))

        # Triangle visualization (8-15s)
        triangle = Polygon(ORIGIN, RIGHT*3, RIGHT*3+UP*4, color=BLUE)
        a_label = MathTex("a").next_to(triangle, DOWN)
        b_label = MathTex("b").next_to(triangle, RIGHT)
        c_label = MathTex("c").next_to(triangle, UL)

        self.play(Create(triangle))
        self.play(Write(a_label), Write(b_label), Write(c_label))
        self.wait(5)
```

Edit `script.txt`:
```
The Pythagorean Theorem is one of the most beautiful and fundamental concepts in mathematics.

It states that in a right triangle, the square of the hypotenuse equals the sum of squares of the other two sides.

Let's visualize this elegant relationship and see why it's so important.
```

Generate the video:
```bash
python helpers/video_generator.py --project pythagorean --full-pipeline
```

### Example 2: Just Generate Audio

```bash
python helpers/video_generator.py \
    --audio "Welcome to my mathematical journey" \
    --output welcome.mp3 \
    --voice en-US-AndrewNeural
```

### Example 3: Custom Voice and Speed

```bash
# List available voices
python helpers/video_generator.py --list-voices

# Generate with British female voice, 10% faster
python helpers/video_generator.py \
    --audio "Today we explore calculus" \
    --output narration.mp3 \
    --voice en-GB-SoniaNeural \
    --rate "+10%"
```

### Example 4: Render Only (No Audio)

```bash
python helpers/video_generator.py \
    --render scenes/my_scene.py \
    --scene MySceneClass \
    --quality h
```

Quality options:
- `l` = 480p (fast preview)
- `m` = 720p
- `h` = 1080p (default)
- `k` = 4K (slow, high quality)

### Example 5: Combine Existing Video and Audio

```bash
python helpers/video_generator.py \
    --combine animation.mp4 narration.mp3 \
    --output final.mp4
```

## Available Voices

### Professional Male Voices
- `en-US-AndrewNeural` - Clear, professional (recommended for math)
- `en-US-GuyNeural` - Warm, conversational
- `en-GB-RyanNeural` - British, authoritative

### Professional Female Voices
- `en-US-AriaNeural` - Clear, educational (great for tutorials)
- `en-US-JennyNeural` - Friendly, approachable
- `en-GB-SoniaNeural` - British, professional

See all voices:
```bash
python helpers/video_generator.py --list-voices
```

## Manim Animation Tips

### Basic Animations

```python
from manim import *

class Demo(Scene):
    def construct(self):
        # Text
        text = Text("Hello World")
        self.play(Write(text))
        self.wait(1)

        # Equations
        eq = MathTex(r"\int_0^\infty e^{-x^2} dx = \frac{\sqrt{\pi}}{2}")
        self.play(Transform(text, eq))
        self.wait(2)

        # Shapes
        circle = Circle(radius=2, color=BLUE)
        self.play(Create(circle))
        self.wait(1)
```

### 3Blue1Brown Style Colors

```python
BLUE_3B1B = "#58C4DD"
YELLOW_3B1B = "#FC6255"
GREEN_3B1B = "#83C167"

circle = Circle(color=BLUE_3B1B)
```

### Smooth Animations

```python
# Slow, smooth fade
self.play(FadeIn(obj), run_time=2)

# Transform with ease
self.play(Transform(a, b), run_time=1.5, rate_func=smooth)
```

### Camera Movement

```python
# Zoom in
self.play(self.camera.frame.animate.scale(0.5))

# Pan to object
self.play(self.camera.frame.animate.move_to(obj))
```

## Timing Synchronization

Match your Manim `wait()` times to your script:

```python
# Script: "Hello" (2 seconds)
self.play(Write(text))
self.wait(2)  # Match audio duration

# Script: "This is important" (3 seconds)
self.play(Create(circle))
self.wait(3)  # Match audio duration
```

Pro tip: Generate audio first, check its duration with:
```bash
ffprobe -i narration.mp3 -show_entries format=duration -v quiet -of csv="p=0"
```

## Project Structure

After creating a project with `--new`:

```
videos/your_project/
├── scenes/
│   └── main_scene.py      # Your Manim animation code
├── audio/
│   └── narration.mp3      # Generated audio (auto)
├── output/
│   └── final_video.mp4    # Final combined video (auto)
└── script.txt             # Your narration script
```

## Workflow

1. **Plan**: Outline your video concept and script
2. **Script**: Write narration in `script.txt`
3. **Code**: Create animations in `scenes/main_scene.py`
4. **Preview**: Render with `-ql` for quick preview
5. **Audio**: Test audio generation separately
6. **Sync**: Adjust wait times to match audio
7. **Final**: Run full pipeline with `-qh` for 1080p

## Troubleshooting

### Manim installation fails
```bash
# Install system dependencies first
sudo apt-get install libcairo2-dev libpango1.0-dev ffmpeg

# Then install manim
pip install --upgrade manim
```

### LaTeX errors
```bash
# Install full TeX distribution
sudo apt-get install texlive-full
```

### Audio/video out of sync
- Check audio duration: `ffprobe narration.mp3`
- Adjust `self.wait()` times in Manim scene
- Use `--shortest` in manual ffmpeg commands

### Voice not found
```bash
# List all voices
edge-tts --list-voices

# Update edge-tts
pip install --upgrade edge-tts
```

## Advanced: Manual Control

### Generate Audio Only
```python
import asyncio
import edge_tts

async def generate():
    text = "Your narration here"
    communicate = edge_tts.Communicate(text, "en-US-AndrewNeural")
    await communicate.save("output.mp3")

asyncio.run(generate())
```

### Render Manim Manually
```bash
manim -qh scene.py SceneClass
```

### Combine Manually
```bash
ffmpeg -i video.mp4 -i audio.mp3 -c:v copy -c:a aac -shortest output.mp4
```

## Resources

- 📚 [Manim Documentation](https://docs.manim.community/)
- 🎥 [3Blue1Brown Channel](https://www.youtube.com/c/3blue1brown)
- 🎤 [edge-tts GitHub](https://github.com/rany2/edge-tts)
- 🎬 [FFmpeg Guide](https://ffmpeg.org/documentation.html)

## Examples Gallery

See the `examples/` directory for complete working examples:
- `examples/eulers_formula/` - Complex numbers visualization
- `examples/derivatives/` - Calculus animation
- `examples/pythagorean/` - Geometric proof

## Tips for Great Videos

1. ✅ **Start simple** - Begin with basic animations
2. ✅ **Preview often** - Use low quality renders to iterate quickly
3. ✅ **Time carefully** - Match audio and visual timing
4. ✅ **Use color** - Make important concepts stand out
5. ✅ **Build gradually** - Don't show everything at once
6. ✅ **Test audio** - Listen to narration before final render
7. ✅ **Version control** - Keep your scene files in git

## License

This skill uses:
- Manim (MIT License)
- edge-tts (GPLv3)
- FFmpeg (LGPL/GPL)

Your generated videos are yours to use freely!
