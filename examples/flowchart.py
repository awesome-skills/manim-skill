"""
Flowchart animation patterns for technical blogs.

Run with: manim -pql flowchart.py SimpleFlow
"""

from manim import *


def make_node(label, color=BLUE, width=2, height=1):
    """Create a labeled flowchart node."""
    rect = RoundedRectangle(
        width=width, height=height, corner_radius=0.15,
        fill_color=color, fill_opacity=0.3,
        stroke_color=color, stroke_width=2
    )
    text = Text(label, font_size=20)
    text.move_to(rect)
    return VGroup(rect, text)


def make_diamond(label, color=YELLOW):
    """Create a decision diamond."""
    diamond = Square(side_length=1.2, color=color, fill_opacity=0.3)
    diamond.rotate(PI / 4)
    text = Text(label, font_size=18)
    text.move_to(diamond)
    return VGroup(diamond, text)


class SimpleFlow(Scene):
    """Linear flowchart: Input → Process → Output"""

    def construct(self):
        # Create nodes
        input_node = make_node("Input", GREEN)
        process_node = make_node("Process", BLUE)
        output_node = make_node("Output", PURPLE)

        # Arrange horizontally
        nodes = VGroup(input_node, process_node, output_node)
        nodes.arrange(RIGHT, buff=1.5)

        # Create arrows
        arrow1 = Arrow(
            input_node.get_right(), process_node.get_left(),
            buff=0.1, color=GRAY
        )
        arrow2 = Arrow(
            process_node.get_right(), output_node.get_left(),
            buff=0.1, color=GRAY
        )

        # Animate construction
        self.play(GrowFromCenter(input_node))
        self.play(GrowArrow(arrow1), GrowFromCenter(process_node))
        self.play(GrowArrow(arrow2), GrowFromCenter(output_node))
        self.wait(1)


class BranchingFlow(Scene):
    """Flowchart with decision branch."""

    def construct(self):
        # Start node
        start = make_node("Request", GREEN).shift(LEFT * 4)

        # Decision
        decision = make_diamond("Valid?").shift(LEFT * 1)

        # Branches
        yes_node = make_node("Process", BLUE).shift(RIGHT * 2 + UP * 1.5)
        no_node = make_node("Error", RED).shift(RIGHT * 2 + DOWN * 1.5)

        # End node
        end_node = make_node("Response", PURPLE).shift(RIGHT * 5)

        # Arrows
        start_arrow = Arrow(start.get_right(), decision.get_left(), buff=0.1, color=GRAY)

        yes_arrow = Arrow(
            decision.get_corner(UR), yes_node.get_left(),
            buff=0.1, color=GREEN
        )
        no_arrow = Arrow(
            decision.get_corner(DR), no_node.get_left(),
            buff=0.1, color=RED
        )

        yes_to_end = Arrow(yes_node.get_right(), end_node.get_left() + UP * 0.3, buff=0.1, color=GRAY)
        no_to_end = Arrow(no_node.get_right(), end_node.get_left() + DOWN * 0.3, buff=0.1, color=GRAY)

        # Labels
        yes_label = Text("Yes", font_size=14, color=GREEN).next_to(yes_arrow, UL, buff=0.05)
        no_label = Text("No", font_size=14, color=RED).next_to(no_arrow, DL, buff=0.05)

        # Animate
        self.play(GrowFromCenter(start))
        self.play(GrowArrow(start_arrow), GrowFromCenter(decision))
        self.play(
            GrowArrow(yes_arrow), FadeIn(yes_label), GrowFromCenter(yes_node),
            GrowArrow(no_arrow), FadeIn(no_label), GrowFromCenter(no_node)
        )
        self.play(GrowArrow(yes_to_end), GrowArrow(no_to_end), GrowFromCenter(end_node))
        self.wait(1)


class VerticalFlow(Scene):
    """Vertical flowchart (top to bottom)."""

    def construct(self):
        # Create vertical flow
        steps = ["Start", "Step 1", "Step 2", "Step 3", "End"]
        colors = [GREEN, BLUE, BLUE, BLUE, PURPLE]

        nodes = VGroup()
        for step, color in zip(steps, colors):
            nodes.add(make_node(step, color, width=2.5, height=0.8))

        nodes.arrange(DOWN, buff=0.8)

        # Create arrows
        arrows = VGroup()
        for i in range(len(nodes) - 1):
            arr = Arrow(
                nodes[i].get_bottom(),
                nodes[i + 1].get_top(),
                buff=0.1, color=GRAY
            )
            arrows.add(arr)

        # Animate with stagger
        for i, node in enumerate(nodes):
            self.play(GrowFromCenter(node), run_time=0.4)
            if i < len(arrows):
                self.play(GrowArrow(arrows[i]), run_time=0.3)

        self.wait(1)


class ProcessHighlight(Scene):
    """Flowchart with animated process indicator."""

    def construct(self):
        # Create nodes
        steps = ["Fetch", "Parse", "Transform", "Save"]
        nodes = VGroup(*[make_node(s, BLUE) for s in steps])
        nodes.arrange(RIGHT, buff=1.2)

        # Create arrows
        arrows = VGroup()
        for i in range(len(nodes) - 1):
            arr = Arrow(
                nodes[i].get_right(), nodes[i + 1].get_left(),
                buff=0.1, color=GRAY
            )
            arrows.add(arr)

        # Show all
        self.play(
            *[FadeIn(n) for n in nodes],
            *[GrowArrow(a) for a in arrows]
        )
        self.wait(0.5)

        # Animate progress through each step
        for i, node in enumerate(nodes):
            # Highlight current
            self.play(
                node[0].animate.set_fill(GREEN, opacity=0.5),
                node[0].animate.set_stroke(GREEN),
                run_time=0.4
            )
            self.wait(0.3)

            # Dim after processing
            if i < len(nodes) - 1:
                self.play(
                    node[0].animate.set_fill(GRAY, opacity=0.2),
                    node[0].animate.set_stroke(GRAY),
                    run_time=0.2
                )

        self.wait(1)
