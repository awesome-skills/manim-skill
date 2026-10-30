"""
Flowchart animation patterns for technical blogs.

Run with: manim -pql flowchart.py SimpleFlow
"""

from manim import *


def make_node(label, color=BLUE, width=2, height=1, font_size=20):
    """Create a labeled flowchart node."""
    rect = RoundedRectangle(
        width=width, height=height, corner_radius=0.15,
        fill_color=color, fill_opacity=0.3,
        stroke_color=color, stroke_width=2
    )
    text = Text(label, font_size=font_size)
    text.move_to(rect)
    return VGroup(rect, text)


def make_diamond(label, color=YELLOW, font_size=18):
    """Create a decision diamond."""
    diamond = Square(side_length=1.2, color=color, fill_opacity=0.3)
    diamond.rotate(PI / 4)
    text = Text(label, font_size=font_size)
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
    """Two example requests select mutually exclusive branches of a field check."""

    def construct(self):
        ground, ink, neutral = "#15212B", "#E9F1F0", "#59707B"
        accepted, rejected = "#6BC8A5", "#E5AD64"
        self.camera.background_color = ground

        def label(words, size=30, color=ink):
            return Text(words, font="sans-serif", warn_missing_font=False,
                        font_size=size, color=color)

        heading = label("One request. One branch.", 46).move_to([-6, 2.9, 0], aligned_edge=LEFT)
        subtitle = label("A small example: is the name field present?", 27, ink).move_to([-6, 2.1, 0], aligned_edge=LEFT)
        self.add(heading, subtitle)
        start = make_node("Request", neutral, width=2.1, font_size=29).move_to([-5.05, 0, 0])
        decision = make_diamond("Name?", neutral, font_size=26).move_to([-2.1, 0, 0])
        yes_node = make_node("Process", neutral, width=2.1, font_size=29).move_to([1, 1.1, 0])
        no_node = make_node("Reject", neutral, width=2.1, font_size=29).move_to([1, -1.1, 0])
        end_node = make_node("Reply", neutral, width=2.1, font_size=29).move_to([4.7, 0, 0])
        nodes = VGroup(start, decision, yes_node, no_node, end_node)
        for node, words in zip(nodes, ["Request", "Name?", "Process", "Reject", "Reply"]):
            node[1].become(label(words, 26 if node is decision else 29).move_to(node[0]))
        start_arrow = Arrow(start.get_right(), decision.get_left(), buff=.12, color=neutral, stroke_width=2)
        yes_arrow = Arrow(decision[0].get_top(), yes_node.get_left(), buff=.12, color=neutral, stroke_width=2)
        no_arrow = Arrow(decision[0].get_bottom(), no_node.get_left(), buff=.12, color=neutral, stroke_width=2)
        yes_to_end = Arrow(yes_node.get_right(), end_node.get_left()+UP*.24, buff=.12, color=neutral, stroke_width=2)
        no_to_end = Arrow(no_node.get_right(), end_node.get_left()+DOWN*.24, buff=.12, color=neutral, stroke_width=2)
        arrows = VGroup(start_arrow, yes_arrow, no_arrow, yes_to_end, no_to_end)
        yes_label = label("Yes", 27, accepted).move_to([-1.15, 1.43, 0])
        no_label = label("No", 27, rejected).move_to([-1.15, -1.43, 0])
        self.play(FadeIn(nodes), *[GrowArrow(a) for a in arrows], FadeIn(yes_label), FadeIn(no_label), run_time=1)
        self.wait(.7)

        def arrive(node, color):
            self.play(node[0].animate.set_stroke(color, width=3).set_fill(color, opacity=.16), run_time=.25)

        def travel(arrow, color):
            # The marker represents travel on a connector; processing occurs inside nodes.
            marker = Dot(arrow.get_start(), radius=.09, color=color)
            self.play(arrow.animate.set_color(color), FadeIn(marker), run_time=.15)
            self.play(MoveAlongPath(marker, arrow), run_time=.75)
            self.play(FadeOut(marker), run_time=.1)

        for index, record in enumerate([{"name": "Ada"}, {}]):
            self.next_section("complete_request" if index == 0 else "missing_name")
            has_name = bool(record.get("name"))
            color = accepted if has_name else rejected
            caption = label('A / name = "Ada"' if has_name else "B / name is missing", 34).move_to([0, -2.55, 0])
            self.play(FadeIn(caption), run_time=.35)
            self.wait(.7)
            arrive(start, color)
            travel(start_arrow, color)
            arrive(decision, color)
            self.wait(.5)
            outgoing, selected, returning = (yes_arrow, yes_node, yes_to_end) if has_name else (no_arrow, no_node, no_to_end)
            travel(outgoing, color)
            arrive(selected, color)
            self.wait(.5)
            travel(returning, color)
            arrive(end_node, color)
            outcome = label("200 / processed" if has_name else "400 / missing name", 29, color).move_to([4.7, -.95, 0])
            self.play(FadeIn(outcome), run_time=.3)
            self.wait(1.2)
            if index == 0:
                self.play(FadeOut(caption), FadeOut(outcome),
                          *[node[0].animate.set_stroke(neutral, width=2).set_fill(neutral, opacity=.3) for node in nodes],
                          *[arrow.animate.set_color(neutral) for arrow in arrows], run_time=.4)
        self.wait(.8)


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
                node[0].animate.set_fill(GREEN, opacity=0.5).set_stroke(GREEN),
                run_time=0.4
            )
            self.wait(0.3)

            # Dim after processing
            if i < len(nodes) - 1:
                self.play(
                    node[0].animate.set_fill(GRAY, opacity=0.2).set_stroke(GRAY),
                    run_time=0.2
                )

        self.wait(1)
