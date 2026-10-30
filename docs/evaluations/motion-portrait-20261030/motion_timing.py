"""Original timing study: shared time, separate monotonic position mappings."""
import numpy as np
from manim import Dot, FadeIn, FadeOut, Line, Scene, Text, ValueTracker, VGroup, config, linear, tempconfig


def soft_progress(t):
    """Cubic Hermite progress on [0, 1]; stationary endpoints, no overshoot."""
    return t * t * (3 - 2 * t)


class MotionTiming(Scene):
    def __init__(self, **kwargs):
        aspect = config.pixel_width / config.pixel_height
        with tempconfig({"frame_width": config.frame_height * aspect}):
            super().__init__(**kwargs)

    def construct(self):
        paper, ink, muted = "#F4EFE5", "#283B3B", "#586D69"
        colors = ["#1D777D", "#B24E30"]
        self.camera.background_color = paper
        portrait = self.camera.frame_width < self.camera.frame_height
        half_path = self.camera.frame_width / 2 - .5 if portrait else 4.9
        start, finish = -half_path, half_path
        progress = ValueTracker(0)
        mappings = [lambda t: t, soft_progress]
        ys = [0.85, -1.0]

        def position(row, t):
            return np.array([start + (finish - start) * mappings[row](t), ys[row], 0])

        def text(words, size, color=ink):
            return Text(words, font="serif", warn_missing_font=False,
                        font_size=size, color=color)

        title = text("Same path.\nDifferent timing." if portrait else "Same path. Different timing.",
                     32 if portrait else 46).move_to([0, 2.9 if portrait else 3.05, 0])
        labels = VGroup(*[
            text(words, 24 if portrait else 31, colors[row]).move_to([start, ys[row] + .6, 0], aligned_edge=[-1, 0, 0])
            for row, words in enumerate(["Constant speed", "Ease in / out"])
        ])
        rails = VGroup(*[
            Line([start, y, 0], [finish, y, 0], color=muted, stroke_width=2, stroke_opacity=.3)
            for y in ys
        ])
        ends = VGroup(*[
            Line([x, y-.14, 0], [x, y+.14, 0], color=muted, stroke_width=2)
            for y in ys for x in [start, finish]
        ])
        dots = VGroup(*[Dot(position(row, 0), radius=.10 if portrait else .15, color=colors[row]) for row in range(2)])
        for row, dot in enumerate(dots):
            dot.add_updater(lambda item, row=row: item.move_to(position(row, progress.get_value())))
        caption = text("Equal distance.\nFour seconds each." if portrait else "Equal distance. Four seconds each.",
                       26 if portrait else 31, muted).move_to([0, -2.7, 0])
        self.next_section("compare_timing")
        self.play(FadeIn(title), FadeIn(labels), FadeIn(rails), FadeIn(ends), FadeIn(caption), run_time=.7)
        self.play(FadeIn(dots), run_time=.4)
        self.wait(.7)
        # The shared clock is linear. Easing happens once, only in position().
        self.play(progress.animate.set_value(1), rate_func=linear, run_time=4)
        self.wait(.8)

        self.next_section("equal_time_samples")
        self.play(FadeOut(dots), FadeOut(caption), run_time=.3)
        progress.set_value(0)
        caption = text("Replay: one mark\nevery half-second." if portrait else "Replay: one mark every half-second.",
                       26 if portrait else 31, muted).move_to([0, -2.7, 0])
        marks = VGroup()
        for row in range(2):
            for time in np.linspace(0, 1, 9):
                mark = Dot(position(row, time), radius=.04 if portrait else .065, color=colors[row])
                mark.add_updater(lambda item, time=time: item.set_opacity(
                    .65 if progress.get_value() >= time - 1e-9 else 0))
                marks.add(mark)
        self.add(marks)
        self.play(FadeIn(caption), FadeIn(dots), run_time=.4)
        self.play(progress.animate.set_value(1), rate_func=linear, run_time=4)
        self.wait(.7)
        self.play(FadeOut(caption), run_time=.2)
        caption = text("Closer marks.\nSlower movement." if portrait else "Closer marks mean slower movement.",
                       26 if portrait else 31, muted).move_to([0, -2.7, 0])
        self.play(FadeIn(caption), run_time=.3)
        self.wait(2)
