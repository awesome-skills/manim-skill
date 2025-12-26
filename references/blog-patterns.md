# Manim Blog Animation Patterns

Common patterns for creating animations in technical blog posts.

## Philosophy

### Keep Animations Focused

Blog animations should:
- Illustrate ONE concept clearly
- Be short (5-15 seconds typically)
- Let surrounding text provide context
- Not include titles/explanations (text does that)

### Animation vs Static Image

Use animation when:
- Showing state changes or transitions
- Illustrating a process step by step
- Demonstrating cause and effect
- Visualizing data flow

Use static images when:
- Showing final state only
- Simple diagrams
- Reference/lookup content

## Flowchart Pattern

### Simple Linear Flow

```python
from manim import *

class LinearFlow(Scene):
    def construct(self):
        def make_node(label, color=BLUE):
            rect = RoundedRectangle(
                width=2, height=1, corner_radius=0.15,
                fill_color=color, fill_opacity=0.3,
                stroke_color=color
            )
            text = Text(label, font_size=20)
            text.move_to(rect)
            return VGroup(rect, text)

        # Create nodes
        nodes = VGroup(
            make_node("Input", GREEN),
            make_node("Process", BLUE),
            make_node("Output", PURPLE)
        ).arrange(RIGHT, buff=1.5)

        # Create arrows
        arrows = VGroup(
            Arrow(nodes[0].get_right(), nodes[1].get_left(), buff=0.1),
            Arrow(nodes[1].get_right(), nodes[2].get_left(), buff=0.1)
        )

        # Animate
        self.play(GrowFromCenter(nodes[0]))
        self.play(GrowArrow(arrows[0]), GrowFromCenter(nodes[1]))
        self.play(GrowArrow(arrows[1]), GrowFromCenter(nodes[2]))
        self.wait()
```

### Branching Flow

```python
class BranchingFlow(Scene):
    def construct(self):
        # Decision diamond
        decision = VGroup(
            Square(side_length=1.2, color=YELLOW).rotate(PI/4),
            Text("?", font_size=24)
        )

        yes_path = make_node("Success", GREEN).shift(RIGHT * 3 + UP * 1.5)
        no_path = make_node("Retry", RED).shift(RIGHT * 3 + DOWN * 1.5)

        yes_arrow = Arrow(decision.get_corner(UR), yes_path.get_left(), buff=0.1)
        no_arrow = Arrow(decision.get_corner(DR), no_path.get_left(), buff=0.1)

        yes_label = Text("Yes", font_size=16, color=GREEN).next_to(yes_arrow, UP, buff=0.1)
        no_label = Text("No", font_size=16, color=RED).next_to(no_arrow, DOWN, buff=0.1)

        self.play(Create(decision))
        self.play(
            GrowArrow(yes_arrow), FadeIn(yes_label), GrowFromCenter(yes_path),
            GrowArrow(no_arrow), FadeIn(no_label), GrowFromCenter(no_path)
        )
        self.wait()
```

## State Diagram Pattern

### State Transitions

```python
class StateTransition(Scene):
    def construct(self):
        def make_state(label, color=BLUE):
            circle = Circle(radius=0.6, color=color, fill_opacity=0.3)
            text = Text(label, font_size=18)
            text.move_to(circle)
            return VGroup(circle, text)

        # States
        state_a = make_state("A", GREEN).shift(LEFT * 3)
        state_b = make_state("B", BLUE)
        state_c = make_state("C", PURPLE).shift(RIGHT * 3)

        # Arrows
        ab_arrow = Arrow(state_a.get_right(), state_b.get_left(), buff=0.1)
        bc_arrow = Arrow(state_b.get_right(), state_c.get_left(), buff=0.1)

        # Indicator dot
        dot = Dot(color=YELLOW, radius=0.15)
        dot.move_to(state_a)

        self.play(FadeIn(state_a), FadeIn(state_b), FadeIn(state_c))
        self.play(Create(ab_arrow), Create(bc_arrow))
        self.play(FadeIn(dot))

        # Animate transition
        self.play(dot.animate.move_to(state_b), run_time=0.8)
        self.play(Indicate(state_b, color=YELLOW))
        self.play(dot.animate.move_to(state_c), run_time=0.8)
        self.wait()
```

