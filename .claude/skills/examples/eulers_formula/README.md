# Euler's Formula Video Example

This example demonstrates how to create a 3Blue1Brown-style video explaining Euler's formula: e^(iπ) + 1 = 0

## What's Included

- `scenes/main_scene.py` - Complete Manim animation code
- `script.txt` - Voice narration script with timing
- `README.md` - This file

## Quick Start

From the `.claude/skills` directory:

```bash
# Make sure you're in the skills directory
cd .claude/skills

# Generate the video using the helper script
python helpers/video_generator.py --new eulers_formula_test

# Copy the example files
cp examples/eulers_formula/scenes/main_scene.py ../../../videos/eulers_formula_test/scenes/
cp examples/eulers_formula/script.txt ../../../videos/eulers_formula_test/

# Run the full pipeline
python helpers/video_generator.py --project eulers_formula_test --full-pipeline
```

Or manually:

```bash
# 1. Generate audio
python -c "
import asyncio
import edge_tts

async def gen():
    with open('script.txt', 'r') as f:
        text = f.read()
    communicate = edge_tts.Communicate(text, 'en-US-AndrewNeural')
    await communicate.save('narration.mp3')

asyncio.run(gen())
"

# 2. Render animation (high quality 1080p)
manim -qh scenes/main_scene.py EulersFormula

# 3. Combine (adjust paths as needed)
ffmpeg -i media/videos/main_scene/1080p60/EulersFormula.mp4 -i narration.mp3 \
       -c:v copy -c:a aac -shortest final_eulers_formula.mp4
```

## The Animation

### Key Scenes

1. **Title (0-4s)**: Animated title with subtitle
2. **Formula Introduction (4-10s)**: The famous equation appears
3. **Complex Plane (11-16s)**: Setting up the coordinate system
4. **Unit Circle (16-20s)**: Drawing the circle
5. **The Journey (20-30s)**: Animating e^(iθ) as θ goes from 0 to π
6. **The Magic (30-35s)**: Showing how -1 + 1 = 0
7. **Final Emphasis (35-40s)**: Concluding with the complete formula

### 3Blue1Brown Style Elements

- **Color Scheme**:
  - Blue (#58C4DD) for mathematical objects
  - Yellow (#FC6255) for emphasis
  - Green (#83C167) for moving points

- **Smooth Animations**: Uses `run_time` and `rate_func` for fluid motion

- **Visual Clarity**: Large font sizes, clear labels, smooth transitions

- **Mathematical Depth**: Shows both the visual and algebraic aspects

## Customization Ideas

### Change the Duration
Adjust `self.wait()` times in the scene to make it longer or shorter.

### Add More Detail
The `EulersFormulaExplanation` class in the scene file shows an alternative approach with more algebraic steps.

### Different Voice
Change the voice in the generation command:
```bash
python helpers/video_generator.py \
    --project eulers_formula \
    --full-pipeline \
    --voice en-GB-SoniaNeural  # British female voice
```

### Higher Quality
Render in 4K:
```bash
python helpers/video_generator.py \
    --project eulers_formula \
    --full-pipeline \
    --quality k
```

## Learning Points

This example demonstrates:

1. **Complex animation sequencing** - Multiple coordinated animations
2. **Mathematical visualization** - Complex plane, unit circle
3. **Color coordination** - Using 3Blue1Brown's color scheme
4. **Timing synchronization** - Matching visuals to narration
5. **Camera positioning** - Scaling and moving elements
6. **Path tracing** - Showing motion trails
7. **Value trackers** - Animating parametric motion

## Extending This Example

Try adding:
- More points on the unit circle (e^(i·π/2), e^(i·π/4), etc.)
- The relationship to sine and cosine (e^(iθ) = cos(θ) + i·sin(θ))
- Animation of the exponential series
- Historical context about Euler
- Other applications of the formula

## Resources

- Understanding e^(ix): https://www.youtube.com/watch?v=v0YEaeIClKY (3Blue1Brown)
- Manim Complex Plane docs: https://docs.manim.community/en/stable/reference/manim.mobject.graphing.coordinate_systems.ComplexPlane.html
- Euler's formula: https://en.wikipedia.org/wiki/Euler%27s_formula

## Output

After running the full pipeline, you'll get:
- `audio/narration.mp3` - Generated voice narration
- `output/final_video.mp4` - Complete video with audio
- Plus Manim's intermediate files in `media/`

Enjoy creating beautiful mathematical animations! 🎨📐
