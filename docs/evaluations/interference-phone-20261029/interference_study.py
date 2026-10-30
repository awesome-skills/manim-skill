"""Original editorial art direction for the same A + B experiment.

All three plots retain the same vertical scale. The result envelope is computed
from phase, not estimated from sampled extrema. No external fonts/assets/TeX.
"""
import numpy as np
from manim import (
    Scene, Text, Line, VGroup, VMobject, Polygon, ValueTracker,
    DecimalNumber, Create, Dot, FadeIn, FadeOut, always_redraw, LEFT, RIGHT,
)


class InterferenceStudy(Scene):
    def construct(self):
        paper, ink, muted = "#F4F1E9", "#203C43", "#657779"
        blue, coral, rule = "#386D87", "#B86148", "#CAD0CA"
        self.camera.background_color = paper

        def label(words, size=22, color=ink, serif=False):
            return Text(words, font="serif" if serif else "sans-serif",
                        font_size=size, color=color, warn_missing_font=False)

        def left_at(obj, x, y):
            return obj.move_to([x, y, 0], aligned_edge=LEFT)

        heading = left_at(label("When waves meet", 52, serif=True), -6.2, 3.12)
        top_rule = Line([-6.2, 2.65, 0], [6.2, 2.65, 0], color=rule, stroke_width=1)
        scale_note = label("Same scale", 26, muted)
        scale_note.move_to([6.2, 3.12, 0], aligned_edge=RIGHT)
        self.add(heading, top_rule, scale_note)

        phase = ValueTracker(0)
        baselines = [1.37, -0.05, -2.05]
        colors = [blue, coral, ink]
        xs = np.linspace(-np.pi, 3 * np.pi, 241)
        screen_x = np.linspace(-1.55, 6.05, len(xs))
        scale = 0.52

        def values(i):
            a = np.sin(xs)
            b = 0.75 * np.sin(xs + phase.get_value())
            return (a, b, a + b)[i]

        def curve(i):
            pts = np.column_stack((screen_x, baselines[i] + scale * values(i), np.zeros(len(xs))))
            return VMobject(stroke_color=colors[i], stroke_width=4 if i < 2 else 5).set_points_smoothly(pts)

        axes = VGroup(*[Line([-1.65, y, 0], [6.15, y, 0], color=rule, stroke_width=1)
                       for y in baselines])
        plot_labels = VGroup(*[left_at(label(s, 29, c), -1.65, y + offset)
                              for s, c, y, offset in zip(
                                  ["A · 1.00", "B · 0.75", "A + B"],
                                  colors, baselines, [0.8, 0.67, 1.15])])
        curves = [always_redraw(lambda i=i: curve(i)) for i in range(3)]

        def wash():
            points = [[screen_x[0], baselines[2], 0]]
            points += [[x, baselines[2] + scale * y, 0] for x, y in zip(screen_x, values(2))]
            points += [[screen_x[-1], baselines[2], 0]]
            return Polygon(*points, stroke_width=0, fill_color=ink, fill_opacity=0.07)

        fill = always_redraw(wash)
        eyebrow = left_at(label("Sum amplitude", 28, muted), -6.2, 0.82)
        class Numeral(Text):
            def __init__(self, value, **kwargs):
                super().__init__(value, font="serif", warn_missing_font=False, **kwargs)

        number = DecimalNumber(1.75, num_decimal_places=2, font_size=76, color=ink,
                               mob_class=Numeral)
        number.add_updater(lambda m: left_at(m.set_value(
            np.sqrt(1 + 0.75 ** 2 + 1.5 * np.cos(phase.get_value()))), -6.2, -0.02))
        number.update()
        ratio_note = left_at(label("Relative to A", 26, muted), -6.2, -0.72)
        phase_rule = Line([-6.2, -1.25, 0], [-3.15, -1.25, 0], color=rule, stroke_width=1)

        def caption(first, second):
            return VGroup(left_at(label(first, 33, serif=True), -6.2, -1.78),
                          left_at(label(second, 26, muted), -6.2, -2.3))

        aligned = caption("Aligned", "Reinforce")
        opposed = caption("Opposed", "Small remainder")
        phase_label = left_at(label("B phase", 24, muted), -1.65, -3.25)
        phase_track = Line([.3, -3.25, 0], [5.8, -3.25, 0], color=rule, stroke_width=2)
        marker = always_redraw(lambda: Dot([.3 + 5.5 * phase.get_value() / (2 * np.pi), -3.25, 0],
                                            radius=0.07, color=coral))
        ticks = VGroup(*[label(s, 25, muted).move_to([x, -3.65, 0])
                        for s, x in [("0", .3), ("½", 3.05), ("1 turn", 5.8)]])

        self.next_section("establish_inputs")
        self.play(Create(axes), FadeIn(plot_labels), run_time=0.8)
        self.play(Create(curves[0]), Create(curves[1]), run_time=1.3)
        self.wait(0.5)
        self.next_section("result")
        self.play(FadeIn(fill), FadeIn(curves[2]), FadeIn(eyebrow), FadeIn(number),
                  FadeIn(ratio_note), Create(phase_rule), FadeIn(aligned), run_time=1.0)
        self.play(FadeIn(VGroup(phase_label, phase_track, ticks)), FadeIn(marker), run_time=0.5)
        self.wait(1.7)
        self.next_section("opposition")
        self.play(FadeOut(aligned), run_time=0.25)
        self.play(phase.animate.set_value(np.pi), run_time=3.5)
        self.play(FadeIn(opposed), run_time=0.35)
        self.wait(2)
        self.next_section("resolve")
        self.play(FadeOut(opposed), run_time=0.25)
        self.play(phase.animate.set_value(2 * np.pi), run_time=3.5)
        self.play(FadeIn(aligned), run_time=0.35)
        self.wait(2)
        for mob in [*curves, fill, marker, number]:
            mob.clear_updaters()
