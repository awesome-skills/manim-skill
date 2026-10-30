"""
State diagram animation patterns for technical blogs.

Run with: manim -pql state_diagram.py SimpleStates
"""

from manim import *
import numpy as np


def make_state(label, color=BLUE, radius=0.6):
    """Create a state circle with label."""
    circle = Circle(radius=radius, color=color, fill_opacity=0.3)
    text = Text(label, font_size=18)
    text.move_to(circle)
    return VGroup(circle, text)


def make_indexed_state(label, index, color=BLUE):
    """Create a state with an index label above."""
    state = make_state(label, color)
    idx = Text(str(index), font_size=14, color=GRAY)
    idx.next_to(state, UP, buff=0.15)
    return VGroup(state, idx)


class SimpleStates(Scene):
    """Basic state transition: A → B → C"""

    def construct(self):
        # Create states
        state_a = make_state("A", GREEN)
        state_b = make_state("B", BLUE)
        state_c = make_state("C", PURPLE)

        states = VGroup(state_a, state_b, state_c)
        states.arrange(RIGHT, buff=2)

        # Arrows
        arrow_ab = Arrow(state_a.get_right(), state_b.get_left(), buff=0.1, color=GRAY)
        arrow_bc = Arrow(state_b.get_right(), state_c.get_left(), buff=0.1, color=GRAY)

        # Show states
        self.play(*[FadeIn(s) for s in states])
        self.play(Create(arrow_ab), Create(arrow_bc))

        # Active indicator
        indicator = Circle(color=YELLOW, radius=0.75, stroke_width=3)
        indicator.move_to(state_a)

        self.play(FadeIn(indicator))
        self.wait(0.3)

        # Transition through states
        self.play(indicator.animate.move_to(state_b), run_time=0.6)
        self.play(Indicate(state_b, color=YELLOW), run_time=0.4)

        self.play(indicator.animate.move_to(state_c), run_time=0.6)
        self.play(Indicate(state_c, color=YELLOW), run_time=0.4)

        self.wait(1)


class StateWithLabels(Scene):
    """An event trace shows a retry without leaving the Loading state."""

    def construct(self):
        paper, ink, quiet = "#F2EEE6", "#253A4A", "#84949A"
        blue, amber = "#326EA8", "#A36725"
        self.camera.background_color = paper

        def label(words, size=30, color=ink):
            return Text(words, font="sans-serif", warn_missing_font=False,
                        font_size=size, color=color)

        def state(words, x):
            circle = Circle(radius=.9, stroke_color=quiet, stroke_width=2,
                            fill_color=paper, fill_opacity=1).move_to([x, -.4, 0])
            return VGroup(circle, label(words, 31).move_to(circle))

        heading = label("A retry can keep the same state.", 44).move_to([-6.1, 3, 0], aligned_edge=LEFT)
        self.add(heading)
        idle, loading, ready = state("Idle", -4), state("Loading", 0), state("Ready", 4)
        start_arrow = Arrow(idle.get_right(), loading.get_left(), buff=.13, color=quiet, stroke_width=2)
        finish_arrow = Arrow(loading.get_right(), ready.get_left(), buff=.13, color=quiet, stroke_width=2)
        start_label = label("start", 28).next_to(start_arrow, UP, buff=.18)
        finish_label = label("done", 28).next_to(finish_arrow, UP, buff=.18)
        # Keep a path without an arrow tip for sampling; add a separate display tip.
        loop_path = CubicBezier(loading[0].point_at_angle(PI/4),
                                [1.8, 1.8, 0], [-1.8, 1.8, 0],
                                loading[0].point_at_angle(3*PI/4))
        tip_direction = normalize(loop_path.get_end() - np.array([-1.8, 1.8, 0]))
        tip = Arrow(loop_path.get_end() - .2*tip_direction, loop_path.get_end(),
                    buff=0, color=amber, stroke_width=0, tip_length=.13,
                    max_tip_length_to_length_ratio=1)
        retry_arc = VGroup(loop_path.copy().set_stroke(amber, width=3), tip)
        retry_label = label("retry", 28, amber).move_to([0, 1.75, 0])
        self.play(FadeIn(idle), FadeIn(loading), FadeIn(ready),
                  GrowArrow(start_arrow), GrowArrow(finish_arrow), Create(retry_arc),
                  FadeIn(start_label), FadeIn(finish_label), FadeIn(retry_label), run_time=1)
        indicator = Circle(radius=1.02, color=blue, stroke_width=3).move_to(idle)
        current = label("Current state: Idle", 34).move_to([0, -2.05, 0])
        self.play(FadeIn(indicator), FadeIn(current), run_time=.4)
        self.wait(1)

        for event, path, destination, color in [
            ("start", start_arrow, loading, blue),
            ("retry", loop_path, loading, amber),
            ("done", finish_arrow, ready, blue),
        ]:
            self.next_section(event)
            event_text = label("Event: " + event, 31, color).move_to([0, -2.85, 0])
            self.play(FadeIn(event_text), run_time=.3)
            self.wait(.5)
            marker = Dot(path.get_start(), radius=.09, color=color)
            self.play(FadeIn(marker), run_time=.15)
            self.play(MoveAlongPath(marker, path), run_time=1.5 if event == "retry" else 1.1)
            self.play(FadeOut(marker), run_time=.15)
            if event != "retry":
                self.play(FadeOut(indicator), FadeOut(current), run_time=.2)
                indicator.move_to(destination)
                current = label("Current state: " + ("Loading" if event == "start" else "Ready"), 34).move_to([0, -2.05, 0])
                self.play(FadeIn(indicator), FadeIn(current), run_time=.25)
            else:
                # The active ring and current-state text deliberately remain unchanged.
                self.play(Indicate(retry_label, color=amber, scale_factor=1.08), run_time=.35)
            self.wait(.9)
            self.play(FadeOut(event_text), run_time=.2)
        conclusion = label("Retry kept Loading active.", 29).move_to([0, -2.85, 0])
        self.play(FadeIn(conclusion), run_time=.4)
        self.wait(2)


