from __future__ import annotations

from collections.abc import Sequence

import numpy as np
from manim import (
    DOWN,
    LEFT,
    ORIGIN,
    PI,
    RIGHT,
    TAU,
    UL,
    UP,
    Arrow,
    Circle,
    Line,
    MathTex,
    ParametricFunction,
    Polygon,
    Rectangle,
    RoundedRectangle,
    Text,
    VGroup,
)

from calculators import catenary_point
from config import CONFIG
from models import AnimationConfig
from utils import as_point, point


def make_catenary_wire(
    start: Sequence[float],
    end: Sequence[float],
    sag: float,
    stroke_width: float,
    animation_config: AnimationConfig = CONFIG,
) -> ParametricFunction:
    """Create a sagging conductor between two support points."""

    style = animation_config.style
    line = animation_config.line
    return ParametricFunction(
        lambda alpha: catenary_point(start, end, alpha, sag, line.catenary_tension),
        t_range=[0, 1],
        color=style.line_color,
        stroke_width=stroke_width,
    )


def make_catenary_phase(
    y_coordinate: float,
    sag: float,
    stroke_width: float,
    animation_config: AnimationConfig = CONFIG,
) -> VGroup:
    """Create one conductor phase as multiple catenary spans."""

    support_xs = animation_config.line.support_x_coordinates
    spans = VGroup()
    reference_span = 4.0
    for start_x, end_x in zip(support_xs[:-1], support_xs[1:]):
        span_factor = (end_x - start_x) / reference_span
        spans.add(
            make_catenary_wire(
                point(start_x, y_coordinate),
                point(end_x, y_coordinate),
                sag=sag * span_factor,
                stroke_width=stroke_width,
                animation_config=animation_config,
            )
        )
    return spans


def make_transmission_tower(
    position: Sequence[float] = ORIGIN,
    scale: float = 1.0,
    animation_config: AnimationConfig = CONFIG,
) -> VGroup:
    """Create a stylized transmission tower from vector primitives."""

    style = animation_config.style
    x, y, _ = as_point(position)
    base_half_width = 0.55 * scale
    base_drop = 1.0 * scale
    top_rise = 0.95 * scale
    mid_half_width = 0.38 * scale
    mid_y = y - 0.05 * scale
    crossarm_half_width = 0.85 * scale
    crossarm_y = y + 0.38 * scale
    upper_arm_half_width = 0.58 * scale
    upper_arm_y = y + 0.70 * scale
    insulator_radius = 0.035 * scale
    insulator_x = 0.78 * scale
    insulator_y = y + 0.31 * scale

    base_left = point(x - base_half_width, y - base_drop)
    base_right = point(x + base_half_width, y - base_drop)
    top = point(x, y + top_rise)
    mid_left = point(x - mid_half_width, mid_y)
    mid_right = point(x + mid_half_width, mid_y)

    tower = VGroup(
        Line(base_left, top),
        Line(base_right, top),
        Line(base_left, base_right),
        Line(mid_left, mid_right),
        Line(base_left, mid_right),
        Line(base_right, mid_left),
        Line(mid_left, top),
        Line(mid_right, top),
        Line(point(x - crossarm_half_width, crossarm_y), point(x + crossarm_half_width, crossarm_y)),
        Line(point(x - upper_arm_half_width, upper_arm_y), point(x + upper_arm_half_width, upper_arm_y)),
        Circle(radius=insulator_radius).move_to(point(x - insulator_x, insulator_y)),
        Circle(radius=insulator_radius).move_to(point(x + insulator_x, insulator_y)),
    )
    tower.set_stroke(style.tower_color, width=2.2)
    tower.set_fill(opacity=0)
    return tower


def make_generator(
    position: Sequence[float] | None = None,
    scale: float = 1.0,
    animation_config: AnimationConfig = CONFIG,
) -> VGroup:
    """Create a simple generator/source icon."""

    style = animation_config.style
    text = animation_config.text
    symbols = animation_config.symbols
    if position is None:
        position = point(animation_config.line.source_x, animation_config.line.terminal_y)

    body = Circle(radius=0.45 * scale, color=style.line_color, stroke_width=3)
    sine = ParametricFunction(
        lambda t: np.array([0.55 * scale * (t / TAU - 0.5), 0.13 * scale * np.sin(t), 0]),
        t_range=[0, TAU],
        color=style.power_color,
        stroke_width=3,
    )
    label = VGroup(
        Text(text.source_label, font_size=24 * scale, color=style.text_color),
        MathTex(fr"({symbols.source_voltage})", color=style.text_color).scale(0.68 * scale),
    ).arrange(DOWN, buff=0.06).next_to(body, DOWN, buff=0.16)
    return VGroup(body, sine, label).move_to(as_point(position))


