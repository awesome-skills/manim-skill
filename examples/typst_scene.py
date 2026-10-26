"""Optional Typst formula example. Install with: uv sync --extra typst.

Render: uv run python -m manim render -ql examples/typst_scene.py TypstFormula
"""
from manim import DOWN, FadeIn, MathTypst, Scene, Typst, VGroup


class TypstFormula(Scene):
    def construct(self):
        title = Typst("Sum of consecutive integers", font_size=36)
        formula = MathTypst("sum_(k=1)^n k = (n(n+1))/2", font_size=48)
        VGroup(title, formula).arrange(DOWN, buff=0.7)
        self.play(FadeIn(title))
        self.play(FadeIn(formula))
        self.wait(1)
