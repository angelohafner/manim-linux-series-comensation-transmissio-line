from manim import *

# Render hint:
# manim -pqh banco_capacitor_serie.py BancoCapacitorSerieScene

config.frame_width = 16
config.frame_height = 9
config.pixel_width = 1920
config.pixel_height = 1080
config.background_color = "#0B1020"

LINE_COLOR = "#8FD3FF"
TOWER_COLOR = "#C9D6E3"
CAP_COLOR = "#FFB000"
POWER_COLOR = "#32E875"
WARNING_COLOR = "#FF5C5C"
TEXT_COLOR = "#F4F7FB"
MUTED_TEXT = "#9FB3C8"
PANEL_FILL = "#111A2E"
BLUE_REACTANCE = "#47A8FF"


def make_transmission_tower(position=ORIGIN, scale=1.0):
    """Create a stylized transmission tower from vector primitives."""
    x, y, _ = position
    base_left = np.array([x - 0.55 * scale, y - 1.0 * scale, 0])
    base_right = np.array([x + 0.55 * scale, y - 1.0 * scale, 0])
    top = np.array([x, y + 0.95 * scale, 0])
    mid_left = np.array([x - 0.38 * scale, y - 0.05 * scale, 0])
    mid_right = np.array([x + 0.38 * scale, y - 0.05 * scale, 0])
    tower = VGroup(
        Line(base_left, top),
        Line(base_right, top),
        Line(base_left, base_right),
        Line(mid_left, mid_right),
        Line(base_left, mid_right),
        Line(base_right, mid_left),
        Line(mid_left, top),
        Line(mid_right, top),
        Line([x - 0.85 * scale, y + 0.38 * scale, 0], [x + 0.85 * scale, y + 0.38 * scale, 0]),
        Line([x - 0.58 * scale, y + 0.7 * scale, 0], [x + 0.58 * scale, y + 0.7 * scale, 0]),
        Circle(radius=0.035 * scale).move_to([x - 0.78 * scale, y + 0.31 * scale, 0]),
        Circle(radius=0.035 * scale).move_to([x + 0.78 * scale, y + 0.31 * scale, 0]),
    )
    tower.set_stroke(TOWER_COLOR, width=2.2)
    tower.set_fill(opacity=0)
    return tower


def make_generator(position=LEFT * 6.4 + DOWN * 1.15, scale=1.0):
    """Create a simple generator/source icon."""
    body = Circle(radius=0.45 * scale, color=LINE_COLOR, stroke_width=3)
    sine = ParametricFunction(
        lambda t: np.array([0.55 * scale * (t / TAU - 0.5), 0.13 * scale * np.sin(t), 0]),
        t_range=[0, TAU],
        color=POWER_COLOR,
        stroke_width=3,
    )
    label = Text("Fonte", font_size=24 * scale, color=TEXT_COLOR).next_to(body, DOWN, buff=0.18)
    group = VGroup(body, sine, label).move_to(position)
    return group


def make_substation(position=RIGHT * 6.4 + DOWN * 1.15, scale=1.0):
    """Create a compact substation/load icon."""
    base = Rectangle(width=0.95 * scale, height=0.65 * scale, color=LINE_COLOR, stroke_width=3)
    roof = Polygon(
        [-0.58 * scale, 0.33 * scale, 0],
        [0, 0.72 * scale, 0],
        [0.58 * scale, 0.33 * scale, 0],
        color=LINE_COLOR,
        stroke_width=3,
    )
    bus = Line([-0.33 * scale, -0.05 * scale, 0], [0.33 * scale, -0.05 * scale, 0], color=POWER_COLOR, stroke_width=3)
    label = Text("Carga", font_size=24 * scale, color=TEXT_COLOR).next_to(base, DOWN, buff=0.18)
    group = VGroup(base, roof, bus, label).move_to(position)
    return group


