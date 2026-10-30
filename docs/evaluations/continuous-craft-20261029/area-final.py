"""Original typographic geometry: doubling a side gives four unit squares.

A fixed lower-left corner anchors the length change. Three copies of the unit
square fill the enlarged outline; numeric emphasis changes only after the proof.
"""
import numpy as np
from manim import (
    Scene, Text, Square, VGroup, Line, DoubleArrow, Create, FadeIn, FadeOut,
    Transform, LaggedStart, LEFT, RIGHT, UP,
)


class AreaScaleStory(Scene):
    def construct(self):
        ground, ink, accent = "#2347B7", "#F9FAF3", "#E6EB9D"
        self.camera.background_color = ground

        def text(words, size, color=ink, weight="NORMAL"):
            return Text(words, font="sans-serif", font_size=size, color=color,
                        weight=weight, warn_missing_font=False)

        def left(obj, x, y):
            return obj.move_to([x, y, 0], aligned_edge=LEFT)

        heading = left(text("A CHANGE OF SCALE", 22), -6.05, 3.25)
        rule = Line([-6.05, 2.8, 0], [6.05, 2.8, 0], color=ink, stroke_width=1, stroke_opacity=.35)
        factor = left(text("2×", 138, weight="BOLD"), -6.05, 1.0)
        role = left(text("the side", 46), -6.05, -.6)
        question = left(text("What happens to area?", 28), -6.05, -1.6)
        self.add(heading, rule)
        self.play(FadeIn(factor, shift=UP * .15), FadeIn(role), run_time=.7)

        unit = 1.65
        corner = np.array([1.15, -1.65, 0])
        center = corner + np.array([unit / 2, unit / 2, 0])
        tile = Square(side_length=unit, fill_color=accent, fill_opacity=1,
                      stroke_color=ground, stroke_width=3).move_to(center)
        one = text("1", 40, ground, "BOLD").move_to(center)
        original = VGroup(tile, one)
        outline = Square(side_length=unit, stroke_color=ink, stroke_width=3).move_to(center).set_z_index(3)
        measure = DoubleArrow(corner + [0, -.5, 0], corner + [unit, -.5, 0],
                              buff=0, color=ink, stroke_width=2, tip_length=.12)
        length_label = text("1", 27).next_to(measure, direction=-UP, buff=.12)
        self.next_section("unit_square")
        self.play(FadeIn(original), Create(outline), Create(measure), FadeIn(length_label),
                  FadeIn(question), run_time=.8)
        self.wait(1.3)

        self.next_section("double_the_side")
        larger = Square(side_length=2 * unit, stroke_color=ink, stroke_width=3).move_to(corner + [unit, unit, 0])
        longer = DoubleArrow(corner + [0, -.5, 0], corner + [2 * unit, -.5, 0],
                             buff=0, color=ink, stroke_width=2, tip_length=.12)
        two = text("2", 27).next_to(longer, direction=-UP, buff=.12)
        self.play(Transform(outline, larger), Transform(measure, longer),
                  Transform(length_label, two), run_time=1.5)
        self.wait(.8)

        self.next_section("tile_the_area")
        copies = [original.copy() for _ in range(3)]
        offsets = [RIGHT * unit, UP * unit, (RIGHT + UP) * unit]
        self.add(*copies)
        self.play(LaggedStart(*[copy.animate.shift(offset) for copy, offset in zip(copies, offsets)],
                              lag_ratio=.22), run_time=2.1)
        self.wait(1.2)
        self.play(FadeOut(factor), FadeOut(role), FadeOut(question), run_time=.25)
        factor = left(text("4×", 138, accent, "BOLD"), -6.05, 1.0)
        role = left(text("the area", 46), -6.05, -.6)
        proof = left(text("2 rows × 2 columns", 28), -6.05, -1.6)
        self.play(FadeIn(factor, shift=UP * .12), FadeIn(role), FadeIn(proof), run_time=.6)
        self.wait(1.8)
        self.next_section("resolve")
        end = text("Twice as wide. Twice as tall.", 32).move_to([0, -3.2, 0])
        self.play(FadeIn(end), run_time=.5)
        self.wait(2)
