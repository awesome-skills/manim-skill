"""
State diagram animation patterns for technical blogs.

Run with: manim -pql state_diagram.py SimpleStates
"""

from manim import *


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
        indicator = Dot(color=YELLOW, radius=0.12)
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
    """State transitions with labeled arrows."""

    def construct(self):
        # States
        idle = make_state("Idle", GREEN).shift(LEFT * 3)
        loading = make_state("Loading", BLUE)
        ready = make_state("Ready", PURPLE).shift(RIGHT * 3)

        # Arrows with labels
        start_arrow = Arrow(idle.get_right(), loading.get_left(), buff=0.1)
        start_label = Text("start", font_size=14).next_to(start_arrow, UP, buff=0.05)

        finish_arrow = Arrow(loading.get_right(), ready.get_left(), buff=0.1)
        finish_label = Text("done", font_size=14).next_to(finish_arrow, UP, buff=0.05)

        # Self-loop for retry
        retry_arc = Arc(radius=0.4, start_angle=PI/4, angle=3*PI/2, color=ORANGE)
        retry_arc.next_to(loading, UP, buff=0.1)
        retry_label = Text("retry", font_size=12, color=ORANGE).next_to(retry_arc, UP, buff=0.05)

        # Build
        self.play(FadeIn(idle))
        self.play(GrowArrow(start_arrow), FadeIn(start_label), FadeIn(loading))
        self.play(Create(retry_arc), FadeIn(retry_label))
        self.play(GrowArrow(finish_arrow), FadeIn(finish_label), FadeIn(ready))
        self.wait(1)


class LinkedListMismatch(Scene):
    """
    Visualize linked list state mismatch (like React Hooks).
    Shows correct matching vs. broken matching when order changes.
    """

    def construct(self):
        # === Render 1 ===
        r1_label = Text("Render 1", font_size=20, color=GRAY)
        r1_label.to_edge(UP, buff=0.8).shift(LEFT * 4)

        r1_states = VGroup(
            make_indexed_state("name", 0, GREEN),
            make_indexed_state("age", 1, GREEN),
            make_indexed_state("effect", 2, PURPLE)
        ).arrange(RIGHT, buff=1)
        r1_states.next_to(r1_label, DOWN, buff=0.5).shift(RIGHT * 2)

        # Arrows in list
        r1_arrows = VGroup(
            Arrow(r1_states[0].get_right(), r1_states[1].get_left(), buff=0.1, color=GRAY),
            Arrow(r1_states[1].get_right(), r1_states[2].get_left(), buff=0.1, color=GRAY)
        )

        self.play(FadeIn(r1_label))
        self.play(*[GrowFromCenter(s) for s in r1_states])
        self.play(*[Create(a) for a in r1_arrows])
        self.wait(0.5)

        # === Render 2 (broken - skipped name) ===
        r2_label = Text("Render 2 (skip name)", font_size=20, color=RED)
        r2_label.shift(DOWN * 1.5 + LEFT * 3)

        r2_states = VGroup(
            make_indexed_state("age", 0, ORANGE),
            make_indexed_state("effect", 1, ORANGE)
        ).arrange(RIGHT, buff=1)
        r2_states.next_to(r2_label, DOWN, buff=0.5).shift(RIGHT * 2)

        r2_arrow = Arrow(r2_states[0].get_right(), r2_states[1].get_left(), buff=0.1, color=GRAY)

        self.play(FadeIn(r2_label))
        self.play(*[GrowFromCenter(s) for s in r2_states])
        self.play(Create(r2_arrow))

        # Wrong matching lines
        wrong_match_1 = DashedLine(
            r1_states[0].get_bottom(), r2_states[0].get_top(),
            color=RED, dash_length=0.1
        )
        wrong_match_2 = DashedLine(
            r1_states[1].get_bottom(), r2_states[1].get_top(),
            color=RED, dash_length=0.1
        )

        x1 = Text("✗", font_size=24, color=RED)
        x1.move_to((r1_states[0].get_center() + r2_states[0].get_center()) / 2 + RIGHT * 0.5)
        x2 = Text("✗", font_size=24, color=RED)
        x2.move_to((r1_states[1].get_center() + r2_states[1].get_center()) / 2 + RIGHT * 0.5)

        err1 = Text("name→age", font_size=12, color=RED).next_to(x1, RIGHT, buff=0.1)
        err2 = Text("age→effect", font_size=12, color=RED).next_to(x2, RIGHT, buff=0.1)

        self.play(Create(wrong_match_1), Create(wrong_match_2))
        self.play(FadeIn(x1, scale=1.5), FadeIn(x2, scale=1.5))
        self.play(FadeIn(err1), FadeIn(err2))

        # Lost state
        lost = Text("effect lost!", font_size=16, color=RED)
        lost.next_to(r1_states[2], DOWN, buff=1.2)
        lost_arrow = Arrow(r1_states[2].get_bottom(), lost.get_top(), buff=0.1, color=RED)

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
        dot = Dot(color=YELLOW, radius=0.1).move_to(state_a)
        self.play(FadeIn(dot))

        # Cycle through
        for _ in range(2):
            self.play(MoveAlongPath(dot, ab_arrow.copy()), run_time=0.5)
            dot.move_to(state_b)
            self.wait(0.2)

            self.play(MoveAlongPath(dot, bc_arrow.copy()), run_time=0.5)
            dot.move_to(state_c)
            self.wait(0.2)

            self.play(MoveAlongPath(dot, ca_arrow.copy()), run_time=0.5)
            dot.move_to(state_a)
            self.wait(0.2)

        self.wait(1)
