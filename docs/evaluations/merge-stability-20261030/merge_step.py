"""Original editorial-style merge: persistent cards travel through clear lanes."""
from manim import (
    Circle, Create, DOWN, FadeIn, FadeOut, LaggedStart, Line,
    MoveAlongPath, CubicBezier, RoundedRectangle, Scene, Text, UP, VGroup,
)


def merge_trace(left, right):
    """Stable merge events; source identity remains separate from its value."""
    i = j = 0
    events = []
    while i < len(left) or j < len(right):
        take_left = j == len(right) or (i < len(left) and left[i] <= right[j])
        side, index = ("left", i) if take_left else ("right", j)
        events.append((side, index, (left if take_left else right)[index]))
        if take_left:
            i += 1
        else:
            j += 1
    return events


class MergeStep(Scene):
    def construct(self):
        def text(words, **kwargs):
            return Text(words, font="serif", warn_missing_font=False, **kwargs)

        paper, ink, muted = "#F6F3EC", "#202C37", "#566774"
        blue, rust = "#216D92", "#A3472B"
        self.camera.background_color = paper
        title = text("One ordered stream", color=ink, font_size=46)
        title.move_to([0, 3.05, 0])
        rule = Line([-6, 2.35, 0], [6, 2.35, 0], color=ink, stroke_opacity=0.2)
        self.add(title, rule)

        left, right = [2, 5, 8], [3, 5, 9]
        cards = {}
        for side, values, color, xs in [
            ("left", left, blue, [-4.7, -3.3, -1.9]),
            ("right", right, rust, [1.9, 3.3, 4.7]),
        ]:
            for index, (value, x) in enumerate(zip(values, xs)):
                tile = RoundedRectangle(width=1.05, height=1.18, corner_radius=0.14,
                                        stroke_color=color, stroke_width=2,
                                        fill_color=paper, fill_opacity=1)
                label = text(str(value), font_size=40, color=color).shift(0.12 * UP)
                origin = text("L" if side == "left" else "R", font_size=22, color=color)
                origin.shift(0.36 * DOWN)
                card = VGroup(tile, label, origin).move_to([x, 0.8, 0])
                cards[(side, index)] = card
        left_label = text("LEFT / sorted", font_size=28, color=blue).move_to([-3.3, 1.95, 0])
        right_label = text("RIGHT / sorted", font_size=28, color=rust).move_to([3.3, 1.95, 0])
        slots = VGroup(*[
            RoundedRectangle(width=1.05, height=1.18, corner_radius=0.14,
                             stroke_color=muted, stroke_width=1, stroke_opacity=0.3)
            .move_to([-3.5 + 1.4 * k, -1.65, 0]) for k in range(6)
        ])
        self.next_section("two_sorted_runs")
        self.play(FadeIn(left_label), FadeIn(right_label),
                  LaggedStart(*[FadeIn(c, shift=0.15 * UP) for c in cards.values()],
                              lag_ratio=0.12), Create(slots), run_time=1.2)
        caption_words = "Compare the heads. Take the smaller value."
        caption = text(caption_words,
                       color=ink, font_size=29).move_to([0, -2.85, 0])
        self.play(FadeIn(caption), run_time=0.4)
        self.wait(1)
        heads = {"left": 0, "right": 0}
        for k, (side, index, value) in enumerate(merge_trace(left, right)):
            self.next_section(f"take_{side}_{index}")
            tied = (heads["left"] < len(left) and heads["right"] < len(right)
                    and left[heads["left"]] == right[heads["right"]])
            exhausted = heads["left"] == len(left) or heads["right"] == len(right)
            words = ("Equal values: take the left one first." if tied else
                     "One run is empty. Take the remaining item." if exhausted else
                     "Compare the heads. Take the smaller value.")
            if caption_words != words:
                next_caption = text(words, color=ink, font_size=29).move_to([0, -2.85, 0])
                self.remove(caption)
                self.add(next_caption)
                self.wait(0.25)
                caption = next_caption
                caption_words = words
            markers = VGroup(*[
                Circle(radius=0.10, color=ink, fill_opacity=1)
                .next_to(cards[(s, n)], UP, buff=0.16)
                for s, n in heads.items() if n < 3
            ])
            self.play(FadeIn(markers), run_time=0.2)
            self.wait(1.4 if tied else 0.6 if k < 2 else 0.25)
            card = cards[(side, index)]
            start, end = card.get_center(), slots[k].get_center()
            # The entire route stays below the source row and above the caption.
            path = CubicBezier(start, start + 0.9 * DOWN, end + 0.9 * UP, end)
            self.play(MoveAlongPath(card, path), FadeOut(markers),
                      run_time=1.1 if k < 2 or tied else 0.65)
            heads[side] += 1
        self.next_section("ordered_result")
        self.play(FadeOut(caption), FadeOut(left_label), FadeOut(right_label),
                  FadeOut(slots), run_time=0.3)
        result = VGroup(*[cards[(side, index)] for side, index, _ in merge_trace(left, right)])
        self.play(result.animate.shift(1.6 * UP), run_time=0.8)
        caption = text("Equal values keep their original order.",
                       color=ink, font_size=30).move_to([0, -1.3, 0])
        self.play(FadeIn(caption), run_time=0.4)
        self.wait(2)
