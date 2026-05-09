from __future__ import annotations

from dataclasses import dataclass

from models.electrical import ElectricalSymbols, NumericalParameters


@dataclass(frozen=True)
class RenderSettings:
    """Manim render settings controlled by the user."""

    manim_executable: str
    scene_file: str
    scene_name: str
    resolution: tuple[int, int]
    fps: int
    preview: bool

    @property
    def resolution_flag(self) -> str:
        """Return the Manim resolution argument in WIDTH,HEIGHT format."""

        width, height = self.resolution
        return f"{width},{height}"


@dataclass(frozen=True)
class StyleConfig:
    """Central color and frame style settings."""

    frame_width: float
    frame_height: float
    background_color: str
    line_color: str
    tower_color: str
    capacitor_color: str
    power_color: str
    warning_color: str
    text_color: str
    muted_text_color: str
    panel_fill_color: str
    reactance_color: str
    reactance_box_fill_color: str


@dataclass(frozen=True)
class TransmissionLineGeometry:
    """Editable geometry for the transmission-line diagram."""

    support_x_coordinates: tuple[float, ...]
    tower_x_coordinates: tuple[float, ...]
    tower_y: float
    tower_scale: float
    source_x: float
    load_x: float
    terminal_y: float
    terminal_scale: float
    phase_y_coordinates: tuple[float, float, float]
    phase_sags: tuple[float, float, float]
    phase_stroke_widths: tuple[float, float, float]
    catenary_tension: float
    capacitor_y: float
    capacitor_scale: float


@dataclass(frozen=True)
class CircuitSymbolGeometry:
    """Editable dimensions for electrical symbols."""

    capacitor_lead_half_width: float
    capacitor_plate_half_gap: float
    capacitor_plate_half_height: float
    capacitor_lead_stroke_width: float
    capacitor_plate_stroke_width: float
    inductor_terminal_half_width: float
    inductor_loop_count: int
    inductor_loop_pitch: float
    inductor_loop_radius_x: float
    inductor_loop_radius_y: float


@dataclass(frozen=True)
class EquivalentCircuitGeometry:
    """Layout parameters for the simplified one-line circuit."""

    source_x: float
    receiver_x: float
    terminal_radius: float
    inductor_x_with_capacitor: float
    inductor_x_without_capacitor: float
    inductor_scale: float
    capacitor_x: float
    capacitor_scale: float
    capacitor_label_buff: float


@dataclass(frozen=True)
class CapacityBarGeometry:
    """Layout parameters for percentage-style bars."""

    height: float
    corner_radius: float
    stroke_width: float
    minimum_fill_width: float
    fill_opacity: float
    label_font_size: int
    label_buff: float


@dataclass(frozen=True)
class ComparisonPanelGeometry:
    """Layout parameters for before/after comparison panels."""

    box_width: float
    box_height: float
    corner_radius: float
    center_offset_x: float
    title_font_size: int
    item_font_size: int
    item_vertical_buff: float
    title_top_buff: float
    item_center_shift_y: float
    capacity_bar_width: float
    capacity_bar_scale: float
    capacity_bar_bottom_buff: float