def make_transmission_line(with_capacitor=False):
    """Create a wide transmission-line diagram with towers and optional series capacitor."""
    y = -1.05
    towers = VGroup(
        make_transmission_tower(LEFT * 4.0 + DOWN * 1.2, 0.9),
        make_transmission_tower(ORIGIN + DOWN * 1.2, 0.9),
        make_transmission_tower(RIGHT * 4.0 + DOWN * 1.2, 0.9),
    )
    top_wire = Line(LEFT * 6 + UP * 0.05, RIGHT * 6 + UP * 0.05, color=LINE_COLOR, stroke_width=4)
    mid_wire = Line(LEFT * 6 + DOWN * 0.25, RIGHT * 6 + DOWN * 0.25, color=LINE_COLOR, stroke_width=3)
    low_wire = Line(LEFT * 6 + DOWN * 0.55, RIGHT * 6 + DOWN * 0.55, color=LINE_COLOR, stroke_width=3)
    line = VGroup(top_wire, mid_wire, low_wire).shift(DOWN * 0.6)
    source = make_generator(LEFT * 6.75 + DOWN * 1.15, 0.9)
    load = make_substation(RIGHT * 6.75 + DOWN * 1.15, 0.9)
    group = VGroup(towers, line, source, load)
    if with_capacitor:
        cap = make_series_capacitor(DOWN * 0.55, 0.85)
        group.add(cap)
    return group


def make_series_capacitor(position=ORIGIN, scale=1.0):
    """Create a series capacitor bank symbol with a highlighted enclosure."""
    x, y, _ = position
    lead_l = Line([x - 0.85 * scale, y, 0], [x - 0.28 * scale, y, 0], color=LINE_COLOR, stroke_width=4)
    lead_r = Line([x + 0.28 * scale, y, 0], [x + 0.85 * scale, y, 0], color=LINE_COLOR, stroke_width=4)
    plate_l = Line([x - 0.15 * scale, y - 0.32 * scale, 0], [x - 0.15 * scale, y + 0.32 * scale, 0], color=CAP_COLOR, stroke_width=5)
    plate_r = Line([x + 0.15 * scale, y - 0.32 * scale, 0], [x + 0.15 * scale, y + 0.32 * scale, 0], color=CAP_COLOR, stroke_width=5)
    box = RoundedRectangle(
        width=1.9 * scale,
        height=1.0 * scale,
        corner_radius=0.12 * scale,
        color=CAP_COLOR,
        stroke_width=2.5,
        fill_color="#2C2100",
        fill_opacity=0.25,
    ).move_to(position)
    label = Text("Banco série", font_size=22 * scale, color=CAP_COLOR).next_to(box, DOWN, buff=0.12)
    return VGroup(box, lead_l, lead_r, plate_l, plate_r, label)


def make_power_arrows(start=LEFT * 5, end=RIGHT * 5, count=5, width=3, color=POWER_COLOR):
    """Create several arrows representing active power transfer."""
    arrows = VGroup()
    start_x = start[0]
    end_x = end[0]
    y = start[1]
    for i in range(count):
        alpha = (i + 0.5) / count
        x = interpolate(start_x, end_x, alpha)
        arrows.add(
            Arrow(
                [x - 0.34, y, 0],
                [x + 0.34, y, 0],
                buff=0,
                color=color,
                stroke_width=width,
                max_tip_length_to_length_ratio=0.28,
            )
        )
    return arrows


def make_inductor(center=ORIGIN, scale=1.0, label="X_L"):
    """Create a simplified inductor/reactance symbol."""
    x, y, _ = center
    lead_l = Line([x - 1.2 * scale, y, 0], [x - 0.55 * scale, y, 0], color=LINE_COLOR, stroke_width=3)
    lead_r = Line([x + 0.55 * scale, y, 0], [x + 1.2 * scale, y, 0], color=LINE_COLOR, stroke_width=3)
    coils = VGroup()
    for k in range(4):
        arc = Arc(
            radius=0.18 * scale,
            start_angle=PI,
            angle=-PI,
            color=BLUE_REACTANCE,
            stroke_width=3,
        ).move_to([x - 0.36 * scale + k * 0.24 * scale, y, 0])
        coils.add(arc)
    text = MathTex(label, color=BLUE_REACTANCE).scale(0.75 * scale).next_to(coils, UP, buff=0.18)
    return VGroup(lead_l, coils, lead_r, text)


