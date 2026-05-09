from __future__ import annotations

import argparse
from dataclasses import replace
from pathlib import Path

from config import CONFIG
from exporters import render_scene
from models import AnimationConfig


def main() -> int:
    """Coordinate configuration, optional CLI overrides, and Manim rendering."""

    args = _parse_arguments()
    animation_config = _apply_cli_overrides(CONFIG, args)
    output_path = render_scene(animation_config, Path(__file__).resolve().parent)
    print(f"Rendered video: {output_path}")
    return 0


def _parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render the series-compensation Manim animation.")
    parser.add_argument("--scene", default=None, help="Manim scene class to render.")
    parser.add_argument("--resolution", default=None, help="Render resolution as WIDTH,HEIGHT. Example: 1920,1080.")
    parser.add_argument("--fps", type=int, default=None, help="Frames per second.")
    parser.add_argument("--preview", action="store_true", help="Open the video after rendering.")
    return parser.parse_args()


def _apply_cli_overrides(config: AnimationConfig, args: argparse.Namespace) -> AnimationConfig:
    render = config.render
    if args.scene is not None:
        render = replace(render, scene_name=args.scene)
    if args.resolution is not None:
        render = replace(render, resolution=_parse_resolution(args.resolution))
    if args.fps is not None:
        render = replace(render, fps=args.fps)
    if args.preview:
        render = replace(render, preview=True)
    return replace(config, render=render)


def _parse_resolution(value: str) -> tuple[int, int]:
    try:
        width_text, height_text = value.split(",", maxsplit=1)
        return int(width_text), int(height_text)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("Resolution must use WIDTH,HEIGHT format.") from exc


if __name__ == "__main__":
    raise SystemExit(main())
