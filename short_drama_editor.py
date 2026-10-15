#!/usr/bin/env python3
"""Minimal rule-based short-drama editor."""
from __future__ import annotations
import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

VIDEO_EXTENSIONS = {".mp4", ".mov", ".m4v", ".avi", ".mkv", ".webm"}

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Create a simple short-drama montage.")
    parser.add_argument("input_dir", type=Path, help="Directory containing source videos")
    parser.add_argument("-o", "--output", type=Path, default=Path("output.mp4"))
    parser.add_argument("--seconds", type=float, default=5.0,
                        help="Maximum seconds to take from each source (default: 5)")
    parser.add_argument("--keep-audio", action="store_true",
                        help="Keep source audio when possible")
    return parser

def run_ffmpeg(args: list[str]) -> None:
    result = subprocess.run(args, text=True, capture_output=True)
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or "ffmpeg failed")

def edit(input_dir: Path, output: Path, seconds: float, keep_audio: bool) -> int:
    if shutil.which("ffmpeg") is None:
        raise RuntimeError("ffmpeg was not found. Install it and ensure it is on PATH.")
    if not input_dir.is_dir():
        raise ValueError(f"Input directory does not exist: {input_dir}")
    if seconds <= 0:
        raise ValueError("--seconds must be greater than 0")
    sources = sorted(p for p in input_dir.iterdir()
                     if p.is_file() and p.suffix.lower() in VIDEO_EXTENSIONS)
    if not sources:
        raise ValueError(f"No supported videos found in {input_dir}")
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="short-drama-editor-") as temp_dir:
        temp = Path(temp_dir)
        clips = []
        for index, source in enumerate(sources):
            clip = temp / f"clip-{index:04d}.mp4"
            command = ["ffmpeg", "-y", "-i", str(source), "-t", str(seconds),
                       "-vf", "scale=trunc(iw/2)*2:trunc(ih/2)*2,fps=30",
                       "-c:v", "libx264", "-preset", "veryfast", "-pix_fmt", "yuv420p"]
            command += ["-c:a", "aac", "-shortest"] if keep_audio else ["-an"]
            run_ffmpeg(command + [str(clip)])
            clips.append(clip)
        concat_file = temp / "concat.txt"
        concat_file.write_text("".join(f"file '{p.as_posix()}'\n" for p in clips), encoding="utf-8")
        run_ffmpeg(["ffmpeg", "-y", "-f", "concat", "-safe", "0",
                    "-i", str(concat_file), "-c", "copy", str(output)])
    return len(sources)

def main() -> int:
    args = build_parser().parse_args()
    try:
        count = edit(args.input_dir, args.output, args.seconds, args.keep_audio)
    except (RuntimeError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    print(f"Created {args.output} from {count} clip(s).")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