def make_equivalent_circuit(with_capacitor=True):
    """Create a one-line equivalent circuit for the transmission path."""
    src = Circle(radius=0.42, color=LINE_COLOR, stroke_width=3).move_to(LEFT * 5.2)
    src_label = MathTex("V_s", color=TEXT_COLOR).scale(0.75).move_to(src)
    recv = Circle(radius=0.42, color=LINE_COLOR, stroke_width=3).move_to(RIGHT * 5.2)
    recv_label = MathTex("V_r", color=TEXT_COLOR).scale(0.75).move_to(recv)
    left_wire = Line(src.get_right(), LEFT * 2.6, color=LINE_COLOR, stroke_width=3)
    right_start = RIGHT * 2.25 if with_capacitor else RIGHT * 1.25
    right_wire = Line(right_start, recv.get_left(), color=LINE_COLOR, stroke_width=3)
    inductor = make_inductor(LEFT * 1.75 if with_capacitor else ORIGIN, 0.9, "X_L")
    elements = VGroup(src, src_label, recv, recv_label, left_wire, right_wire, inductor)
    if with_capacitor:
        cap = make_series_capacitor(RIGHT * 1.45, 0.65)
        mid_wire = Line(LEFT * 0.64, RIGHT * 0.9, color=LINE_COLOR, stroke_width=3)
        cap_label = MathTex("X_C", color=CAP_COLOR).scale(0.75).next_to(cap[0], UP, buff=0.15)
        elements.add(mid_wire, cap, cap_label)
    return elements


def make_capacity_bar(label="Capacidade", value=0.45, color=POWER_COLOR, width=3.4):
    """Create a horizontal percentage bar."""
    outline = RoundedRectangle(width=width, height=0.34, corner_radius=0.08, color=MUTED_TEXT, stroke_width=2)
    fill = RoundedRectangle(
        width=max(width * value, 0.05),
        height=0.34,
        corner_radius=0.08,
        color=color,
        fill_color=color,
        fill_opacity=0.75,
        stroke_width=0,
    )
    fill.align_to(outline, LEFT)
    text = Text(label, font_size=24, color=TEXT_COLOR).next_to(outline, UP, buff=0.14)
    return VGroup(text, outline, fill)


def make_comparison_panel():
    """Create side-by-side comparison panels for before and after compensation."""
    before_box = RoundedRectangle(width=5.8, height=3.7, corner_radius=0.18, color=WARNING_COLOR, fill_color=PANEL_FILL, fill_opacity=0.85)
    after_box = RoundedRectangle(width=5.8, height=3.7, corner_radius=0.18, color=POWER_COLOR, fill_color=PANEL_FILL, fill_opacity=0.85)
    before_box.move_to(LEFT * 3.25)
    after_box.move_to(RIGHT * 3.25)

    before_title = Text("Antes", font_size=32, color=WARNING_COLOR).next_to(before_box.get_top(), DOWN, buff=0.25)
    after_title = Text("Depois", font_size=32, color=POWER_COLOR).next_to(after_box.get_top(), DOWN, buff=0.25)

    before_items = VGroup(
        Text("X_eq alto", font_size=25, color=TEXT_COLOR),
        Text("Potência limitada", font_size=25, color=TEXT_COLOR),
        Text("Menor margem de estabilidade", font_size=25, color=TEXT_COLOR),
    ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).move_to(before_box.get_center() + UP * 0.25)
    after_items = VGroup(
        Text("X_eq menor", font_size=25, color=TEXT_COLOR),
        Text("Maior transferência de potência", font_size=25, color=TEXT_COLOR),
        Text("Melhor estabilidade", font_size=25, color=TEXT_COLOR),
    ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).move_to(after_box.get_center() + UP * 0.25)

    before_bar = make_capacity_bar("Capacidade", 0.42, WARNING_COLOR, 3.6).scale(0.8).next_to(before_box.get_bottom(), UP, buff=0.35)
    after_bar = make_capacity_bar("Capacidade", 0.82, POWER_COLOR, 3.6).scale(0.8).next_to(after_box.get_bottom(), UP, buff=0.35)
    return VGroup(before_box, after_box, before_title, after_title, before_items, after_items, before_bar, after_bar)


