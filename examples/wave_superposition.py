"""Original continuous-state example: one phase drives both inputs and their sum."""
import numpy as np
from manim import (
    Create, Dot, FadeIn, FadeOut, Line, Scene, Text, ValueTracker,
    VGroup, VMobject, always_redraw, linear,
)


def wave_values(x, phase):
    first = np.sin(x)
    second = 0.75 * np.sin(x + phase)
    return first, second, first + second


class WaveSuperposition(Scene):
    def construct(self):
        def text(words, **kwargs):
            return Text(words, font="sans-serif", warn_missing_font=False, **kwargs)

        self.camera.background_color = "#101923"
        ink, muted = "#EAF1F4", "#9CAEBB"
        colors = ["#70C6E3", "#E9B775", "#B9DFC5"]
        title = text("Same place. Add the heights.", font_size=42, color=ink)
        title.move_to([0, 3.25, 0])
        self.add(title)
        baselines = [1.65, 0.1, -1.85]
        phase = ValueTracker(0)
        probe = ValueTracker(-4.4)
        xs = np.linspace(-4.8, 4.8, 161)

        def curve(index):
            values = wave_values(xs, phase.get_value())[index]
            points = np.column_stack((xs, baselines[index] + 0.62 * values, np.zeros_like(xs)))
            return VMobject(stroke_color=colors[index], stroke_width=4).set_points_as_corners(points)

        axes = VGroup(*[
            Line([-5, y, 0], [5, y, 0], color=muted, stroke_width=1, stroke_opacity=0.4)
            for y in baselines
        ])
        labels = VGroup(*[
            text(label, font_size=26, color=color).move_to([-5.8, y, 0])
            for label, color, y in zip(["A", "B", "A + B"], colors, baselines)
        ])
        curves = [always_redraw(lambda i=i: curve(i)) for i in range(3)]
        self.next_section("two_inputs")
        self.play(Create(axes), FadeIn(labels), FadeIn(curves[0]), FadeIn(curves[1]), run_time=1)
        self.wait(0.6)
        self.next_section("sum_at_every_position")
        self.play(FadeIn(curves[2]), run_time=0.8)

        def samples():
            x = probe.get_value()
            values = wave_values(x, phase.get_value())
            guide = Line([x, 2.35, 0], [x, -3.0, 0], color=muted,
                         stroke_width=1, stroke_opacity=0.3)
            dots = [Dot([x, y + 0.62 * v, 0], radius=0.065, color=c)
                    for y, v, c in zip(baselines, values, colors)]
            return VGroup(guide, *dots)

        samples_view = always_redraw(samples)
        caption = text("The guide samples all three curves at the same x.",
                       color=ink, font_size=24).move_to([0, -3.45, 0])
        self.play(FadeIn(samples_view), FadeIn(caption), run_time=0.5)
        self.play(probe.animate.set_value(4.4), rate_func=linear, run_time=4)
        self.play(FadeOut(samples_view), FadeOut(caption), run_time=0.3)
        self.next_section("change_phase")
        caption = text("Shift B by half a cycle: the sum shrinks.",
                       color=ink, font_size=24).move_to([0, -3.45, 0])
        self.play(FadeIn(caption), run_time=0.4)
        self.play(phase.animate.set_value(np.pi), run_time=3)
        self.wait(1.5)
        self.next_section("restore_phase")
        self.play(FadeOut(caption), run_time=0.3)
        caption = text("Align them again: the sum grows.",
                       color=ink, font_size=24).move_to([0, -3.45, 0])
        self.play(FadeIn(caption), run_time=0.4)
        self.play(phase.animate.set_value(2 * np.pi), run_time=3)
        self.wait(1.8)
        for curve_view in curves:
            curve_view.clear_updaters()
