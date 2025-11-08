#!/usr/bin/env python3
"""
3Blue1Brown Style Video Generator Helper Script
Automates the process of creating educational animation videos
"""

import os
import sys
import asyncio
import argparse
from pathlib import Path


def check_dependencies():
    """Check if required dependencies are installed"""
    missing = []

    try:
        import manim
    except ImportError:
        missing.append("manim")

    try:
        import edge_tts
    except ImportError:
        missing.append("edge-tts")

    try:
        import pydub
    except ImportError:
        missing.append("pydub")

    if missing:
        print("❌ Missing dependencies:")
        for dep in missing:
            print(f"   - {dep}")
        print("\nInstall with: pip install " + " ".join(missing))
        return False

    # Check ffmpeg
    if os.system("which ffmpeg > /dev/null 2>&1") != 0:
        print("❌ ffmpeg is not installed or not in PATH")
        return False

    return True


async def generate_audio(text, output_file, voice="en-US-AndrewNeural", rate="+0%"):
    """Generate audio from text using edge-tts"""
    try:
        import edge_tts

        print(f"🎤 Generating audio with voice: {voice}")
        communicate = edge_tts.Communicate(text, voice, rate=rate)
        await communicate.save(output_file)
        print(f"✅ Audio saved to: {output_file}")
        return True
    except Exception as e:
        print(f"❌ Error generating audio: {e}")
        return False


def render_manim(scene_file, scene_class, quality="h", output_dir=None):
    """Render Manim scene"""
    try:
        quality_flags = {
            "l": "-ql",  # Low quality (480p)
            "m": "-qm",  # Medium quality (720p)
            "h": "-qh",  # High quality (1080p)
            "k": "-qk",  # 4K quality (2160p)
        }

        flag = quality_flags.get(quality, "-qh")

        print(f"🎬 Rendering Manim scene: {scene_class}")
        print(f"   Quality: {quality.upper()}")

        cmd = f"manim {flag} {scene_file} {scene_class}"
        if output_dir:
            cmd += f" --media_dir {output_dir}"

        result = os.system(cmd)

        if result == 0:
            print("✅ Manim render complete")
            return True
        else:
            print("❌ Manim render failed")
            return False
    except Exception as e:
        print(f"❌ Error rendering Manim: {e}")
        return False


def combine_audio_video(video_file, audio_file, output_file):
    """Combine video and audio using ffmpeg"""
    try:
        print("🎞️  Combining audio and video...")

        cmd = f'ffmpeg -i "{video_file}" -i "{audio_file}" -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 -shortest "{output_file}" -y'
        result = os.system(cmd)

        if result == 0:
            print(f"✅ Final video saved to: {output_file}")
            return True
        else:
            print("❌ Failed to combine audio and video")
            return False
    except Exception as e:
        print(f"❌ Error combining media: {e}")
        return False


def create_project_structure(project_name):
    """Create directory structure for a video project"""
    base_dir = Path("videos") / project_name
    base_dir.mkdir(parents=True, exist_ok=True)

    # Create subdirectories
    (base_dir / "scenes").mkdir(exist_ok=True)
    (base_dir / "audio").mkdir(exist_ok=True)
    (base_dir / "output").mkdir(exist_ok=True)

    # Create template files
    template_scene = '''from manim import *

class MainScene(Scene):
    def construct(self):
        # Title
        title = Text("Your Title Here", font_size=60)
        self.play(Write(title))
        self.wait(2)
        self.play(FadeOut(title))

        # Main content
        equation = MathTex(r"e^{i\\pi} + 1 = 0", font_size=72)
        self.play(Write(equation))
        self.wait(3)

        # Add your animations here
'''

    template_script = '''# Video Script

## Introduction (0-5s)
"Welcome! Today we're exploring an amazing mathematical concept."

## Main Content (5-20s)
"Let's start by understanding the fundamentals..."

## Conclusion (20-30s)
"And that's the beauty of mathematics. Thanks for watching!"

---

## Animation Notes:
- Scene 1: Title fade in/out
- Scene 2: Show main equation
- Scene 3: Visual proof or demonstration
'''

    scene_file = base_dir / "scenes" / "main_scene.py"
    script_file = base_dir / "script.txt"

    if not scene_file.exists():
        scene_file.write_text(template_scene)
        print(f"✅ Created scene template: {scene_file}")

    if not script_file.exists():
        script_file.write_text(template_script)
        print(f"✅ Created script template: {script_file}")

    print(f"\n📁 Project structure created in: {base_dir}")
    return base_dir


