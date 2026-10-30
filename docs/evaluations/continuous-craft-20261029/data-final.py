"""Original data-story scene: the same 24 records become three count bars.

Synthetic categories, not a real survey. Each dot keeps its identity while it
moves into a category and becomes one equal-height bar unit. No plugin needed.
"""
from collections import Counter
import numpy as np
from manim import (
    Scene, Text, Dot, Line, VGroup,
    Create, FadeIn, FadeOut, Transform, LaggedStart, LEFT,
)

RECORDS = tuple("ABCBCBACBCABCBABCBCABCAB")


class DataToDecision(Scene):
    def construct(self):
        paper, ink, muted = "#EDF2F7", "#172C42", "#596E83"
        palette = {"A": "#317C96", "B": "#7563B4", "C": "#BD633A"}
        names = {"A": "Explore", "B": "Build", "C": "Share"}
        self.camera.background_color = paper

        def text(words, size=24, color=ink):
            return Text(words, font="sans-serif", font_size=size,
                        color=color, warn_missing_font=False)

        def left(obj, x, y):
            return obj.move_to([x, y, 0], aligned_edge=LEFT)

        total = len(RECORDS)
        counts = Counter(RECORDS)
        title = left(text("24 records. Three choices.", 44), -6.15, 2.95)
        kicker = left(text("DATA STORIES  /  02", 17, muted), -6.15, 3.55)
        foot = left(text("Illustrative data", 28, muted), -6.15, -3.45)
        self.add(kicker, title, foot)
        dots = VGroup(*[
            Dot([-4.4 + (i % 8) * 1.25, 1.15 - (i // 8) * 1.05, 0],
                radius=0.16, color=palette[category])
            for i, category in enumerate(RECORDS)
        ])
        legend = VGroup(*[VGroup(Dot(radius=0.06, color=palette[c]),
                                  text(names[c], 32, muted)).arrange(buff=0.15)
                         for c in "ABC"]).arrange(buff=0.6).move_to([0, -2.45, 0])
        self.next_section("records")
        self.play(LaggedStart(*[FadeIn(d, scale=0.7) for d in dots], lag_ratio=0.035),
                  FadeIn(legend), run_time=1.3)
        self.wait(1.2)

        centers = {"A": -3.8, "B": 0, "C": 3.8}
        groups = {c: [i for i, value in enumerate(RECORDS) if value == c] for c in "ABC"}
        category_labels = VGroup(*[text(names[c], 40, palette[c]).move_to([centers[c], -2.45, 0]) for c in "ABC"])
        grouped = {}
        for c, ids in groups.items():
            for rank, i in enumerate(ids):
                grouped[i] = np.array([centers[c] + (rank % 2 - 0.5) * 0.6,
                                       1.35 - (rank // 2) * 0.6, 0])
        self.next_section("group")
        self.play(FadeOut(legend), FadeOut(title), run_time=0.3)
        title = left(text("Group by what they chose.", 44), -6.15, 2.95)
        self.play(FadeIn(title), FadeIn(category_labels), run_time=0.4)
        # Simultaneous paths preserve the same record objects, not replacements.
        self.play(*[dot.animate.move_to(grouped[i]) for i, dot in enumerate(dots)], run_time=2.1)
        self.wait(1.3)

        self.next_section("count")
        self.play(FadeOut(title), run_time=0.25)
        title = left(text("Stack the same records. Count.", 42), -6.15, 2.95)
        self.play(FadeIn(title), run_time=0.35)
        base, unit = -1.95, 0.34
        baseline = Line([-5.4, base - 0.04, 0], [5.4, base - 0.04, 0], color=muted,
                        stroke_width=1, stroke_opacity=0.45)
        self.play(Create(baseline), run_time=0.35)
        targets = {}
        for c, ids in groups.items():
            for rank, i in enumerate(ids):
                targets[i] = dots[i].copy().stretch_to_fit_width(0.82).stretch_to_fit_height(unit - 0.025)
                targets[i].move_to([centers[c], base + unit * (counts[c] - rank - 0.5), 0])
        # Arrange small circular units first; widen only after their lanes are clear.
        stack_dots = [dot.copy().scale(0.875).move_to(targets[i].get_center())
                      for i, dot in enumerate(dots)]
        self.play(*[Transform(dot, stack_dots[i]) for i, dot in enumerate(dots)], run_time=1.4)
        self.play(*[Transform(dot, targets[i]) for i, dot in enumerate(dots)], run_time=0.8)
        count_labels = VGroup(*[text(str(counts[c]), 38, palette[c]).move_to(
            [centers[c], base + counts[c] * unit + 0.43, 0]) for c in "ABC"])
        self.play(FadeIn(count_labels), run_time=0.4)
        self.wait(1.4)

        self.next_section("conclusion")
        self.play(FadeOut(title), run_time=0.25)
        winner = max(counts, key=counts.get)
        title = left(text(f"{names[winner]} leads: {counts[winner]} of {total}.", 44), -6.15, 2.95)
        note = text("Each mark is one record.", 32, muted).move_to([0, -2.98, 0])
        # Keep every unit visible; only reduce competing emphasis.
        self.play(FadeIn(title), FadeIn(note),
                  *[dot.animate.set_fill(opacity=0.52) for i, dot in enumerate(dots)
                    if RECORDS[i] != winner], run_time=0.7)
        self.wait(2.5)
