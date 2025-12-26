"""
Minimal Manim scene template.

Run with: manim -pql basic_scene.py BasicScene
"""

from manim import *


class BasicScene(Scene):
    """Minimal scene demonstrating core patterns."""

    def construct(self):
        # Create a simple shape
        circle = Circle(radius=1, color=BLUE, fill_opacity=0.5)

        # Add text
        label = Text("Hello Manim", font_size=36)
        label.next_to(circle, DOWN, buff=0.5)

        # Animate
        self.play(Create(circle))
        self.play(Write(label))
        self.wait(1)

        # Transform
        square = Square(side_length=2, color=RED, fill_opacity=0.5)
        self.play(Transform(circle, square))
        self.wait(1)


class CodeExample(Scene):
    """Scene with syntax-highlighted code."""

    def construct(self):
        # Note: Use code_string, not code (v0.19+)
        code = Code(
            code_string="""def greet(name):
    return f"Hello, {name}!"

print(greet("World"))""",
            language="python",
            background="rectangle",
            formatter_style="monokai",
        )
        code.scale(0.8)

        self.play(Create(code))
        self.wait(2)


class MathExample(Scene):
    """Scene with LaTeX math."""

    def construct(self):
        # Math equation
        equation = MathTex(r"E = mc^2", font_size=72)

        # More complex equation
        complex_eq = MathTex(
            r"\int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}",
            font_size=48
        )
        complex_eq.next_to(equation, DOWN, buff=1)

        self.play(Write(equation))
        self.wait(0.5)
        self.play(Write(complex_eq))
        self.wait(1)


class GraphExample(Scene):
    """Scene with function graph."""

    def construct(self):
        # Create axes
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-1, 9, 2],
            x_length=8,
            y_length=5,
            axis_config={"color": BLUE}
        )

        # Plot function
        graph = axes.plot(lambda x: x**2, color=WHITE)
        label = axes.get_graph_label(graph, label="x^2")

        # Coordinate labels
        x_label = axes.get_x_axis_label("x")
        y_label = axes.get_y_axis_label("y")

        self.play(Create(axes), Write(x_label), Write(y_label))
        self.play(Create(graph), Write(label))
        self.wait(1)