## Linked List Pattern

### Data Structure Visualization

```python
class LinkedList(Scene):
    def construct(self):
        def make_list_node(value, color=BLUE):
            # Value box
            val_box = Rectangle(width=1, height=0.8, color=color)
            val_text = Text(str(value), font_size=20)
            val_text.move_to(val_box)

            # Pointer box
            ptr_box = Rectangle(width=0.4, height=0.8, color=color)
            ptr_box.next_to(val_box, RIGHT, buff=0)

            return VGroup(val_box, val_text, ptr_box)

        # Create nodes
        nodes = [make_list_node(i) for i in ["A", "B", "C"]]
        for i, node in enumerate(nodes):
            node.move_to(LEFT * 4 + RIGHT * i * 2.5)

        # Create arrows
        arrows = []
        for i in range(len(nodes) - 1):
            arr = Arrow(
                nodes[i][2].get_center(),
                nodes[i+1][0].get_left(),
                buff=0.1, color=GRAY
            )
            arrows.append(arr)

        # Null terminator
        null = Text("∅", font_size=24, color=GRAY)
        null.next_to(nodes[-1], RIGHT, buff=0.5)
        null_arrow = Arrow(nodes[-1][2].get_center(), null.get_left(), buff=0.1, color=GRAY)

        # Animate construction
        for i, node in enumerate(nodes):
            self.play(GrowFromCenter(node), run_time=0.5)
            if i < len(arrows):
                self.play(GrowArrow(arrows[i]), run_time=0.3)

        self.play(GrowArrow(null_arrow), FadeIn(null))
        self.wait()
```

## Comparison Pattern

### Before/After

```python
class BeforeAfter(Scene):
    def construct(self):
        # Before state
        before_label = Text("Before", font_size=24, color=GRAY)
        before_label.to_edge(UP + LEFT, buff=0.5)

        before_content = VGroup(
            Rectangle(width=3, height=2, color=RED, fill_opacity=0.3),
            Text("Broken", font_size=20, color=RED)
        )
        before_content[1].move_to(before_content[0])
        before_content.shift(LEFT * 3)

        # After state
        after_label = Text("After", font_size=24, color=GRAY)
        after_label.to_edge(UP + RIGHT, buff=0.5)

        after_content = VGroup(
            Rectangle(width=3, height=2, color=GREEN, fill_opacity=0.3),
            Text("Fixed", font_size=20, color=GREEN)
        )
        after_content[1].move_to(after_content[0])
        after_content.shift(RIGHT * 3)

        # Arrow between
        transform_arrow = Arrow(
            before_content.get_right(),
            after_content.get_left(),
            buff=0.3, color=WHITE
        )

        # Animate
        self.play(FadeIn(before_label), GrowFromCenter(before_content))
        self.wait(0.5)
        self.play(GrowArrow(transform_arrow))
        self.play(FadeIn(after_label), GrowFromCenter(after_content))
        self.wait()
```

## Data Matching Pattern

### Index-Based Matching (React Hooks Style)

```python
class IndexMatching(Scene):
    def construct(self):
        def make_slot(label, color):
            rect = RoundedRectangle(
                width=1.5, height=0.7, corner_radius=0.1,
                fill_color=color, fill_opacity=0.3, stroke_color=color
            )
            text = Text(label, font_size=16)
            text.move_to(rect)
            return VGroup(rect, text)

        # Row 1: First render
        r1_label = Text("Render 1", font_size=18, color=GRAY).shift(LEFT * 4 + UP * 1.5)
        r1_slots = VGroup(
            make_slot("A", BLUE),
            make_slot("B", BLUE),
            make_slot("C", PURPLE)
        ).arrange(RIGHT, buff=0.5).next_to(r1_label, RIGHT, buff=0.5)

        # Row 2: Matching render
        r2_label = Text("Render 2", font_size=18, color=GRAY).shift(LEFT * 4 + DOWN * 0.5)
        r2_slots = VGroup(
            make_slot("A", BLUE),
            make_slot("B", BLUE),
            make_slot("C", PURPLE)
        ).arrange(RIGHT, buff=0.5).next_to(r2_label, RIGHT, buff=0.5)

        # Match lines
        matches = VGroup()
        for i in range(3):
            line = DashedLine(
                r1_slots[i].get_bottom(),
                r2_slots[i].get_top(),
                color=GREEN, dash_length=0.1
            )
            matches.add(line)

        # Check marks
        checks = VGroup()
        for i in range(3):
            check = Text("✓", font_size=20, color=GREEN)
            check.move_to((r1_slots[i].get_center() + r2_slots[i].get_center()) / 2 + RIGHT * 0.4)
            checks.add(check)

        # Animate
        self.play(FadeIn(r1_label), *[GrowFromCenter(s) for s in r1_slots])
        self.wait(0.5)
        self.play(FadeIn(r2_label), *[GrowFromCenter(s) for s in r2_slots])
        self.play(*[Create(m) for m in matches])
        self.play(*[FadeIn(c, scale=1.3) for c in checks])
        self.wait()
```

