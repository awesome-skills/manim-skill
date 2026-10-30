"""Original camera-led explanation: inspect one fixed curve at two scales."""
import numpy as np
from manim import (
    MovingCameraScene, Text, VMobject, Dot, Line, VGroup, Rectangle,
    Create, FadeIn, FadeOut, Restore, LEFT,
)


def curve_y(x):
    return 0.15 * np.asarray(x) ** 2 - 1.2


def tangent_y(x, at=1.0):
    return curve_y(at) + 0.3 * at * (np.asarray(x) - at)


class LocalLinearity(MovingCameraScene):
    def construct(self):
        bg, ink, muted = "#142727", "#F2F0DC", "#ADBDB4"
        cyan, gold = "#8CD6D0", "#F2BC74"
        self.camera.background_color = bg

        def text(words, size, color=ink):
            return Text(words, font="sans-serif", font_size=size, color=color,
                        warn_missing_font=False)

        def left(obj, x, y):
            return obj.move_to([x, y, 0], aligned_edge=LEFT)

        overview_width = self.camera.frame.width

        def view_text(words, size, color=ink):
            # Keep the same apparent text size after a camera move has settled.
            return text(words, size * self.camera.frame.width / overview_width, color)

        title = left(text("A curve, seen up close.", 46), -6.1, 3.1)
        subtitle = left(text("Keep the point. Change the scale.", 28, muted), -6.1, 2.38)
        xs = np.linspace(-4.8, 4.8, 401)
        curve = VMobject(stroke_color=cyan, stroke_width=4).set_points_smoothly(
            np.column_stack([xs, curve_y(xs), np.zeros(len(xs))]))
        point = np.array([1.0, float(curve_y(1.0)), 0])
        marker = Dot(point, radius=.035, color=ink).set_z_index(5)
        tangent = Line([-4.8, float(tangent_y(-4.8)), 0],
                       [4.8, float(tangent_y(4.8)), 0], color=gold, stroke_width=2.5)
        legend = VGroup(text("Curve", 27, cyan), text("Tangent at the point", 27, gold)).arrange(buff=.6).move_to([0, -3.05, 0])
        self.camera.frame.save_state()
        self.next_section("whole")
        self.add(title, subtitle)
        self.play(Create(curve), run_time=1.2)
        self.play(FadeIn(marker), Create(tangent), FadeIn(legend), run_time=1)
        self.wait(1.3)
        window = Rectangle(width=3, height=3 * 9 / 16, color=ink,
                           stroke_opacity=.6, stroke_width=1).move_to(point)
        self.play(Create(window), run_time=.5)
        self.wait(.6)

        self.next_section("closer")
        self.play(FadeOut(title), FadeOut(subtitle), FadeOut(legend), FadeOut(window), run_time=.35)
        self.play(self.camera.frame.animate.move_to(point).set(width=3), run_time=2)
        near_title = left(view_text("Same point. Same curve.", 48), point[0] - 1.3, point[1] + .65)
        near_caption = view_text("The tangent is a local approximation.", 42, muted).move_to(point + [0, -.65, 0])
        self.play(FadeIn(near_title), FadeIn(near_caption), run_time=.4)
        self.wait(1.8)

        self.next_section("closer_still")
        self.play(FadeOut(near_title), FadeOut(near_caption), run_time=.25)
        self.play(self.camera.frame.animate.set(width=1.5), run_time=1.5)
        closer_title = left(view_text("A smaller neighborhood", 48), point[0] - .65, point[1] + .32)
        closer_caption = view_text("Curve and tangent nearly coincide here.", 42, muted).move_to(point + [0, -.33, 0])
        self.play(FadeIn(closer_title), FadeIn(closer_caption), run_time=.4)
        self.wait(1.8)
        self.play(FadeOut(closer_title), FadeOut(closer_caption), run_time=.25)

        self.next_section("return_to_context")
        self.play(Restore(self.camera.frame), run_time=1.8)
        conclusion = left(text("Locally straight. Globally curved.", 44), -6.1, 3.1)
        self.play(FadeIn(conclusion), FadeIn(legend), run_time=.5)
        self.wait(2)