def make_substation(
    position: Sequence[float] | None = None,
    scale: float = 1.0,
    animation_config: AnimationConfig = CONFIG,
) -> VGroup:
    """Create a compact substation/load icon."""

    style = animation_config.style
    text = animation_config.text
    symbols = animation_config.symbols
    if position is None:
        position = point(animation_config.line.load_x, animation_config.line.terminal_y)

    base = Rectangle(width=0.95 * scale, height=0.65 * scale, color=style.line_color, stroke_width=3)
    roof = Polygon(
        point(-0.58 * scale, 0.33 * scale),
        point(0.0, 0.72 * scale),
        point(0.58 * scale, 0.33 * scale),
        color=style.line_color,
        stroke_width=3,
    )
    bus = Line(point(-0.33 * scale, -0.05 * scale), point(0.33 * scale, -0.05 * scale), color=style.power_color, stroke_width=3)
    label = VGroup(
        Text(text.load_label, font_size=24 * scale, color=style.text_color),
        MathTex(fr"({symbols.receiver_voltage})", color=style.text_color).scale(0.68 * scale),
    ).arrange(DOWN, buff=0.06).next_to(base, DOWN, buff=0.16)
    return VGroup(base, roof, bus, label).move_to(as_point(position))


def make_transmission_line(
    with_capacitor: bool = False,
    animation_config: AnimationConfig = CONFIG,
) -> VGroup:
    """Create a wide transmission-line diagram with optional series capacitor."""

    line_geometry = animation_config.line
    towers = VGroup(
        *[
            make_transmission_tower(
                point(tower_x, line_geometry.tower_y),
                line_geometry.tower_scale,
                animation_config,
            )
            for tower_x in line_geometry.tower_x_coordinates
        ]
    )
    phases = VGroup(
        *[
            make_catenary_phase(y_coordinate, sag, stroke_width, animation_config)
            for y_coordinate, sag, stroke_width in zip(
                line_geometry.phase_y_coordinates,
                line_geometry.phase_sags,
                line_geometry.phase_stroke_widths,
            )
        ]
    )
    source = make_generator(point(line_geometry.source_x, line_geometry.terminal_y), line_geometry.terminal_scale, animation_config)
    load = make_substation(point(line_geometry.load_x, line_geometry.terminal_y), line_geometry.terminal_scale, animation_config)
    group = VGroup(towers, phases, source, load)
    if with_capacitor:
        capacitor = make_series_capacitor(point(0.0, line_geometry.capacitor_y), line_geometry.capacitor_scale, animation_config)
        group.add(capacitor)
    return group


def make_series_capacitor(
    position: Sequence[float] = ORIGIN,
    scale: float = 1.0,
    animation_config: AnimationConfig = CONFIG,
) -> VGroup:
    """Create a clean circuit-style series capacitor symbol."""

    style = animation_config.style
    geometry = animation_config.symbols_geometry
    x, y, _ = as_point(position)
    lead_half_width = geometry.capacitor_lead_half_width * scale
    plate_half_gap = geometry.capacitor_plate_half_gap * scale
    plate_half_height = geometry.capacitor_plate_half_height * scale

    lead_left = Line(
        point(x - lead_half_width, y),
        point(x - plate_half_gap, y),
        color=style.capacitor_color,
        stroke_width=geometry.capacitor_lead_stroke_width,
    )
    lead_right = Line(
        point(x + plate_half_gap, y),
        point(x + lead_half_width, y),
        color=style.capacitor_color,
        stroke_width=geometry.capacitor_lead_stroke_width,
    )
    plate_left = Line(
        point(x - plate_half_gap, y - plate_half_height),
        point(x - plate_half_gap, y + plate_half_height),
        color=style.capacitor_color,
        stroke_width=geometry.capacitor_plate_stroke_width,
    )
    plate_right = Line(
        point(x + plate_half_gap, y - plate_half_height),
        point(x + plate_half_gap, y + plate_half_height),
        color=style.capacitor_color,
        stroke_width=geometry.capacitor_plate_stroke_width,
    )
    return VGroup(lead_left, plate_left, plate_right, lead_right)


def make_power_arrows(
    start: Sequence[float],
    end: Sequence[float],
    count: int,
    width: float,
    color: str,
) -> VGroup:
    """Create several arrows representing active power transfer."""

    arrows = VGroup()
    start_point = as_point(start)
    end_point = as_point(end)
    for index in range(count):
        alpha = (index + 0.5) / count
        x_position = start_point[0] + (end_point[0] - start_point[0]) * alpha
        y_position = start_point[1]
        arrows.add(
            Arrow(
                point(x_position - 0.34, y_position),
                point(x_position + 0.34, y_position),
                buff=0,
                color=color,
                stroke_width=width,
                max_tip_length_to_length_ratio=0.28,
            )
        )
    return arrows


