# 3Blue1Brown Style Video Generator

## Description
Create stunning mathematical and educational animation videos in the style of 3Blue1Brown using Manim (Mathematical Animation Engine) with synchronized human-like audio narration.

## Overview
This skill enables you to generate professional educational videos with:
- Mathematical and visual animations using Manim
- High-quality human-like voiceover using TTS
- Automatic synchronization of audio and visuals
- Export to MP4 format

## Dependencies

### Required Software
```bash
# Python 3.8+
sudo apt-get update
sudo apt-get install -y python3-pip python3-dev

# System dependencies for Manim
sudo apt-get install -y \
    ffmpeg \
    libcairo2-dev \
    libpango1.0-dev \
    texlive-full \
    texlive-latex-extra \
    texlive-fonts-extra \
    texlive-latex-recommended \
    texlive-science \
    tipa \
    libpangocairo-1.0-0

# Install Manim Community Edition
pip install manim

# Install audio generation tools
pip install edge-tts  # Free, high-quality TTS
pip install pydub     # Audio manipulation
```

### Alternative TTS Options
- **edge-tts** (Free): Microsoft Edge TTS - High quality, no API key needed
- **OpenAI TTS**: Requires API key, very natural voices
- **ElevenLabs**: Requires API key, most realistic but paid
- **gTTS**: Google TTS, free but lower quality

## Usage Instructions

When the user requests a 3Blue1Brown-style video, follow these steps:

### Step 1: Understand the Content
Ask the user for:
- **Topic**: What subject should the video cover?
- **Duration**: Target video length (default: 30-60 seconds)
- **Complexity**: Beginner, Intermediate, or Advanced
- **Voice**: Which voice to use for narration (default: en-US-AndrewNeural for male, en-US-AriaNeural for female)

### Step 2: Generate Script
Create a detailed script that includes:
- Narration text with timing markers
- Animation descriptions for each section
- Mathematical concepts to visualize
- Transitions and visual effects

Example script format:
```
[0-5s] "Today, we're going to explore the beauty of Euler's formula"
Animation: Fade in title, show e^(iπ) + 1 = 0

[5-12s] "Starting with the exponential function..."
Animation: Show exponential growth graph, transform to complex plane

[12-20s] "When we venture into the complex plane, something magical happens"
Animation: Show unit circle, plot e^(iθ)
```

### Step 3: Create Manim Scene
Write a Python file using Manim to create the animations:

```python
from manim import *

class VideoScene(Scene):
    def construct(self):
        # Example: Euler's formula visualization
        title = Tex(r"$e^{i\pi} + 1 = 0$", font_size=72)
        self.play(Write(title))
        self.wait(2)

        # Add more animations based on script
        # Use self.play() for animations
        # Use self.wait() for pauses
```

### Step 4: Generate Audio
Generate audio narration using edge-tts or another TTS service:

```python
import edge_tts
import asyncio

async def generate_audio(text, output_file, voice="en-US-AndrewNeural"):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_file)

# Generate narration
narration = "Your full narration text here..."
asyncio.run(generate_audio(narration, "narration.mp3"))
```

### Step 5: Render Video
Render the Manim scene:

```bash
manim -pqh scene.py VideoScene
```

This creates a high-quality MP4 file.

### Step 6: Synchronize Audio and Video
Combine the animation with narration:

```bash
ffmpeg -i animation.mp4 -i narration.mp3 -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 final_video.mp4
```

## Common Animation Patterns

### Mathematical Equations
```python
equation = MathTex(r"\int_0^\infty e^{-x^2} dx = \frac{\sqrt{\pi}}{2}")
self.play(Write(equation))
```

### Geometric Transformations
```python
square = Square()
circle = Circle()
self.play(Transform(square, circle))
```

### Graphs and Plots
```python
axes = Axes(x_range=[-3, 3], y_range=[-5, 5])
graph = axes.plot(lambda x: x**2, color=BLUE)
self.play(Create(axes), Create(graph))
```

### Text and Narration Sync
```python
text = Text("This appears first")
self.play(Write(text))
self.wait(2)  # Sync with 2 seconds of narration
```

## Voice Options (edge-tts)

Popular English voices:
- **en-US-AndrewNeural**: Male, professional, great for math
- **en-US-AriaNeural**: Female, clear, educational
- **en-US-GuyNeural**: Male, warm, conversational
- **en-GB-RyanNeural**: British male, authoritative
- **en-GB-SoniaNeural**: British female, clear