@dataclass(frozen=True)
class SceneLayout:
    """Scene-level positions, scales, and spacing values."""

    manim_units_per_centimeter: float
    section_label_font_size: int
    section_label_corner_buff: float
    opening_line_scale: float
    opening_line_shift_y: float
    opening_arrow_start_x: float
    opening_arrow_end_x: float
    opening_arrow_y: float
    opening_arrow_count: int
    opening_arrow_width: float
    long_line_scale: float
    long_line_shift_y: float
    long_line_statement_top_buff: float
    long_line_statement_down_shift: float
    long_line_xl_block_y: float
    long_line_xl_block_width: float
    long_line_xl_block_height: float
    long_line_xl_block_corner_radius: float
    long_line_warning_x: float
    long_line_warning_y: float
    long_line_warning_arrow_start_x: float
    long_line_warning_arrow_end_x: float
    long_line_formula_bottom_buff: float
    long_line_formula_up_shift: float
    long_line_note_buff: float
    uncompensated_title_top_buff: float
    uncompensated_title_down_shift: float
    uncompensated_circuit_shift_y: float
    uncompensated_equation_buff: float
    uncompensated_bar_buff: float
    install_title_top_buff: float
    install_title_down_shift: float
    install_line_scale: float
    install_line_shift_y: float
    install_capacitor_scale_multiplier: float
    install_capacitor_title_buff: float
    install_xc_label_buff: float
    install_xl_position: tuple[float, float]
    install_opposite_text_buff: float
    install_text_group_shift_y: float
    install_symbol_group_shift_y: float
    reactance_equation_top_buff: float
    reactance_equation_down_shift: float
    reactance_label_y: float
    reactance_before_x: float
    reactance_after_x: float
    reactance_before_bar_width: float
    reactance_after_bar_width: float
    reactance_removed_width: float
    reactance_bar_height: float
    reactance_arrow_gap: float
    reactance_xc_label_buff: float
    reactance_note_bottom_buff: float
    power_formula_top_buff: float
    power_formula_down_shift: float
    power_line_scale: float
    power_line_shift_y: float
    power_capacitor_up_shift: float
    power_weak_arrow_start_x: float
    power_weak_arrow_end_x: float
    power_strong_arrow_start_x: float
    power_strong_arrow_end_x: float
    power_arrow_y: float
    power_weak_arrow_count: int
    power_strong_arrow_count: int
    power_weak_arrow_width: float
    power_strong_arrow_width: float
    power_comparison_scale: float
    power_comparison_bottom_buff: float
    power_final_line_scale: float
    power_final_line_top_buff: float
    power_final_arrow_margin: float
    power_final_formula_y: float
    benefits_title_top_buff: float
    benefits_title_down_shift: float
    benefits_rows_center_y: float
    benefits_row_vertical_buff: float
    benefits_row_horizontal_buff: float
    benefits_icon_radius: float
    benefits_icon_font_size: int
    benefits_text_font_size: int
    closing_line_scale: float
    closing_line_shift_y: float
    closing_capacitor_up_shift: float
    closing_text_top_buff: float
    closing_arrow_start_x: float
    closing_arrow_end_x: float
    closing_arrow_y: float
    closing_arrow_count: int
    closing_arrow_width: float
    closing_formula_bottom_buff: float
    closing_formula_horizontal_buff: float
    closing_group_shift_y: float


@dataclass(frozen=True)
class TimingConfig:
    """Animation timing values."""

    very_fast: float
    fast: float
    medium: float
    slow: float
    very_slow: float
    standard_pause: float
    short_pause: float
    fade_out: float


@dataclass(frozen=True)
class BenefitItem:
    """One benefit row shown in the practical-benefits scene."""

    icon: str
    sentence: str
    color_key: str


@dataclass(frozen=True)
class TextConfig:
    """All editable user-facing text."""

    source_label: str
    load_label: str
    capacity_label: str
    opening_title: str
    opening_subtitle: str
    long_line_section: str
    long_line_statement: str
    long_line_limit_label: str
    long_line_x_suffix: str
    uncompensated_section: str
    uncompensated_title: str
    install_section: str
    install_title: str
    capacitor_bank_title: str
    opposite_reactance_text: str
    reactance_section: str
    reactance_before_title: str
    reactance_after_title: str
    reactance_note: str
    comparison_before_title: str
    comparison_after_title: str
    comparison_before_reactance_suffix: str
    comparison_after_reactance_suffix: str
    comparison_before_power: str
    comparison_before_stability: str
    comparison_after_power: str
    comparison_after_stability: str
    power_section: str
    benefits_section: str
    benefits_title: str
    benefits: tuple[BenefitItem, ...]
    closing_text: str


@dataclass(frozen=True)
class AnimationConfig:
    """Top-level configuration object for the whole project."""

    render: RenderSettings
    style: StyleConfig
    text: TextConfig
    symbols: ElectricalSymbols
    numerical: NumericalParameters
    line: TransmissionLineGeometry
    symbols_geometry: CircuitSymbolGeometry
    equivalent_circuit: EquivalentCircuitGeometry
    capacity_bar: CapacityBarGeometry
    comparison_panel: ComparisonPanelGeometry
    layout: SceneLayout
    timing: TimingConfig
