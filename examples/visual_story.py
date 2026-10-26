"""Original head-to-tail vector explanation; ManimCE, Pango only, no TeX."""
import numpy as np
from manim import (
    Arrow, Create, DashedLine, Dot, FadeIn, FadeOut, LEFT, NumberPlane,
    Scene, Text, TransformFromCopy, UP, VGroup,
)


class VectorStory(Scene):
    def construct(self):
        self.next_section("same_origin")
        self.camera.background_color = "#101722"
        ink, muted = "#EDF2F7", "#96A6BC"
        blue, amber, mint = "#73BFFF", "#FFC979", "#77E0B5"

        def caption(words):
            return Text(words, font_size=27, color=muted).move_to([0, -3.15, 0])

        title = Text("How do two vectors add?", font_size=40, color=ink)
        title.to_edge(UP, buff=0.48)
        plane = NumberPlane(
            x_range=[-1, 6, 1], y_range=[-1, 4, 1], x_length=8.4, y_length=4.5,
            background_line_style={"stroke_color": "#50637D", "stroke_opacity": 0.22},
            axis_config={"stroke_color": "#8191A7", "stroke_opacity": 0.45,
                         "include_ticks": False},
        ).move_to([0, -0.05, 0])
        origin, a_tip, b_tip, end = [plane.c2p(*p) for p in [(0, 0), (3, 1), (1, 2), (4, 3)]]
        a = Arrow(origin, a_tip, buff=0, color=blue, stroke_width=7)
        b = Arrow(origin, b_tip, buff=0, color=amber, stroke_width=7)
        a_label = Text("a", font_size=32, color=blue).next_to(a.get_center(), [0, -1, 0], buff=0.15)
        b_label = Text("b", font_size=32, color=amber).next_to(b.get_center(), LEFT, buff=0.16)
        origin_dot = Dot(origin, radius=0.065, color=ink)
        words = caption("Start with two displacements from the same origin.")
        self.play(FadeIn(title), Create(plane), run_time=1)
        self.play(FadeIn(origin_dot), Create(a), FadeIn(a_label), run_time=0.8)
        self.play(Create(b), FadeIn(b_label), FadeIn(words), run_time=0.8)
        self.wait(1.5)
        self.play(FadeOut(words), run_time=0.25)
        words = caption("Slide b to the tip of a. Its direction and length stay the same.")
        self.play(FadeIn(words), run_time=0.3)
        ghost = b.copy().set_opacity(0.18)
        self.add(ghost)
        self.next_section("head_to_tail")
        offset = a_tip - origin
        self.play(b.animate.shift(offset), b_label.animate.shift(offset), run_time=1.8)
        assert np.allclose(b.get_start(), a_tip)
        assert np.allclose(b.get_end(), end)
        self.wait(1.2)
        tip = Dot(end, radius=0.075, color=mint)
        guides = VGroup(
            DashedLine(end, plane.c2p(4, 0), color=mint, stroke_opacity=0.35),
            DashedLine(end, plane.c2p(0, 3), color=mint, stroke_opacity=0.35),
        )
        self.play(FadeIn(tip), Create(guides), run_time=0.7)
        self.play(FadeOut(words), run_time=0.25)
        words = caption("The sum is the single displacement to the final endpoint.")
        self.next_section("resultant")
        result = Arrow(origin, end, buff=0, color=mint, stroke_width=8)
        result_label = Text("a + b", font_size=34, color=mint)
        result_label.next_to(result.get_center(), UP, buff=0.22)
        self.play(Create(result), FadeIn(result_label), FadeIn(words), run_time=1.3)
        self.wait(1.5)
        self.play(FadeOut(ghost), FadeOut(guides), run_time=0.5)
        equation = VGroup(
            Text("a", color=blue, font_size=34), Text("+", color=ink, font_size=34),
            Text("b", color=amber, font_size=34), Text("=", color=ink, font_size=34),
            Text("a + b", color=mint, font_size=34),
        ).arrange(buff=0.2).move_to([0, -2.45, 0])
        self.play(TransformFromCopy(a_label, equation[0]),
                  TransformFromCopy(b_label, equation[2]),
                  TransformFromCopy(result_label, equation[4]),
                  FadeIn(equation[1]), FadeIn(equation[3]), run_time=1)
        self.wait(2)
