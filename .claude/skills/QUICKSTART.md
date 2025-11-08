# Quick Start - 3Blue1Brown Video Generator

Get started creating beautiful math videos in 5 minutes!

## TL;DR

```bash
# 1. Install
sudo apt-get install -y python3-pip ffmpeg libcairo2-dev libpango1.0-dev texlive-full
pip install manim edge-tts pydub

# 2. Create
cd .claude/skills
python helpers/video_generator.py --new my_video

# 3. Edit
# Edit: videos/my_video/script.txt
# Edit: videos/my_video/scenes/main_scene.py

# 4. Generate
python helpers/video_generator.py --project my_video --full-pipeline

# 5. Watch
# Output: videos/my_video/output/final_video.mp4
```

## Step-by-Step

### 1. Install Dependencies (One Time)

**Quick install** (might miss some LaTeX features):
```bash
sudo apt-get install -y python3-pip ffmpeg libcairo2-dev libpango1.0-dev texlive
pip install manim edge-tts pydub
```

**Full install** (recommended, ~3GB):
```bash
sudo apt-get install -y python3-pip ffmpeg libcairo2-dev libpango1.0-dev texlive-full
pip install manim edge-tts pydub
```

**Check installation**:
```bash
cd .claude/skills
python helpers/video_generator.py --check
```

### 2. Create Your First Video

```bash
# Navigate to skills directory
cd .claude/skills

# Create a new project
python helpers/video_generator.py --new pythagorean
```

This creates:
```
videos/pythagorean/
  ├── scenes/main_scene.py   # Your animation code
  ├── script.txt              # Your narration
  ├── audio/                  # Generated audio (auto)
  └── output/                 # Final video (auto)
```

### 3. Write Your Script

Edit `videos/pythagorean/script.txt`:

```
The Pythagorean theorem is one of the most important concepts in mathematics.

It states that in a right triangle, the square of the hypotenuse equals
the sum of the squares of the other two sides.

Let's visualize this beautiful relationship.
```

### 4. Create Your Animation

Edit `videos/pythagorean/scenes/main_scene.py`:

```python
from manim import *

class MainScene(Scene):
    def construct(self):
        # Title (0-3s)
        title = Text("Pythagorean Theorem", font_size=60)
        self.play(Write(title))
        self.wait(2)
        self.play(FadeOut(title))

        # Equation (3-8s)
        equation = MathTex(r"a^2 + b^2 = c^2", font_size=72)
        self.play(Write(equation))
        self.wait(3)
        self.play(equation.animate.shift(UP*2).scale(0.7))

        # Triangle (8-15s)
        triangle = Polygon(ORIGIN, RIGHT*3, RIGHT*3+UP*4, color=BLUE)
        self.play(Create(triangle))
        self.wait(5)
```

### 5. Generate Video

```bash
python helpers/video_generator.py --project pythagorean --full-pipeline
```

Wait 1-2 minutes for rendering...

### 6. Watch Your Video!

```bash
# Video is saved here:
ls videos/pythagorean/output/final_video.mp4

# Play it (if you have a video player)
xdg-open videos/pythagorean/output/final_video.mp4
```

## What You Get

- 📹 **MP4 video** in 1080p (Full HD)
- 🎤 **Human-like voice** narration
- 🎨 **Professional animations** like 3Blue1Brown
- ⚡ **Synchronized** audio and visuals

## Common Commands

### Preview (Low Quality, Fast)
```bash
python helpers/video_generator.py --render scenes/main_scene.py MainScene --quality l
```

### Different Voice
```bash
# List voices
python helpers/video_generator.py --list-voices

# Use British female voice
python helpers/video_generator.py --project my_video --full-pipeline --voice en-GB-SoniaNeural
```

### Just Audio
```bash
python helpers/video_generator.py --audio "Your text here" --output test.mp3
```

### High Quality (4K)
```bash
python helpers/video_generator.py --project my_video --full-pipeline --quality k
```

## Manim Cheat Sheet

### Text
```python
text = Text("Hello World", font_size=48)
self.play(Write(text))
```

### Math Equations
```python
eq = MathTex(r"\int_0^\infty e^{-x^2} dx", font_size=60)
self.play(Write(eq))
```

### Shapes
```python
circle = Circle(radius=2, color=BLUE)
square = Square(side_length=3, color=RED)
self.play(Create(circle), Create(square))
```

### Animations
```python
self.play(Write(obj))           # Write text/equations
self.play(Create(obj))          # Draw shapes
self.play(FadeIn(obj))          # Fade in
self.play(FadeOut(obj))         # Fade out
self.play(Transform(a, b))      # Transform a into b
self.wait(2)                    # Wait 2 seconds
```

### 3Blue1Brown Colors
```python
BLUE_3B1B = "#58C4DD"
YELLOW_3B1B = "#FC6255"
GREEN_3B1B = "#83C167"

circle = Circle(color=BLUE_3B1B)
```

## Pro Tips

1. **Start simple**: Begin with basic text and shapes
2. **Preview often**: Use `-ql` for quick low-quality previews
3. **Match timing**: Adjust `self.wait()` to match your script
4. **Use colors**: Make important parts stand out
5. **Test audio first**: Generate and listen before final render

## Example Projects

Try the included example:

```bash
# Copy Euler's formula example
cp -r examples/eulers_formula ../../../videos/

# Generate it
python helpers/video_generator.py --project eulers_formula --full-pipeline

# Watch
xdg-open ../../videos/eulers_formula/output/final_video.mp4
```

## Troubleshooting

### "manim: command not found"
```bash
pip install --user manim
export PATH="$HOME/.local/bin:$PATH"
```

### "LaTeX Error"
```bash
sudo apt-get install -y texlive-latex-extra
```

### "No module named 'edge_tts'"
```bash
pip install edge-tts
```

### "ffmpeg not found"
```bash
sudo apt-get install -y ffmpeg
```

## Next Steps

- 📖 Read full documentation: `README.md`
- 🔧 See installation guide: `INSTALL.md`
- 📚 Learn Manim: https://docs.manim.community/
- 🎥 Watch 3Blue1Brown: https://www.youtube.com/c/3blue1brown

## Help

Stuck? Check:
- Full README: `.claude/skills/README.md`
- Installation guide: `.claude/skills/INSTALL.md`
- Example projects: `.claude/skills/examples/`
- Manim docs: https://docs.manim.community/

---

**Happy animating!** 🎬✨
