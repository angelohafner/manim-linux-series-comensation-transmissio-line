from __future__ import annotations

from manim import (
    BOLD,
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Arrow,
    Circle,
    Create,
    Circumscribe,
    FadeIn,
    FadeOut,
    GrowArrow,
    GrowFromEdge,
    Indicate,
    LaggedStart,
    MathTex,
    Rectangle,
    ReplacementTransform,
    RoundedRectangle,
    Scene,
    SurroundingRectangle,
    Text,
    Transform,
    VGroup,
    Write,
)

from config import CONFIG
from models import AnimationConfig
from plotters.components import (
    make_capacity_bar,
    make_comparison_panel,
    make_equivalent_circuit,
    make_power_arrows,
    make_series_capacitor,
    make_transmission_line,
    section_label,
)
from plotters.styles import configure_manim_frame, resolve_color
from utils import point


configure_manim_frame(CONFIG.style)


class SeriesCapacitorScene(Scene):
    """Educational animation about series capacitor banks in transmission systems."""

    animation_config: AnimationConfig = CONFIG

    def construct(self) -> None:
        """Render the complete educational sequence."""

        self._set_background()
        self.opening_scene()
        self.long_line_problem_scene()
        self.uncompensated_circuit_scene()
        self.install_capacitor_scene()
        self.reactance_compensation_scene()
        self.power_transfer_scene()
        self.practical_benefits_scene()
        self.closing_scene()

    def _set_background(self) -> None:
        self.camera.background_color = self.animation_config.style.background_color

    def opening_scene(self) -> None:
        """Introduce the topic and the base transmission-line diagram."""

        cfg = self.animation_config
        style = cfg.style
        text = cfg.text
        layout = cfg.layout
        timing = cfg.timing

        title = Text(text.opening_title, font_size=52, color=style.text_color, weight=BOLD).to_edge(UP, buff=0.35)
        subtitle = Text(text.opening_subtitle, font_size=29, color=style.muted_text_color).next_to(title, DOWN, buff=0.14)
        line = make_transmission_line(False, cfg).scale(layout.opening_line_scale).shift(UP * layout.opening_line_shift_y)
        arrows = make_power_arrows(
            point(layout.opening_arrow_start_x, layout.opening_arrow_y),
            point(layout.opening_arrow_end_x, layout.opening_arrow_y),
            layout.opening_arrow_count,
            layout.opening_arrow_width,
            style.power_color,
        )

        self.play(Write(title), FadeIn(subtitle, shift=DOWN), run_time=2.2)
        self.play(Create(line), run_time=timing.very_slow)
        self.play(LaggedStart(*[GrowArrow(arrow) for arrow in arrows], lag_ratio=0.16), run_time=timing.slow)
        self.play(Indicate(arrows, color=style.power_color), run_time=1.2)
        self.wait(timing.standard_pause)
        self.play(FadeOut(VGroup(title, subtitle, line, arrows)), run_time=timing.fade_out)

    def long_line_problem_scene(self) -> None:
        """Explain the inductive-reactance limitation of long lines."""

        cfg = self.animation_config
        style = cfg.style
        text = cfg.text
        symbols = cfg.symbols
        layout = cfg.layout
        timing = cfg.timing

        label = section_label(text.long_line_section, cfg)
        line = make_transmission_line(False, cfg).scale(layout.long_line_scale).shift(UP * layout.long_line_shift_y)
        statement = Text(text.long_line_statement, font_size=32, color=style.text_color).to_edge(
            UP,
            buff=layout.long_line_statement_top_buff,
        ).shift(DOWN * layout.long_line_statement_down_shift)
        reactance_block = RoundedRectangle(
            width=layout.long_line_xl_block_width,
            height=layout.long_line_xl_block_height,
            corner_radius=layout.long_line_xl_block_corner_radius,
            color=style.reactance_color,
            fill_color=style.reactance_box_fill_color,
            fill_opacity=0.65,
        ).move_to(UP * layout.long_line_xl_block_y)
        reactance_text = MathTex(symbols.inductive_reactance, color=style.reactance_color).scale(0.95).move_to(reactance_block)
        warning = Text(text.long_line_limit_label, font_size=24, color=style.warning_color).move_to(
            point(layout.long_line_warning_x, layout.long_line_warning_y)
        )
        weak_arrow = Arrow(
            point(layout.long_line_warning_arrow_start_x, layout.long_line_warning_y),
            point(layout.long_line_warning_arrow_end_x, layout.long_line_warning_y),
            buff=0,
            color=style.warning_color,
            stroke_width=3,
        )
        formula = MathTex(
            r"P=\frac{V_s V_r}{",
            "X",
            r"}\sin(\delta)",
            color=style.text_color,
        ).scale(0.92).to_edge(DOWN, buff=layout.long_line_formula_bottom_buff).shift(UP * layout.long_line_formula_up_shift)
        formula[1].set_color(style.warning_color)
        x_box = SurroundingRectangle(formula[1], color=style.warning_color, buff=0.08)
        note = VGroup(
            MathTex("X", color=style.muted_text_color).scale(0.75),
            Text(text.long_line_x_suffix, font_size=27, color=style.muted_text_color),
        ).arrange(RIGHT, buff=0.08).next_to(formula, UP, buff=layout.long_line_note_buff)

        self.play(FadeIn(label), Create(line), run_time=1.5)
        self.play(Write(statement), run_time=timing.medium)
        self.play(
            FadeIn(reactance_block, scale=0.8),
            Write(reactance_text),
            Circumscribe(line[1], color=style.reactance_color),
            run_time=timing.slow,
        )
        self.play(GrowArrow(weak_arrow), FadeIn(warning, shift=UP), run_time=timing.medium)
        self.play(Write(formula), run_time=timing.slow)
        self.play(Create(x_box), FadeIn(note, shift=UP), run_time=timing.medium)
        self.play(Indicate(formula[1], color=style.warning_color), run_time=timing.fast)
        self.wait(timing.standard_pause)
        self.play(
            FadeOut(VGroup(label, line, statement, reactance_block, reactance_text, weak_arrow, warning, formula, x_box, note)),
            run_time=timing.fade_out,
        )

    def uncompensated_circuit_scene(self) -> None:
        """Show the equivalent circuit without compensation."""

        cfg = self.animation_config
        style = cfg.style
        text = cfg.text
        symbols = cfg.symbols
        layout = cfg.layout
        timing = cfg.timing

        label = section_label(text.uncompensated_section, cfg)
        title = Text(text.uncompensated_title, font_size=38, color=style.text_color).to_edge(
            UP,
            buff=layout.uncompensated_title_top_buff,
        ).shift(DOWN * layout.uncompensated_title_down_shift)
        circuit = make_equivalent_circuit(False, cfg).shift(UP * layout.uncompensated_circuit_shift_y)
        equation = MathTex(
            symbols.equivalent_reactance,
            "=",
            symbols.inductive_reactance,
            color=style.text_color,
        ).scale(1.1).next_to(circuit, DOWN, buff=layout.uncompensated_equation_buff)
        equation[2].set_color(style.reactance_color)
        bar = make_capacity_bar(
            text.capacity_label + " de transmiss\u00e3o",
            cfg.numerical.uncompensated_capacity_fraction,
            style.warning_color,
            4.5,
            cfg,
        ).next_to(equation, DOWN, buff=layout.uncompensated_bar_buff)

        self.play(FadeIn(label), Write(title), run_time=timing.medium)
        self.play(Create(circuit), run_time=2.2)
        self.play(Write(equation), run_time=1.2)
        self.play(FadeIn(bar[:2]), GrowFromEdge(bar[2], LEFT), run_time=1.5)
        self.play(Indicate(bar[2], color=style.warning_color), run_time=timing.fast)
        self.wait(timing.standard_pause)
        self.play(FadeOut(VGroup(label, title, circuit, equation, bar)), run_time=timing.fade_out)

    def install_capacitor_scene(self) -> None:
        """Show the insertion of the capacitor bank in series with the line."""

        cfg = self.animation_config
        style = cfg.style
        text = cfg.text
        symbols = cfg.symbols
        layout = cfg.layout
        timing = cfg.timing

        label = section_label(text.install_section, cfg)
        title = Text(text.install_title, font_size=38, color=style.text_color).to_edge(
            UP,
            buff=layout.install_title_top_buff,
        ).shift(DOWN * layout.install_title_down_shift)
        line = make_transmission_line(False, cfg).scale(layout.install_line_scale).shift(DOWN * abs(layout.install_line_shift_y))
        capacitor = make_series_capacitor(point(0.0, cfg.line.capacitor_y), cfg.line.capacitor_scale, cfg).scale(
            layout.install_capacitor_scale_multiplier
        )
        capacitor_title = Text(text.capacitor_bank_title, font_size=32, color=style.capacitor_color).next_to(
            capacitor,
            UP,
            buff=layout.install_capacitor_title_buff,
        )
        capacitive_reactance = MathTex(symbols.capacitive_reactance, color=style.capacitor_color).scale(1.1).next_to(
            capacitor,
            RIGHT,
            buff=layout.install_xc_label_buff,
        )
        inductive_reactance = MathTex(symbols.inductive_reactance, color=style.reactance_color).scale(1.0).move_to(
            point(layout.install_xl_position[0], layout.install_xl_position[1])
        )
        opposite = Text(text.opposite_reactance_text, font_size=27, color=style.muted_text_color).next_to(
            capacitive_reactance,
            DOWN,
            buff=layout.install_opposite_text_buff,
        ).shift(UP * layout.manim_units_per_centimeter)
        VGroup(capacitor_title, opposite).shift(UP * layout.install_text_group_shift_y)
        VGroup(capacitor, capacitive_reactance).shift(UP * layout.install_symbol_group_shift_y)

        self.play(FadeIn(label), Write(title), Create(line), run_time=timing.slow)
        self.play(FadeIn(capacitor, scale=0.4), Circumscribe(capacitor, color=style.capacitor_color), run_time=timing.slow)
        self.play(Write(capacitor_title), Write(capacitive_reactance), run_time=1.2)
        self.play(
            FadeIn(inductive_reactance),
            Indicate(inductive_reactance, color=style.reactance_color),
            Indicate(capacitive_reactance, color=style.capacitor_color),
            run_time=timing.medium,
        )
        self.play(FadeIn(opposite, shift=UP), run_time=timing.fast)
        self.wait(timing.standard_pause)
        self.play(
            FadeOut(VGroup(label, title, line, capacitor, capacitor_title, capacitive_reactance, inductive_reactance, opposite)),
            run_time=timing.fade_out,
        )

    def reactance_compensation_scene(self) -> None:
        """Show the equivalent reactance before and after compensation."""

        cfg = self.animation_config
        style = cfg.style
        text = cfg.text
        symbols = cfg.symbols
        layout = cfg.layout
        timing = cfg.timing

        label = section_label(text.reactance_section, cfg)
        equation = MathTex(
            symbols.equivalent_reactance,
            "=",
            symbols.inductive_reactance,
            "-",
            symbols.capacitive_reactance,
            color=style.text_color,
        ).scale(1.35).to_edge(UP, buff=layout.reactance_equation_top_buff).shift(DOWN * layout.reactance_equation_down_shift)
        equation[2].set_color(style.reactance_color)
        equation[4].set_color(style.capacitor_color)

        before_label = Text(text.reactance_before_title, font_size=30, color=style.muted_text_color).move_to(
            point(layout.reactance_before_x, layout.reactance_label_y)
        )
        after_label = Text(text.reactance_after_title, font_size=30, color=style.muted_text_color).move_to(
            point(layout.reactance_after_x, layout.reactance_label_y)
        )
        before_bar = Rectangle(
            width=layout.reactance_before_bar_width,
            height=layout.reactance_bar_height,
            color=style.reactance_color,
            fill_color=style.reactance_color,
            fill_opacity=0.65,
        ).move_to(point(layout.reactance_before_x, 0.0))
        before_text = MathTex(symbols.inductive_reactance, color=style.text_color).move_to(before_bar)
        after_bar = Rectangle(
            width=layout.reactance_after_bar_width,
            height=layout.reactance_bar_height,
            color=style.power_color,
            fill_color=style.power_color,
            fill_opacity=0.65,
        ).move_to(point(layout.reactance_after_x, 0.0))
        removed = Rectangle(
            width=layout.reactance_removed_width,
            height=layout.reactance_bar_height,
            color=style.capacitor_color,
            fill_color=style.capacitor_color,
            fill_opacity=0.55,
        ).next_to(after_bar, RIGHT, buff=0)
        after_text = MathTex(symbols.equivalent_reactance, color=style.text_color).move_to(after_bar)
        capacitive_text = MathTex(symbols.capacitive_reactance, color=style.capacitor_color).next_to(
            removed,
            UP,
            buff=layout.reactance_xc_label_buff,
        )
        arrow = Arrow(
            before_bar.get_right() + RIGHT * layout.reactance_arrow_gap,
            after_bar.get_left() + LEFT * layout.reactance_arrow_gap,
            buff=0.1,
            color=style.text_color,
        )
        note = Text(text.reactance_note, font_size=34, color=style.text_color).to_edge(DOWN, buff=layout.reactance_note_bottom_buff)

        self.play(FadeIn(label), Write(equation), run_time=1.6)
        self.play(Indicate(equation[4], color=style.capacitor_color), run_time=timing.fast)
        self.play(FadeIn(before_label), GrowFromEdge(before_bar, LEFT), Write(before_text), run_time=timing.medium)
        self.play(GrowArrow(arrow), FadeIn(after_label), run_time=timing.fast)
        self.play(
            ReplacementTransform(before_bar.copy(), after_bar),
            FadeIn(removed, shift=RIGHT),
            Write(after_text),
            Write(capacitive_text),
            run_time=1.7,
        )
        self.play(FadeOut(removed, shift=DOWN), Indicate(after_bar, color=style.power_color), Write(note), run_time=1.5)
        self.wait(timing.standard_pause)
        self.play(
            FadeOut(VGroup(label, equation, before_label, after_label, before_bar, before_text, after_bar, after_text, capacitive_text, arrow, note)),
            run_time=timing.fade_out,
        )

    def power_transfer_scene(self) -> None:
        """Connect lower equivalent reactance to higher transferable power."""

        cfg = self.animation_config
        style = cfg.style
        text = cfg.text
        symbols = cfg.symbols
        layout = cfg.layout
        timing = cfg.timing

        label = section_label(text.power_section, cfg)
        formula = MathTex(
            r"P=\frac{V_s V_r}{",
            symbols.equivalent_reactance,
            r"}\sin(\delta)",
            color=style.text_color,
        ).scale(1.15).to_edge(UP, buff=layout.power_formula_top_buff).shift(DOWN * layout.power_formula_down_shift)
        formula[1].set_color(style.power_color)

        line = make_transmission_line(True, cfg).scale(layout.power_line_scale).shift(DOWN * abs(layout.power_line_shift_y))
        line[-1].shift(UP * layout.power_capacitor_up_shift)
        weak = make_power_arrows(
            point(layout.power_weak_arrow_start_x, layout.power_arrow_y),
            point(layout.power_weak_arrow_end_x, layout.power_arrow_y),
            layout.power_weak_arrow_count,
            layout.power_weak_arrow_width,
            style.warning_color,
        )
        strong = make_power_arrows(
            point(layout.power_strong_arrow_start_x, layout.power_arrow_y),
            point(layout.power_strong_arrow_end_x, layout.power_arrow_y),
            layout.power_strong_arrow_count,
            layout.power_strong_arrow_width,
            style.power_color,
        )
        comparison = make_comparison_panel(cfg).scale(layout.power_comparison_scale).to_edge(DOWN, buff=layout.power_comparison_bottom_buff)
        final_line = line.copy().scale(layout.power_final_line_scale).to_edge(UP, buff=layout.power_final_line_top_buff)
        final_arrow_y = final_line[1][0].get_center()[1]
        final_strong = make_power_arrows(
            point(final_line[1][0].get_left()[0] + layout.power_final_arrow_margin, final_arrow_y),
            point(final_line[1][0].get_right()[0] - layout.power_final_arrow_margin, final_arrow_y),
            layout.power_strong_arrow_count,
            layout.power_strong_arrow_width,
            style.power_color,
        )

        self.play(FadeIn(label), Write(formula), run_time=1.6)
        self.play(Create(line), LaggedStart(*[GrowArrow(arrow) for arrow in weak], lag_ratio=0.12), run_time=timing.slow)
        self.play(Indicate(formula[1], color=style.power_color), run_time=timing.fast)
        self.play(ReplacementTransform(weak, strong), run_time=1.3)
        self.play(Indicate(strong, color=style.power_color), run_time=timing.fast)
        self.play(
            Transform(line, final_line),
            Transform(strong, final_strong),
            formula.animate.scale(0.82).move_to(DOWN * abs(layout.power_final_formula_y)),
            run_time=1.2,
        )
        self.play(FadeIn(comparison[0:4]), run_time=timing.fast)
        self.play(LaggedStart(*[FadeIn(item, shift=UP * 0.15) for item in comparison[4]], lag_ratio=0.2), run_time=timing.medium)
        self.play(LaggedStart(*[FadeIn(item, shift=UP * 0.15) for item in comparison[5]], lag_ratio=0.2), run_time=timing.medium)
        self.play(
            FadeIn(comparison[6][:2]),
            GrowFromEdge(comparison[6][2], LEFT),
            FadeIn(comparison[7][:2]),
            GrowFromEdge(comparison[7][2], LEFT),
            run_time=1.5,
        )
        self.wait(timing.standard_pause)
        self.play(FadeOut(VGroup(label, formula, line, strong, comparison)), run_time=timing.fade_out)

    def practical_benefits_scene(self) -> None:
        """Summarize practical engineering benefits."""

        cfg = self.animation_config
        style = cfg.style
        text = cfg.text
        layout = cfg.layout
        timing = cfg.timing

        label = section_label(text.benefits_section, cfg)
        title = Text(text.benefits_title, font_size=42, color=style.text_color).to_edge(
            UP,
            buff=layout.benefits_title_top_buff,
        ).shift(DOWN * layout.benefits_title_down_shift)
        rows = VGroup()
        for item in text.benefits:
            color = resolve_color(style, item.color_key)
            icon_circle = Circle(radius=layout.benefits_icon_radius, color=color, fill_color=color, fill_opacity=0.18, stroke_width=3)
            icon = Text(item.icon, font_size=layout.benefits_icon_font_size, color=color, weight=BOLD).move_to(icon_circle)
            sentence = Text(item.sentence, font_size=layout.benefits_text_font_size, color=style.text_color)
            row = VGroup(icon_circle, icon, sentence).arrange(RIGHT, buff=layout.benefits_row_horizontal_buff)
            rows.add(row)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=layout.benefits_row_vertical_buff).move_to(DOWN * abs(layout.benefits_rows_center_y))

        self.play(FadeIn(label), Write(title), run_time=timing.medium)
        for row in rows:
            self.play(FadeIn(row[0], scale=0.7), Write(row[1]), FadeIn(row[2], shift=RIGHT * 0.25), run_time=0.9)
            self.play(Indicate(row[0], color=row[0].get_color()), run_time=timing.very_fast)
        self.wait(timing.short_pause)
        self.play(FadeOut(VGroup(label, title, rows)), run_time=timing.fade_out)

    def closing_scene(self) -> None:
        """Close the animation with the main engineering takeaway."""

        cfg = self.animation_config
        style = cfg.style
        text = cfg.text
        symbols = cfg.symbols
        layout = cfg.layout
        timing = cfg.timing

        line = make_transmission_line(True, cfg).scale(layout.closing_line_scale).shift(DOWN * abs(layout.closing_line_shift_y))
        line[-1].shift(UP * layout.closing_capacitor_up_shift)
        final_text = Text(text.closing_text, font_size=34, color=style.text_color, line_spacing=0.95).to_edge(
            UP,
            buff=layout.closing_text_top_buff,
        )
        glow = make_power_arrows(
            point(layout.closing_arrow_start_x, layout.closing_arrow_y),
            point(layout.closing_arrow_end_x, layout.closing_arrow_y),
            layout.closing_arrow_count,
            layout.closing_arrow_width,
            style.power_color,
        )
        equivalent_formula = MathTex(
            f"{symbols.equivalent_reactance}={symbols.inductive_reactance}-{symbols.capacitive_reactance}",
            color=style.capacitor_color,
        ).scale(1.0)
        implication = MathTex(r"\Rightarrow", color=style.text_color).scale(1.0)
        maximum_power = MathTex(fr"{symbols.maximum_power}\uparrow", color=style.power_color).scale(1.0)
        formula = VGroup(equivalent_formula, implication, maximum_power).arrange(
            RIGHT,
            buff=layout.closing_formula_horizontal_buff,
        ).to_edge(DOWN, buff=layout.closing_formula_bottom_buff)
        VGroup(line, glow, formula).shift(UP * layout.closing_group_shift_y)

        self.play(Create(line), Write(final_text), run_time=2.2)
        self.play(LaggedStart(*[GrowArrow(arrow) for arrow in glow], lag_ratio=0.12), Write(formula), run_time=2.2)
        self.play(Circumscribe(line[-1][0], color=style.capacitor_color), Indicate(maximum_power, color=style.power_color), run_time=1.5)
        self.wait(timing.standard_pause)
        self.play(FadeOut(VGroup(line, final_text, glow, formula)), run_time=1.5)


class FirstSlideScene(SeriesCapacitorScene):
    """Render only the opening slide."""

    def construct(self) -> None:
        self._set_background()
        self.opening_scene()


class FirstTwoSlidesScene(SeriesCapacitorScene):
    """Render only the first two slides."""

    def construct(self) -> None:
        self._set_background()
        self.opening_scene()
        self.long_line_problem_scene()


class FirstThreeSlidesScene(SeriesCapacitorScene):
    """Render only the first three slides."""

    def construct(self) -> None:
        self._set_background()
        self.opening_scene()
        self.long_line_problem_scene()
        self.uncompensated_circuit_scene()


class FirstFourSlidesScene(SeriesCapacitorScene):
    """Render only the first four slides."""

    def construct(self) -> None:
        self._set_background()
        self.opening_scene()
        self.long_line_problem_scene()
        self.uncompensated_circuit_scene()
        self.install_capacitor_scene()
