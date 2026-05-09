from __future__ import annotations

from manim import config as manim_config

from models import StyleConfig


def configure_manim_frame(style: StyleConfig) -> None:
    """Apply global Manim frame settings from the project configuration."""

    manim_config.frame_width = style.frame_width
    manim_config.frame_height = style.frame_height
    manim_config.background_color = style.background_color


def resolve_color(style: StyleConfig, color_key: str) -> str:
    """Resolve a semantic color key used by editable content."""

    colors = {
        "capacitor": style.capacitor_color,
        "line": style.line_color,
        "muted": style.muted_text_color,
        "power": style.power_color,
        "reactance": style.reactance_color,
        "text": style.text_color,
        "warning": style.warning_color,
    }
    if color_key not in colors:
        raise ValueError(f"Unknown color key: {color_key}")
    return colors[color_key]
