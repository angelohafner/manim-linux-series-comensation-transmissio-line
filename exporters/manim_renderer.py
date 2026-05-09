from __future__ import annotations

import subprocess
from pathlib import Path

from models import AnimationConfig
from utils import validate_config


def render_scene(animation_config: AnimationConfig, project_root: Path | None = None) -> Path:
    """Render the configured Manim scene and return the expected video path."""

    validate_config(animation_config)
    root = project_root or Path(__file__).resolve().parents[1]
    command = _build_manim_command(animation_config)
    subprocess.run(command, cwd=root, check=True)
    return expected_video_path(animation_config, root)


def expected_video_path(animation_config: AnimationConfig, project_root: Path | None = None) -> Path:
    """Return Manim's conventional output path for the configured scene."""

    root = project_root or Path(__file__).resolve().parents[1]
    scene_file_stem = Path(animation_config.render.scene_file).stem
    height = animation_config.render.resolution[1]
    fps = animation_config.render.fps
    quality_folder = f"{height}p{fps}"
    return root / "media" / "videos" / scene_file_stem / quality_folder / f"{animation_config.render.scene_name}.mp4"


def _build_manim_command(animation_config: AnimationConfig) -> list[str]:
    render = animation_config.render
    executable = _resolve_manim_executable(render.manim_executable)
    command = [
        executable,
        "-r",
        render.resolution_flag,
        "--fps",
        str(render.fps),
        render.scene_file,
        render.scene_name,
    ]
    if render.preview:
        command.append("-p")
    return command


def _resolve_manim_executable(configured_executable: str) -> str:
    configured_path = Path(configured_executable)
    if configured_path.exists():
        return str(configured_path)
    return configured_executable
