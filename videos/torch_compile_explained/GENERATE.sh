#!/bin/bash
# Quick generation script for torch.compile video

set -e  # Exit on error

echo "🎬 torch.compile Video Generator"
echo "================================"
echo ""

# Check if we're in the right directory
if [ ! -f "script.txt" ]; then
    echo "❌ Error: Please run this from the torch_compile_explained directory"
    exit 1
fi

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check dependencies
echo "📋 Checking dependencies..."
MISSING=0

if ! command_exists python3; then
    echo "❌ python3 not found"
    MISSING=1
fi

if ! command_exists ffmpeg; then
    echo "❌ ffmpeg not found"
    MISSING=1
fi

if ! python3 -c "import manim" 2>/dev/null; then
    echo "❌ manim not installed (pip install manim)"
    MISSING=1
fi

if ! python3 -c "import edge_tts" 2>/dev/null; then
    echo "❌ edge-tts not installed (pip install edge-tts)"
    MISSING=1
fi

if [ $MISSING -eq 1 ]; then
    echo ""
    echo "Please install missing dependencies:"
    echo "  sudo apt-get install -y python3-pip ffmpeg libcairo2-dev libpango1.0-dev texlive-full"
    echo "  pip install manim edge-tts pydub"
    echo ""
    echo "See README.md for detailed installation instructions."
    exit 1
fi

echo "✅ All dependencies found"
echo ""

# Parse command line arguments
QUALITY="h"  # Default to high quality (1080p)
VOICE="en-US-AndrewNeural"

while [[ $# -gt 0 ]]; do
    case $1 in
        -q|--quality)
            QUALITY="$2"
            shift 2
            ;;
        -v|--voice)
            VOICE="$2"
            shift 2
            ;;
        -h|--help)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  -q, --quality QUALITY   Render quality: l(480p), m(720p), h(1080p), k(4K)"
            echo "                          Default: h"
            echo "  -v, --voice VOICE       TTS voice name"
            echo "                          Default: en-US-AndrewNeural"
            echo "  -h, --help             Show this help message"
            echo ""
            echo "Examples:"
            echo "  $0                      # Generate with defaults (1080p, US male voice)"
            echo "  $0 -q k                 # Generate in 4K"
            echo "  $0 -v en-GB-SoniaNeural # Use British female voice"
            echo "  $0 -q m -v en-US-AriaNeural  # 720p with US female voice"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use -h or --help for usage information"
            exit 1
            ;;
    esac
done

# Map quality to description
case $QUALITY in
    l) QUALITY_DESC="480p (Low - Fast preview)" ;;
    m) QUALITY_DESC="720p (Medium)" ;;
    h) QUALITY_DESC="1080p (High)" ;;
    k) QUALITY_DESC="4K (Ultra - Slow)" ;;
    *) echo "Invalid quality: $QUALITY"; exit 1 ;;
esac

echo "⚙️  Configuration:"
echo "   Quality: $QUALITY_DESC"
echo "   Voice: $VOICE"
echo ""

# Create directories
mkdir -p audio output

# Step 1: Generate audio
echo "🎤 Step 1/3: Generating audio narration..."
python3 - <<EOF
import asyncio
import edge_tts
import sys

async def generate_audio():
    try:
        with open('script.txt', 'r') as f:
            text = f.read()

        # Remove section headers and timing comments
        lines = []
        for line in text.split('\n'):
            if not line.startswith('#') and line.strip():
                lines.append(line)
        text = '\n'.join(lines)

        print(f"   Generating {len(text)} characters of narration...")
        communicate = edge_tts.Communicate(text, "$VOICE")
        await communicate.save("audio/narration.mp3")
        print("   ✅ Audio saved to audio/narration.mp3")
        return True
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

success = asyncio.run(generate_audio())
sys.exit(0 if success else 1)
EOF

if [ $? -ne 0 ]; then
    echo "❌ Audio generation failed"
    exit 1
fi

# Check audio duration
DURATION=$(ffprobe -i audio/narration.mp3 -show_entries format=duration -v quiet -of csv="p=0")
echo "   Audio duration: ${DURATION}s (expected ~300s)"
echo ""

# Step 2: Render Manim animation
echo "🎨 Step 2/3: Rendering Manim animation (this may take 5-15 minutes)..."

# Map quality to manim flag
case $QUALITY in
    l) MANIM_FLAG="-ql" ;;
    m) MANIM_FLAG="-qm" ;;
    h) MANIM_FLAG="-qh" ;;
    k) MANIM_FLAG="-qk" ;;
esac

manim $MANIM_FLAG scenes/main_scene.py TorchCompileExplained

if [ $? -ne 0 ]; then
    echo "❌ Manim rendering failed"
    exit 1
fi

echo "✅ Animation rendered"
echo ""

# Step 3: Find rendered video and combine with audio
echo "🎞️  Step 3/3: Combining audio and video..."

# Find the rendered video (Manim outputs to different paths based on quality)
VIDEO_PATH=""
for dir in media/videos/main_scene/*/; do
    if [ -f "${dir}TorchCompileExplained.mp4" ]; then
        VIDEO_PATH="${dir}TorchCompileExplained.mp4"
        break
    fi
done

if [ -z "$VIDEO_PATH" ]; then
    echo "❌ Could not find rendered video in media/ directory"
    exit 1
fi

echo "   Found video: $VIDEO_PATH"

# Combine video and audio
ffmpeg -y \
    -i "$VIDEO_PATH" \
    -i audio/narration.mp3 \
    -c:v copy \
    -c:a aac \
    -shortest \
    output/final_video.mp4 \
    -loglevel warning

if [ $? -ne 0 ]; then
    echo "❌ Video combination failed"
    exit 1
fi

echo "✅ Video combined successfully"
echo ""

# Get final video info
VIDEO_SIZE=$(du -h output/final_video.mp4 | cut -f1)
VIDEO_DURATION=$(ffprobe -i output/final_video.mp4 -show_entries format=duration -v quiet -of csv="p=0")

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎉 Video generated successfully!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📹 Output: output/final_video.mp4"
echo "📊 Size: $VIDEO_SIZE"
echo "⏱️  Duration: ${VIDEO_DURATION}s"
echo "🎨 Quality: $QUALITY_DESC"
echo "🎤 Voice: $VOICE"
echo ""
echo "To watch your video:"
echo "  xdg-open output/final_video.mp4"
echo ""
echo "Or copy it to your desired location:"
echo "  cp output/final_video.mp4 ~/torch_compile_tutorial.mp4"
echo ""