List all available voices:
```bash
edge-tts --list-voices
```

## Output Structure

Create the following directory structure for each video:
```
videos/
  ├── [topic_name]/
  │   ├── script.txt           # Full narration script
  │   ├── scene.py             # Manim animation code
  │   ├── narration.mp3        # Generated audio
  │   ├── animation.mp4        # Manim output
  │   └── final_video.mp4      # Combined result
```

## Best Practices

1. **Timing**: Manim animations should match narration duration
   - Use `self.wait()` to control timing
   - Preview video length before adding audio

2. **Visual Clarity**:
   - Keep text large and readable (font_size=48+)
   - Use high contrast colors
   - Don't overcrowd the frame

3. **Pacing**:
   - Allow 2-3 seconds per concept
   - Use smooth transitions
   - Add pauses for complex ideas

4. **Audio Quality**:
   - Use natural voice speeds (rate: +0% to +10%)
   - Add slight pauses between sections
   - Match tone to content complexity

5. **Mathematical Accuracy**:
   - Verify all equations and formulas
   - Use proper LaTeX notation
   - Explain step-by-step transformations

## Example: Complete Workflow

```python
# 1. Create scene.py
from manim import *

class PythagoreanTheorem(Scene):
    def construct(self):
        # Title
        title = Tex(r"The Pythagorean Theorem", font_size=60)
        self.play(Write(title))
        self.wait(2)
        self.play(FadeOut(title))

        # Theorem
        theorem = MathTex(r"a^2 + b^2 = c^2", font_size=72)
        self.play(Write(theorem))
        self.wait(3)

        # Triangle
        self.play(theorem.animate.shift(UP*2).scale(0.7))
        triangle = Polygon(
            ORIGIN, RIGHT*3, RIGHT*3+UP*4,
            color=BLUE
        )
        self.play(Create(triangle))
        self.wait(3)

# 2. Generate audio
import edge_tts
import asyncio

async def generate():
    text = """
    The Pythagorean Theorem is one of the most fundamental concepts in mathematics.
    It states that in a right triangle, the square of the hypotenuse equals
    the sum of squares of the other two sides. Let's visualize this beautiful relationship.
    """
    communicate = edge_tts.Communicate(text, "en-US-AndrewNeural")
    await communicate.save("narration.mp3")

asyncio.run(generate())

# 3. Render
# manim -pqh scene.py PythagoreanTheorem

# 4. Combine
# ffmpeg -i media/videos/scene/1080p60/PythagoreanTheorem.mp4 -i narration.mp3 \
#        -c:v copy -c:a aac -shortest final_video.mp4
```

## Troubleshooting

### Manim Installation Issues
- Ensure all LaTeX packages are installed
- Try `manim checkhealth` to diagnose issues
- Use `pip install --upgrade manim` for latest version

### Audio Sync Problems
- Check audio duration: `ffprobe narration.mp3`
- Adjust Manim wait times to match audio
- Use `-shortest` flag in ffmpeg to avoid black frames

### Rendering Performance
- Use `-ql` for low quality previews
- Use `-qh` for final high-quality render
- Cache partial renders to speed up iterations

## Tips for 3Blue1Brown Style

1. **Color Scheme**: Use blue (#58C4DD), yellow (#FC6255), green (#83C167)
2. **Smooth Animations**: Use `run_time=2` for smoother transitions
3. **Camera Movement**: Use `self.camera.frame` to zoom and pan
4. **Layered Reveals**: Build complexity gradually
5. **Visual Metaphors**: Use geometric shapes to represent abstract concepts

## When to Use This Skill

Use this skill when the user wants to:
- Create educational math videos
- Visualize complex mathematical concepts
- Generate animated explanations with voiceover
- Produce 3Blue1Brown-style content
- Make professional educational content

## Error Handling

If errors occur:
1. Check all dependencies are installed
2. Verify Python version (3.8+)
3. Ensure ffmpeg is available
4. Check disk space for video rendering
5. Validate LaTeX syntax in mathematical expressions

## Resources

- Manim Documentation: https://docs.manim.community/
- 3Blue1Brown's Manim: https://github.com/3b1b/manim
- edge-tts voices: https://github.com/rany2/edge-tts
- FFmpeg guide: https://ffmpeg.org/documentation.html