def make_inductor(
    center: Sequence[float] = ORIGIN,
    scale: float = 1.0,
    label: str = "X_L",
    animation_config: AnimationConfig = CONFIG,
) -> VGroup:
    """Create an inductor with looped vertical turns."""

    style = animation_config.style
    geometry = animation_config.symbols_geometry
    x, y, _ = as_point(center)
    terminal_half_width = geometry.inductor_terminal_half_width * scale
    loop_count = geometry.inductor_loop_count
    loop_pitch = geometry.inductor_loop_pitch * scale
    loop_radius_x = geometry.inductor_loop_radius_x * scale
    loop_radius_y = geometry.inductor_loop_radius_y * scale
    coil_span = (loop_count - 0.5) * loop_pitch
    coil_base_x = x - coil_span / 2.0
    coil_start_x = coil_base_x - loop_radius_x
    coil_end_x = coil_base_x + coil_span + loop_radius_x

    lead_left = Line(point(x - terminal_half_width, y), point(coil_start_x, y), color=style.line_color, stroke_width=3)
    lead_right = Line(point(coil_end_x, y), point(x + terminal_half_width, y), color=style.line_color, stroke_width=3)
    coils = ParametricFunction(
        lambda t: np.array(
            [
                coil_base_x + loop_pitch * t / TAU + loop_radius_x * np.cos(t + PI),
                y + loop_radius_y * np.sin(t + PI),
                0,
            ]
        ),
        t_range=[0, (loop_count - 0.5) * TAU],
        color=style.reactance_color,
        stroke_width=4.0,
    )
    text = MathTex(label, color=style.reactance_color).scale(0.75 * scale).next_to(coils, UP, buff=0.18)
    return VGroup(lead_left, coils, lead_right, text)


def make_equivalent_circuit(
    with_capacitor: bool = True,
    animation_config: AnimationConfig = CONFIG,
) -> VGroup:
    """Create a one-line equivalent circuit for the transmission path."""

    style = animation_config.style
    symbols = animation_config.symbols
    geometry = animation_config.equivalent_circuit

    source = Circle(radius=geometry.terminal_radius, color=style.line_color, stroke_width=3).move_to(LEFT * abs(geometry.source_x))
    source_label = MathTex(symbols.source_voltage, color=style.text_color).scale(0.75).move_to(source)
    receiver = Circle(radius=geometry.terminal_radius, color=style.line_color, stroke_width=3).move_to(RIGHT * geometry.receiver_x)
    receiver_label = MathTex(symbols.receiver_voltage, color=style.text_color).scale(0.75).move_to(receiver)

    inductor_x = geometry.inductor_x_with_capacitor if with_capacitor else geometry.inductor_x_without_capacitor
    inductor_center = point(inductor_x, 0.0)
    inductor_scale = geometry.inductor_scale
    inductor_left = inductor_center + LEFT * (animation_config.symbols_geometry.inductor_terminal_half_width * inductor_scale)
    inductor_right = inductor_center + RIGHT * (animation_config.symbols_geometry.inductor_terminal_half_width * inductor_scale)
    left_wire = Line(source.get_right(), inductor_left, color=style.line_color, stroke_width=3)
    inductor = make_inductor(inductor_center, inductor_scale, symbols.inductive_reactance, animation_config)
    elements = VGroup(source, source_label, receiver, receiver_label, left_wire, inductor)

    if with_capacitor:
        capacitor = make_series_capacitor(point(geometry.capacitor_x, 0.0), geometry.capacitor_scale, animation_config)
        capacitor_left = RIGHT * (geometry.capacitor_x - animation_config.symbols_geometry.capacitor_lead_half_width * geometry.capacitor_scale)
        capacitor_right = RIGHT * (geometry.capacitor_x + animation_config.symbols_geometry.capacitor_lead_half_width * geometry.capacitor_scale)
        mid_wire = Line(inductor_right, capacitor_left, color=style.line_color, stroke_width=3)
        right_wire = Line(capacitor_right, receiver.get_left(), color=style.line_color, stroke_width=3)
        capacitor_label = MathTex(symbols.capacitive_reactance, color=style.capacitor_color).scale(0.75).next_to(
            capacitor[0],
            UP,
            buff=geometry.capacitor_label_buff,
        )
        elements.add(mid_wire, right_wire, capacitor, capacitor_label)
    else:
        right_wire = Line(inductor_right, receiver.get_left(), color=style.line_color, stroke_width=3)
        elements.add(right_wire)
    return elements