class LinkedListMismatch(Scene):
    """Position-based state identity breaks when a slot is skipped."""

    def construct(self):
        first = VGroup(
            make_indexed_state("name", 0, GREEN),
            make_indexed_state("age", 1, GREEN),
            make_indexed_state("effect", 2, PURPLE),
        )
        second = VGroup(
            make_indexed_state("age", 0, ORANGE),
            make_indexed_state("effect", 1, ORANGE),
        )
        for i, state in enumerate(first):
            state.move_to([3 * (i - 1), 1.8, 0])
        for i, state in enumerate(second):
            state.move_to([3 * (i - 1), -2.1, 0])

        first_title = Text("Render 1", font_size=26).to_edge(UP, buff=0.35)
        second_title = Text("Render 2: skip name", font_size=24, color=ORANGE)
        second_title.to_edge(LEFT, buff=0.5).set_y(-0.9)
        first_arrows = VGroup(*[
            Arrow(first[i][0].get_right(), first[i + 1][0].get_left(), buff=0.1, color=GRAY)
            for i in range(2)
        ])
        second_arrow = Arrow(second[0][0].get_right(), second[1][0].get_left(), buff=0.1, color=GRAY)
        self.play(FadeIn(first_title), *[FadeIn(state) for state in first])
        self.play(*[GrowArrow(arrow) for arrow in first_arrows])
        self.wait(0.5)
        self.play(FadeIn(second_title), *[FadeIn(state) for state in second], GrowArrow(second_arrow))

        matches = VGroup(*[
            DashedLine(first[i][0].get_bottom(), second[i][0].get_top(), color=RED)
            for i in range(2)
        ])
        errors = VGroup(
            Text("slot 0: name → age", font_size=22, color=RED).next_to(matches[0], LEFT, buff=0.2),
            Text("slot 1: age → effect", font_size=22, color=RED).next_to(matches[1], RIGHT, buff=0.2),
        )
        lost = Text("slot 2: no match", font_size=22, color=RED).move_to([3, -0.9, 0])
        lost_arrow = Arrow(first[2][0].get_bottom(), lost.get_top(), buff=0.15, color=RED)
        self.play(*[Create(line) for line in matches], FadeIn(errors))
        self.play(GrowArrow(lost_arrow), FadeIn(lost))
        self.wait(1.5)


class CyclicStates(Scene):
    """State machine with cycle."""

    def construct(self):
        # States in a triangle
        state_a = make_state("Init", GREEN).shift(UP * 1.5)
        state_b = make_state("Run", BLUE).shift(DOWN * 0.5 + LEFT * 2)
        state_c = make_state("Stop", PURPLE).shift(DOWN * 0.5 + RIGHT * 2)

        # Curved arrows for cycle
        ab_arrow = CurvedArrow(state_a.get_bottom() + LEFT * 0.3, state_b.get_top(), angle=-0.3)
        bc_arrow = CurvedArrow(state_b.get_right(), state_c.get_left(), angle=-0.3)
        ca_arrow = CurvedArrow(state_c.get_top() + RIGHT * 0.3, state_a.get_bottom() + RIGHT * 0.3, angle=-0.5)

        # Labels
        ab_label = Text("start", font_size=12).next_to(ab_arrow, LEFT, buff=0.05)
        bc_label = Text("finish", font_size=12).next_to(bc_arrow, DOWN, buff=0.05)
        ca_label = Text("reset", font_size=12).next_to(ca_arrow, RIGHT, buff=0.05)

        # Build
        self.play(FadeIn(state_a), FadeIn(state_b), FadeIn(state_c))
        self.play(
            Create(ab_arrow), FadeIn(ab_label),
            Create(bc_arrow), FadeIn(bc_label),
            Create(ca_arrow), FadeIn(ca_label)
        )

        # Animate cycle
        dot = Dot(color=YELLOW, radius=0.1).move_to(state_a[0].get_bottom() + UP * 0.18)
        self.play(FadeIn(dot))

        # Cycle through
        for _ in range(2):
            self.play(dot.animate.move_to(ab_arrow.get_start()), run_time=0.2)
            self.play(MoveAlongPath(dot, ab_arrow.copy()), run_time=0.5)
            self.play(dot.animate.move_to(state_b[0].get_bottom() + UP * 0.18), run_time=0.2)
            self.wait(0.2)

            self.play(dot.animate.move_to(bc_arrow.get_start()), run_time=0.2)
            self.play(MoveAlongPath(dot, bc_arrow.copy()), run_time=0.5)
            self.play(dot.animate.move_to(state_c[0].get_bottom() + UP * 0.18), run_time=0.2)
            self.wait(0.2)

            self.play(dot.animate.move_to(ca_arrow.get_start()), run_time=0.2)
            self.play(MoveAlongPath(dot, ca_arrow.copy()), run_time=0.5)
            self.play(dot.animate.move_to(state_a[0].get_bottom() + UP * 0.18), run_time=0.2)
            self.wait(0.2)

        self.wait(1)
