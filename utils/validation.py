from __future__ import annotations

from models import AnimationConfig


def validate_config(config: AnimationConfig) -> None:
    """Validate the most important user-editable inputs."""

    _validate_render_settings(config)
    _validate_transmission_line(config)
    _validate_numeric_values(config)


def _validate_render_settings(config: AnimationConfig) -> None:
    width, height = config.render.resolution
    if width <= 0 or height <= 0:
        raise ValueError("Render resolution must use positive width and height.")
    if config.render.fps <= 0:
        raise ValueError("Render FPS must be positive.")
    if not config.render.scene_file:
        raise ValueError("A Manim scene file must be configured.")
    if not config.render.scene_name:
        raise ValueError("A Manim scene name must be configured.")


def _validate_transmission_line(config: AnimationConfig) -> None:
    line = config.line
    if len(line.support_x_coordinates) < 2:
        raise ValueError("At least two support points are required for catenary spans.")
    if len(line.phase_y_coordinates) != 3:
        raise ValueError("The animation expects exactly three phase conductors.")
    if len(line.phase_sags) != len(line.phase_y_coordinates):
        raise ValueError("Each phase conductor must have one sag value.")
    if len(line.phase_stroke_widths) != len(line.phase_y_coordinates):
        raise ValueError("Each phase conductor must have one stroke width.")
    if line.tower_scale <= 0 or line.terminal_scale <= 0:
        raise ValueError("Transmission-line scales must be positive.")
    if line.capacitor_scale <= 0:
        raise ValueError("The series capacitor scale must be positive.")
    if config.symbols_geometry.inductor_loop_count < 2:
        raise ValueError("The inductor needs at least two visible loops.")


def _validate_numeric_values(config: AnimationConfig) -> None:
    values = (
        config.numerical.uncompensated_capacity_fraction,
        config.numerical.before_capacity_fraction,
        config.numerical.after_capacity_fraction,
    )
    for value in values:
        if not 0.0 <= value <= 1.0:
            raise ValueError("Capacity fractions must be between 0 and 1.")