def make_capacity_bar(
    label: str,
    value: float,
    color: str,
    width: float,
    animation_config: AnimationConfig = CONFIG,
) -> VGroup:
    """Create a horizontal percentage bar."""

    style = animation_config.style
    geometry = animation_config.capacity_bar
    outline = RoundedRectangle(
        width=width,
        height=geometry.height,
        corner_radius=geometry.corner_radius,
        color=style.muted_text_color,
        stroke_width=geometry.stroke_width,
    )
    fill = RoundedRectangle(
        width=max(width * value, geometry.minimum_fill_width),
        height=geometry.height,
        corner_radius=geometry.corner_radius,
        color=color,
        fill_color=color,
        fill_opacity=geometry.fill_opacity,
        stroke_width=0,
    )
    fill.align_to(outline, LEFT)
    text = Text(label, font_size=geometry.label_font_size, color=style.text_color).next_to(outline, UP, buff=geometry.label_buff)
    return VGroup(text, outline, fill)


def make_comparison_panel(animation_config: AnimationConfig = CONFIG) -> VGroup:
    """Create side-by-side comparison panels for before and after compensation."""

    style = animation_config.style
    text = animation_config.text
    symbols = animation_config.symbols
    numerical = animation_config.numerical
    geometry = animation_config.comparison_panel

    before_box = RoundedRectangle(
        width=geometry.box_width,
        height=geometry.box_height,
        corner_radius=geometry.corner_radius,
        color=style.warning_color,
        fill_color=style.panel_fill_color,
        fill_opacity=0.85,
    )
    after_box = RoundedRectangle(
        width=geometry.box_width,
        height=geometry.box_height,
        corner_radius=geometry.corner_radius,
        color=style.power_color,
        fill_color=style.panel_fill_color,
        fill_opacity=0.85,
    )
    before_box.move_to(LEFT * geometry.center_offset_x)
    after_box.move_to(RIGHT * geometry.center_offset_x)

    before_title = Text(text.comparison_before_title, font_size=geometry.title_font_size, color=style.warning_color).next_to(
        before_box.get_top(),
        DOWN,
        buff=geometry.title_top_buff,
    )
    after_title = Text(text.comparison_after_title, font_size=geometry.title_font_size, color=style.power_color).next_to(
        after_box.get_top(),
        DOWN,
        buff=geometry.title_top_buff,
    )

    def reactance_text(suffix: str) -> VGroup:
        equivalent = MathTex(symbols.equivalent_reactance, color=style.text_color).scale(0.72)
        suffix_text = Text(suffix, font_size=geometry.item_font_size, color=style.text_color)
        return VGroup(equivalent, suffix_text).arrange(RIGHT, buff=0.12)

    before_items = VGroup(
        reactance_text(text.comparison_before_reactance_suffix),
        Text(text.comparison_before_power, font_size=geometry.item_font_size, color=style.text_color),
        Text(text.comparison_before_stability, font_size=geometry.item_font_size, color=style.text_color),
    ).arrange(DOWN, aligned_edge=LEFT, buff=geometry.item_vertical_buff).move_to(
        before_box.get_center() + UP * geometry.item_center_shift_y
    )
    after_items = VGroup(
        reactance_text(text.comparison_after_reactance_suffix),
        Text(text.comparison_after_power, font_size=geometry.item_font_size, color=style.text_color),
        Text(text.comparison_after_stability, font_size=geometry.item_font_size, color=style.text_color),
    ).arrange(DOWN, aligned_edge=LEFT, buff=geometry.item_vertical_buff).move_to(
        after_box.get_center() + UP * geometry.item_center_shift_y
    )

    before_bar = make_capacity_bar(
        text.capacity_label,
        numerical.before_capacity_fraction,
        style.warning_color,
        geometry.capacity_bar_width,
        animation_config,
    ).scale(geometry.capacity_bar_scale).next_to(before_box.get_bottom(), UP, buff=geometry.capacity_bar_bottom_buff)
    after_bar = make_capacity_bar(
        text.capacity_label,
        numerical.after_capacity_fraction,
        style.power_color,
        geometry.capacity_bar_width,
        animation_config,
    ).scale(geometry.capacity_bar_scale).next_to(after_box.get_bottom(), UP, buff=geometry.capacity_bar_bottom_buff)
    return VGroup(before_box, after_box, before_title, after_title, before_items, after_items, before_bar, after_bar)


def section_label(label_text: str, animation_config: AnimationConfig = CONFIG) -> Text:
    """Create a small upper-left section label."""

    style = animation_config.style
    layout = animation_config.layout
    return Text(label_text, font_size=layout.section_label_font_size, color=style.muted_text_color).to_corner(
        UL,
        buff=layout.section_label_corner_buff,
    )