async def main():
    parser = argparse.ArgumentParser(
        description="3Blue1Brown Style Video Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create new project
  python video_generator.py --new my_video

  # Generate audio only
  python video_generator.py --audio "Your narration text" --output narration.mp3

  # Render Manim scene
  python video_generator.py --render scene.py MainScene

  # Full pipeline
  python video_generator.py --project my_video --full-pipeline

  # List available voices
  python video_generator.py --list-voices
        """
    )

    parser.add_argument("--new", metavar="PROJECT", help="Create new project structure")
    parser.add_argument("--audio", metavar="TEXT", help="Generate audio from text")
    parser.add_argument("--output", metavar="FILE", help="Output file path")
    parser.add_argument("--voice", default="en-US-AndrewNeural", help="TTS voice")
    parser.add_argument("--rate", default="+0%", help="Speech rate (e.g., +10%%, -10%%)")
    parser.add_argument("--render", metavar="FILE", help="Manim scene file to render")
    parser.add_argument("--scene", metavar="CLASS", help="Scene class name")
    parser.add_argument("--quality", choices=["l", "m", "h", "k"], default="h",
                        help="Render quality (l=480p, m=720p, h=1080p, k=4K)")
    parser.add_argument("--combine", nargs=2, metavar=("VIDEO", "AUDIO"),
                        help="Combine video and audio files")
    parser.add_argument("--list-voices", action="store_true",
                        help="List available TTS voices")
    parser.add_argument("--project", metavar="NAME",
                        help="Project name for full pipeline")
    parser.add_argument("--full-pipeline", action="store_true",
                        help="Run full pipeline (render + audio + combine)")
    parser.add_argument("--check", action="store_true",
                        help="Check if dependencies are installed")

    args = parser.parse_args()

    # Check dependencies
    if args.check or not check_dependencies():
        return

    # List voices
    if args.list_voices:
        print("🎤 Available voices (use --voice <name>):\n")
        os.system("edge-tts --list-voices | grep -E '(Name|Gender)' | head -40")
        return

    # Create new project
    if args.new:
        create_project_structure(args.new)
        return

    # Generate audio
    if args.audio:
        output = args.output or "narration.mp3"
        await generate_audio(args.audio, output, args.voice, args.rate)
        return

    # Render Manim scene
    if args.render and args.scene:
        render_manim(args.render, args.scene, args.quality)
        return

    # Combine video and audio
    if args.combine:
        video_file, audio_file = args.combine
        output = args.output or "final_video.mp4"
        combine_audio_video(video_file, audio_file, output)
        return

    # Full pipeline
    if args.full_pipeline and args.project:
        project_dir = Path("videos") / args.project

        if not project_dir.exists():
            print(f"❌ Project not found: {project_dir}")
            print(f"Create it with: python video_generator.py --new {args.project}")
            return

        print(f"🚀 Running full pipeline for: {args.project}\n")

        # Read script
        script_file = project_dir / "script.txt"
        if script_file.exists():
            script = script_file.read_text()
            print(f"📝 Script loaded from: {script_file}")
        else:
            print(f"❌ Script not found: {script_file}")
            return

        # Generate audio
        audio_file = project_dir / "audio" / "narration.mp3"
        await generate_audio(script, str(audio_file), args.voice, args.rate)

        # Render Manim
        scene_file = project_dir / "scenes" / "main_scene.py"
        if not scene_file.exists():
            print(f"❌ Scene file not found: {scene_file}")
            return

        render_manim(str(scene_file), "MainScene", args.quality)

        # Find rendered video
        video_file = None
        media_dir = Path("media/videos")
        if media_dir.exists():
            for f in media_dir.rglob("*.mp4"):
                video_file = f
                break

        if not video_file:
            print("❌ Could not find rendered video")
            return

        # Combine
        output_file = project_dir / "output" / "final_video.mp4"
        combine_audio_video(str(video_file), str(audio_file), str(output_file))

        print(f"\n🎉 Pipeline complete! Video saved to: {output_file}")
        return

    # No arguments
    parser.print_help()


if __name__ == "__main__":
    asyncio.run(main())