## Process Animation Pattern

### Step-by-Step Process

```python
class StepProcess(Scene):
    def construct(self):
        steps = ["Parse", "Validate", "Transform", "Output"]

        nodes = VGroup()
        for i, step in enumerate(steps):
            node = VGroup(
                Circle(radius=0.5, color=BLUE, fill_opacity=0.3),
                Text(step, font_size=14)
            )
            node[1].move_to(node[0])
            nodes.add(node)

        nodes.arrange(RIGHT, buff=1.2)

        arrows = VGroup()
        for i in range(len(nodes) - 1):
            arr = Arrow(nodes[i].get_right(), nodes[i+1].get_left(), buff=0.1, color=GRAY)
            arrows.add(arr)

        # Build
        self.play(*[FadeIn(n) for n in nodes], *[GrowArrow(a) for a in arrows])
        self.wait(0.5)

        # Highlight progress
        for i, node in enumerate(nodes):
            self.play(
                node[0].animate.set_fill(GREEN, opacity=0.5),
                run_time=0.5
            )
            self.wait(0.3)

        self.wait()
```

## Error Visualization Pattern

### Highlighting Problems

```python
class ErrorHighlight(Scene):
    def construct(self):
        # Correct state
        correct = VGroup(
            RoundedRectangle(width=2, height=1, color=GREEN),
            Text("Valid", font_size=20)
        )
        correct[1].move_to(correct[0])
        correct.shift(LEFT * 3)

        # Error state
        error = VGroup(
            RoundedRectangle(width=2, height=1, color=RED),
            Text("Error", font_size=20)
        )
        error[1].move_to(error[0])
        error.shift(RIGHT * 3)

        # X mark
        cross = Cross(error, stroke_color=RED, stroke_width=6)

        # Arrow with label
        arrow = Arrow(correct.get_right(), error.get_left(), buff=0.3, color=RED)
        label = Text("breaks", font_size=16, color=RED)
        label.next_to(arrow, UP, buff=0.1)

        self.play(GrowFromCenter(correct))
        self.play(GrowArrow(arrow), FadeIn(label))
        self.play(GrowFromCenter(error))
        self.play(Create(cross))

        # Flash emphasis
        self.play(Flash(error, color=RED, flash_radius=0.8))
        self.wait()
```

## Tips for Blog Animations

### Export Settings

```bash
# For web embedding (good quality, small size)
manim -qm --format=gif scene.py SceneName

# For higher quality
manim -qh --format=gif scene.py SceneName
```

### Optimal Duration

- **5-8 seconds**: Simple concept, single transition
- **8-15 seconds**: Multi-step process, state changes
- **15-30 seconds**: Complex visualization (rare, split if possible)

### Looping Considerations

For GIFs that loop:
- End state should visually connect to start
- Or add pause at end before loop
- Consider adding subtle indicator of completion

### Color Accessibility

```python
# High contrast combinations
SUCCESS_BG = "#1a472a"   # Dark green
SUCCESS_FG = "#4ade80"   # Light green

ERROR_BG = "#4a1a1a"     # Dark red
ERROR_FG = "#f87171"     # Light red

NEUTRAL_BG = "#1a1a2e"   # Dark blue
NEUTRAL_FG = "#60a5fa"   # Light blue
```

### Reduce Visual Noise

- Use consistent colors across related elements
- Limit to 3-4 colors per animation
- Use opacity to create hierarchy
- Remove unnecessary decorations