def section_label(text):
    """Create a small upper-left section label."""
    return Text(text, font_size=26, color=MUTED_TEXT).to_corner(UL, buff=0.35)


class BancoCapacitorSerieScene(Scene):
    """Educational animation about series capacitor banks in transmission systems."""

    def construct(self):
        self.camera.background_color = "#0B1020"
        self.opening_scene()
        self.long_line_problem_scene()
        self.uncompensated_circuit_scene()
        self.install_capacitor_scene()
        self.reactance_compensation_scene()
        self.power_transfer_scene()
        self.practical_benefits_scene()
        self.closing_scene()

    def opening_scene(self):
        title = Text("Banco de Capacitor Série", font_size=56, color=TEXT_COLOR, weight=BOLD).to_edge(UP, buff=0.45)
        subtitle = Text("Como ele aumenta a capacidade de transmissão?", font_size=32, color=MUTED_TEXT).next_to(title, DOWN, buff=0.18)
        line = make_transmission_line(False).scale(0.86).shift(DOWN * 0.35)
        arrows = make_power_arrows(LEFT * 4.5 + DOWN * 1.0, RIGHT * 4.5 + DOWN * 1.0, 5, width=4)

        self.play(Write(title), FadeIn(subtitle, shift=DOWN), run_time=2.2)
        self.play(Create(line), run_time=2.5)
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.16), run_time=2.0)
        self.play(Indicate(arrows, color=POWER_COLOR), run_time=1.2)
        self.wait(4.0)
        self.play(FadeOut(VGroup(title, subtitle, line, arrows)), run_time=1.0)

    def long_line_problem_scene(self):
        label = section_label("1. O problema da linha longa")
        line = make_transmission_line(False).scale(0.92).shift(DOWN * 0.45)
        statement = Text("Linhas longas possuem alta reatância indutiva", font_size=34, color=TEXT_COLOR).to_edge(UP, buff=0.75)
        xl_block = RoundedRectangle(width=1.45, height=0.75, corner_radius=0.12, color=BLUE_REACTANCE, fill_color="#102A44", fill_opacity=0.65)
        xl_block.move_to(DOWN * 0.55)
        xl_text = MathTex("X_L", color=BLUE_REACTANCE).scale(0.95).move_to(xl_block)
        warning = Text("limite", font_size=24, color=WARNING_COLOR).move_to(RIGHT * 2.25 + DOWN * 0.15)
        weak_arrow = Arrow(LEFT * 2.7 + DOWN * 0.15, RIGHT * 1.8 + DOWN * 0.15, buff=0, color=WARNING_COLOR, stroke_width=3)
        formula = MathTex(r"P=\frac{V_s V_r}{", "X", r"}\sin(\delta)", color=TEXT_COLOR).scale(1.0).to_edge(DOWN, buff=0.45)
        formula[1].set_color(WARNING_COLOR)
        x_box = SurroundingRectangle(formula[1], color=WARNING_COLOR, buff=0.08)
        note = Text("X maior  →  menor potência transferível", font_size=27, color=MUTED_TEXT).next_to(formula, UP, buff=0.28)

        self.play(FadeIn(label), Create(line), run_time=1.5)
        self.play(Write(statement), run_time=1.4)
        self.play(FadeIn(xl_block, scale=0.8), Write(xl_text), Circumscribe(line[1], color=BLUE_REACTANCE), run_time=2.0)
        self.play(GrowArrow(weak_arrow), FadeIn(warning, shift=UP), run_time=1.4)
        self.play(Write(formula), run_time=2.0)
        self.play(Create(x_box), FadeIn(note, shift=UP), run_time=1.4)
        self.play(Indicate(formula[1], color=WARNING_COLOR), run_time=1.0)
        self.wait(4.0)
        self.play(FadeOut(VGroup(label, line, statement, xl_block, xl_text, weak_arrow, warning, formula, x_box, note)), run_time=1.0)

    def uncompensated_circuit_scene(self):
        label = section_label("2. Circuito equivalente sem compensação")
        title = Text("Sem compensação série", font_size=38, color=TEXT_COLOR).to_edge(UP, buff=0.7)
        circuit = make_equivalent_circuit(False).shift(UP * 0.15)
        eq = MathTex("X_{eq}", "=", "X_L", color=TEXT_COLOR).scale(1.1).next_to(circuit, DOWN, buff=0.55)
        eq[2].set_color(BLUE_REACTANCE)
        bar = make_capacity_bar("Capacidade de transmissão", 0.43, WARNING_COLOR, 4.5).next_to(eq, DOWN, buff=0.55)

        self.play(FadeIn(label), Write(title), run_time=1.4)
        self.play(Create(circuit), run_time=2.2)
        self.play(Write(eq), run_time=1.2)
        self.play(FadeIn(bar[:2]), GrowFromEdge(bar[2], LEFT), run_time=1.5)
        self.play(Indicate(bar[2], color=WARNING_COLOR), run_time=1.0)
        self.wait(4.0)
        self.play(FadeOut(VGroup(label, title, circuit, eq, bar)), run_time=1.0)

    def install_capacitor_scene(self):
        label = section_label("3. Inserção do banco de capacitor série")
        title = Text("Instalação em série no meio da linha", font_size=38, color=TEXT_COLOR).to_edge(UP, buff=0.7)
        line = make_transmission_line(False).scale(0.92).shift(DOWN * 0.45)
        cap = make_series_capacitor(DOWN * 0.55, 0.85).scale(0.95)
        cap_title = Text("Banco de Capacitor Série", font_size=32, color=CAP_COLOR).next_to(cap, UP, buff=0.55)
        xc = MathTex("X_C", color=CAP_COLOR).scale(1.1).next_to(cap, RIGHT, buff=0.35)
        xl = MathTex("X_L", color=BLUE_REACTANCE).scale(1.0).move_to(LEFT * 2.4 + UP * 0.35)
        opposite = Text("efeito oposto à reatância indutiva", font_size=27, color=MUTED_TEXT).next_to(xc, DOWN, buff=0.22)

        self.play(FadeIn(label), Write(title), Create(line), run_time=2.0)
        self.play(FadeIn(cap, scale=0.4), Circumscribe(cap[0], color=CAP_COLOR), run_time=2.0)
        self.play(Write(cap_title), Write(xc), run_time=1.2)
        self.play(FadeIn(xl), Indicate(xl, color=BLUE_REACTANCE), Indicate(xc, color=CAP_COLOR), run_time=1.4)
        self.play(FadeIn(opposite, shift=UP), run_time=1.0)
        self.wait(4.0)
        self.play(FadeOut(VGroup(label, title, line, cap, cap_title, xc, xl, opposite)), run_time=1.0)

    def reactance_compensation_scene(self):
        label = section_label("4. Compensação da reatância")
        eq = MathTex("X_{eq}", "=", "X_L", "-", "X_C", color=TEXT_COLOR).scale(1.35).to_edge(UP, buff=0.95)
        eq[2].set_color(BLUE_REACTANCE)
        eq[4].set_color(CAP_COLOR)
        before_label = Text("Antes", font_size=30, color=MUTED_TEXT).move_to(LEFT * 3.3 + UP * 0.75)
        after_label = Text("Depois", font_size=30, color=MUTED_TEXT).move_to(RIGHT * 3.3 + UP * 0.75)
        before_bar = Rectangle(width=4.5, height=0.55, color=BLUE_REACTANCE, fill_color=BLUE_REACTANCE, fill_opacity=0.65).move_to(LEFT * 3.3)
        before_text = MathTex("X_L", color=TEXT_COLOR).move_to(before_bar)
        after_bar = Rectangle(width=2.65, height=0.55, color=POWER_COLOR, fill_color=POWER_COLOR, fill_opacity=0.65).move_to(RIGHT * 3.3)
        removed = Rectangle(width=1.85, height=0.55, color=CAP_COLOR, fill_color=CAP_COLOR, fill_opacity=0.55).next_to(after_bar, RIGHT, buff=0)
        after_text = MathTex("X_{eq}", color=TEXT_COLOR).move_to(after_bar)
        xc_text = MathTex("X_C", color=CAP_COLOR).next_to(removed, UP, buff=0.18)
        arrow = Arrow(before_bar.get_right() + RIGHT * 0.4, after_bar.get_left() + LEFT * 0.4, buff=0.1, color=TEXT_COLOR)
        note = Text("A reatância equivalente da linha diminui", font_size=34, color=TEXT_COLOR).to_edge(DOWN, buff=0.75)

        self.play(FadeIn(label), Write(eq), run_time=1.6)
        self.play(Indicate(eq[4], color=CAP_COLOR), run_time=1.0)
        self.play(FadeIn(before_label), GrowFromEdge(before_bar, LEFT), Write(before_text), run_time=1.4)
        self.play(GrowArrow(arrow), FadeIn(after_label), run_time=1.0)
        self.play(ReplacementTransform(before_bar.copy(), after_bar), FadeIn(removed, shift=RIGHT), Write(after_text), Write(xc_text), run_time=1.7)
        self.play(FadeOut(removed, shift=DOWN), Indicate(after_bar, color=POWER_COLOR), Write(note), run_time=1.5)
        self.wait(4.0)
        self.play(FadeOut(VGroup(label, eq, before_label, after_label, before_bar, before_text, after_bar, after_text, xc_text, arrow, note)), run_time=1.0)

    def power_transfer_scene(self):
        label = section_label("5. Aumento da potência transferível")
        formula = MathTex(r"P=\frac{V_s V_r}{", "X_{eq}", r"}\sin(\delta)", color=TEXT_COLOR).scale(1.15).to_edge(UP, buff=0.65)
        formula[1].set_color(POWER_COLOR)
        line = make_transmission_line(True).scale(0.75).shift(DOWN * 0.15)
        weak = make_power_arrows(LEFT * 4.2 + DOWN * 0.85, RIGHT * 4.2 + DOWN * 0.85, 4, width=3, color=WARNING_COLOR)
        strong = make_power_arrows(LEFT * 4.5 + DOWN * 0.85, RIGHT * 4.5 + DOWN * 0.85, 6, width=6, color=POWER_COLOR)
        comparison = make_comparison_panel().scale(0.83).to_edge(DOWN, buff=0.25)

        self.play(FadeIn(label), Write(formula), run_time=1.6)
        self.play(Create(line), LaggedStart(*[GrowArrow(a) for a in weak], lag_ratio=0.12), run_time=2.0)
        self.play(Indicate(formula[1], color=POWER_COLOR), run_time=1.0)
        self.play(ReplacementTransform(weak, strong), run_time=1.3)
        self.play(Indicate(strong, color=POWER_COLOR), run_time=1.0)
        self.play(line.animate.scale(0.75).to_edge(UP, buff=1.45), formula.animate.scale(0.82).to_corner(UR, buff=0.35), run_time=1.2)
        self.play(FadeIn(comparison[0:4]), run_time=1.0)
        self.play(LaggedStart(*[FadeIn(item, shift=UP * 0.15) for item in comparison[4]], lag_ratio=0.2), run_time=1.4)
        self.play(LaggedStart(*[FadeIn(item, shift=UP * 0.15) for item in comparison[5]], lag_ratio=0.2), run_time=1.4)
        self.play(FadeIn(comparison[6][:2]), GrowFromEdge(comparison[6][2], LEFT), FadeIn(comparison[7][:2]), GrowFromEdge(comparison[7][2], LEFT), run_time=1.5)
        self.wait(4.0)
        self.play(FadeOut(VGroup(label, formula, line, strong, comparison)), run_time=1.0)

    def practical_benefits_scene(self):
        label = section_label("6. Benefícios práticos")
        title = Text("Por que usar compensação série?", font_size=42, color=TEXT_COLOR).to_edge(UP, buff=0.65)
        items = [
            ("↑", "Aumenta a capacidade de transmissão", POWER_COLOR),
            ("V", "Reduz queda de tensão", LINE_COLOR),
            ("δ", "Melhora a estabilidade do sistema", CAP_COLOR),
            ("+", "Evita ou adia a construção de novas linhas", MUTED_TEXT),
        ]
        rows = VGroup()
        for icon_text, sentence, color in items:
            icon_circle = Circle(radius=0.34, color=color, fill_color=color, fill_opacity=0.18, stroke_width=3)
            icon = Text(icon_text, font_size=30, color=color, weight=BOLD).move_to(icon_circle)
            text = Text(sentence, font_size=31, color=TEXT_COLOR)
            row = VGroup(icon_circle, icon, text).arrange(RIGHT, buff=0.35)
            rows.add(row)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to(DOWN * 0.15)

        self.play(FadeIn(label), Write(title), run_time=1.4)
        for row in rows:
            self.play(FadeIn(row[0], scale=0.7), Write(row[1]), FadeIn(row[2], shift=RIGHT * 0.25), run_time=0.9)
            self.play(Indicate(row[0], color=row[0].get_color()), run_time=0.35)
        self.wait(3.0)
        self.play(FadeOut(VGroup(label, title, rows)), run_time=1.0)

    def closing_scene(self):
        line = make_transmission_line(True).scale(0.9).shift(DOWN * 0.45)
        final_text = Text(
            "O banco de capacitor série compensa parte da reatância da linha\n"
            "e permite transmitir mais potência com maior estabilidade.",
            font_size=34,
            color=TEXT_COLOR,
            line_spacing=0.95,
        ).to_edge(UP, buff=0.75)
        glow = make_power_arrows(LEFT * 4.8 + DOWN * 1.0, RIGHT * 4.8 + DOWN * 1.0, 6, width=6, color=POWER_COLOR)
        formula = MathTex("X_{eq}=X_L-X_C", r"\quad", r"\Rightarrow", r"\quad", r"P_{max}\uparrow", color=TEXT_COLOR).scale(1.0).to_edge(DOWN, buff=0.55)
        formula[0].set_color(CAP_COLOR)
        formula[4].set_color(POWER_COLOR)

        self.play(Create(line), Write(final_text), run_time=2.2)
        self.play(LaggedStart(*[GrowArrow(a) for a in glow], lag_ratio=0.12), Write(formula), run_time=2.2)
        self.play(Circumscribe(line[-1][0], color=CAP_COLOR), Indicate(formula[4], color=POWER_COLOR), run_time=1.5)
        self.wait(4.0)
        self.play(FadeOut(VGroup(line, final_text, glow, formula)), run_time=1.5)
