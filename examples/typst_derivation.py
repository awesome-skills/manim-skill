"""Original, labeled derivation for CE 0.22; requires the existing Typst extra.

Each occurrence has its own label, including the three copies of b squared.
Render: uv run python -m manim render -ql examples/typst_derivation.py TypstDerivation
"""
from manim import (
    BLUE_B, Create, FadeIn, FadeOut, GREEN_B, Line, MathTypst,
    ReplacementTransform, Scene, Text, UP, VGroup, YELLOW_B,
)


def equation_parts(terms):
    """Keep Typst's full-equation layout, then expose disjoint named groups."""
    source = " ".join("{{ " + content + " : " + key + " }}" for key, content in terms)
    formula = MathTypst(source, font_size=84)
    parts = {key: formula.select(key) for key, _ in terms}
    # All stages share the equals sign as a spatial anchor.
    formula.shift(-parts["equals"].get_center())
    for key, part in parts.items():
        assert len(part), f"Empty Typst selection: {key}"
        if key == "left_a":
            part.set_color(BLUE_B)
        elif key == "right_c":
            part.set_color(GREEN_B)
        elif key in {"left_b", "subtract_left_b", "subtract_right_b"}:
            part.set_color(YELLOW_B)
    return parts


class TypstDerivation(Scene):
    def construct(self):
        self.camera.background_color = "#101722"
        title = Text("Keep both sides equal", font_size=40).to_edge(UP, buff=0.6)
        caption = Text("Start with the same relationship.", font_size=27)
        caption.move_to([0, -2.1, 0])
        first = equation_parts([
            ("left_a", "a^2"), ("left_plus", "+"), ("left_b", "b^2"),
            ("equals", "="), ("right_c", "c^2"),
        ])
        second = equation_parts([
            ("left_a", "a^2"), ("left_plus", "+"), ("left_b", "b^2"),
            ("left_minus", "-"), ("subtract_left_b", "b^2"),
            ("equals", "="), ("right_c", "c^2"),
            ("right_minus", "-"), ("subtract_right_b", "b^2"),
        ])
        final = equation_parts([
            ("left_a", "a^2"), ("equals", "="), ("right_c", "c^2"),
            ("right_minus", "-"), ("subtract_right_b", "b^2"),
        ])
        self.next_section("relationship")
        # Add the selections, not their parent formula: each glyph has one owner.
        self.play(FadeIn(title), FadeIn(caption), *[FadeIn(p) for p in first.values()])
        self.wait(1.5)
        self.next_section("subtract_both_sides")
        self.play(FadeOut(caption), run_time=0.25)
        caption = Text("Subtract b squared from BOTH sides.", font_size=27)
        caption.move_to([0, -2.1, 0])
        self.play(FadeIn(caption), run_time=0.3)
        self.play(*[ReplacementTransform(first[k], second[k]) for k in first], run_time=1)
        added = ["left_minus", "subtract_left_b", "right_minus", "subtract_right_b"]
        self.play(*[FadeIn(second[k], shift=0.15 * UP) for k in added], run_time=0.7)
        self.wait(1.5)
        self.next_section("cancel_and_resolve")
        cancelled = VGroup(*[second[k] for k in
                             ["left_plus", "left_b", "left_minus", "subtract_left_b"]])
        strike = Line(cancelled.get_left(), cancelled.get_right(), color=YELLOW_B)
        self.play(Create(strike), run_time=0.5)
        self.wait(0.6)
        self.play(FadeOut(caption), run_time=0.25)
        caption = Text("The added and subtracted terms cancel on the left.", font_size=27)
        caption.move_to([0, -2.1, 0])
        # Remove the strike before retained terms move through its old position.
        self.play(FadeOut(cancelled), FadeOut(strike), FadeIn(caption), run_time=0.5)
        self.play(*[ReplacementTransform(second[k], final[k]) for k in final], run_time=1.2)
        # A completed replacement leaves the targets as the live objects.
        assert all(p in self.mobjects for p in final.values())
        self.wait(2)
