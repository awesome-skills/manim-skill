# Manim Animations Reference

Complete reference for Manim Community Edition animations and timing control.

## Creation Animations

### Create

Draw the stroke of a Mobject.

```python
self.play(Create(circle))
self.play(Create(square, run_time=2))

# Reverse: Uncreate
self.play(Uncreate(circle))
```

### Write

Write text or LaTeX character by character.

```python
self.play(Write(text))
self.play(Write(tex, run_time=3))

# Reverse: Unwrite
self.play(Unwrite(text))
```

### DrawBorderThenFill

Draw border first, then fill.

```python
self.play(DrawBorderThenFill(shape))
```

### GrowFromCenter

Grow from center point.

```python
self.play(GrowFromCenter(circle))
```

### GrowFromPoint

Grow from a specific point.

```python
self.play(GrowFromPoint(mobject, point=LEFT))
```

### GrowFromEdge

Grow from an edge.

```python
self.play(GrowFromEdge(mobject, edge=LEFT))
```

### GrowArrow

Specialized for arrows.

```python
self.play(GrowArrow(arrow))
```

### SpinInFromNothing

Spin in while growing.

```python
self.play(SpinInFromNothing(mobject))
```

## Fade Animations

### FadeIn

```python
self.play(FadeIn(mobject))

# With direction
self.play(FadeIn(mobject, shift=UP))
self.play(FadeIn(mobject, shift=RIGHT * 0.5))

# With scaling
self.play(FadeIn(mobject, scale=0.5))  # Grow while fading in

# Combined
self.play(FadeIn(mobject, shift=UP, scale=1.5))
```

### FadeOut

```python
self.play(FadeOut(mobject))

# With direction
self.play(FadeOut(mobject, shift=DOWN))

# With scaling
self.play(FadeOut(mobject, scale=0.5))  # Shrink while fading out
```

### FadeTransform

Fade between two mobjects.

```python
self.play(FadeTransform(old_mob, new_mob))
```

## Transform Animations

### Transform vs ReplacementTransform

| Animation | After Animation | Use Case |
|-----------|-----------------|----------|
| **Transform** | Original object morphs but keeps its reference | Chain multiple transforms on same object |
| **ReplacementTransform** | Original removed, target becomes active | Clean replacement, no leftover references |

### Transform

Morph one mobject into another. Original reference stays.

```python
self.play(Transform(square, circle))
# After: square looks like circle, but is still the square object
# Use square (not circle) for subsequent animations
```

### ReplacementTransform

Replace the original with the new one.

```python
self.play(ReplacementTransform(square, circle))
# After: circle is the active object, square is removed
# Use circle for subsequent animations
```

**Tip:** To avoid lingering references with ReplacementTransform, use `.copy()`:
```python
self.play(ReplacementTransform(obj1, obj2.copy()))
```

### TransformFromCopy

Transform a copy while keeping original.

```python
self.play(TransformFromCopy(original, target))
# Both original and target remain
```

### ClockwiseTransform / CounterclockwiseTransform

Transform with rotation direction.

```python
self.play(ClockwiseTransform(mob1, mob2))
self.play(CounterclockwiseTransform(mob1, mob2))
```

### MoveToTarget

Pre-define target state, then animate to it.

```python
circle = Circle()
circle.generate_target()
circle.target.shift(RIGHT * 2)
circle.target.scale(0.5)
circle.target.set_color(RED)

self.play(MoveToTarget(circle))
```

### TransformMatchingShapes

Match similar shapes between groups.

```python
text1 = Text("Hello")
text2 = Text("World")
self.play(TransformMatchingShapes(text1, text2))
```

### TransformMatchingTex

Match LaTeX components.

```python
eq1 = MathTex("a", "+", "b")
eq2 = MathTex("b", "+", "a")
self.play(TransformMatchingTex(eq1, eq2))
```

## Movement Animations

### Shift Animation (via .animate)

```python
self.play(mob.animate.shift(RIGHT * 2))
```

### MoveTo (via .animate)

```python
self.play(mob.animate.move_to(ORIGIN))
self.play(mob.animate.move_to(other_mob))  # Move to another object
```

### MoveAlongPath

Move along a curve.

```python
path = Arc(radius=2, angle=PI)
self.play(MoveAlongPath(mobject, path, run_time=2))
```

### Rotate

```python
self.play(Rotate(mobject, angle=PI/2))
self.play(Rotate(mobject, angle=PI, about_point=ORIGIN))
```

### Rotating

Continuous rotation.

```python
self.play(Rotating(mobject, radians=2*PI, run_time=2))
```

### Circumscribe

Draw attention by tracing around.

```python
self.play(Circumscribe(mobject, color=YELLOW))
```

## Indication Animations

### Indicate

Scale up and back with color.

```python
self.play(Indicate(mobject, color=RED))
```

### Flash

Brief bright flash.

```python
self.play(Flash(mobject, color=YELLOW, flash_radius=0.5))
```

### Wiggle

Shake the object.

```python
self.play(Wiggle(mobject, scale_value=1.2))
```

### FocusOn

Zoom focus effect.

```python
self.play(FocusOn(mobject))
```

### ShowPassingFlash

Flash traveling along a path.

```python
self.play(ShowPassingFlash(line.copy(), time_width=0.5))
```

### ApplyWave

Wave effect through mobject.

```python
self.play(ApplyWave(text))
```

## The .animate Syntax

Convert any mobject method into an animation.

### Basic Usage

```python
# Instead of instant change:
mob.shift(RIGHT)

# Animate the change:
self.play(mob.animate.shift(RIGHT))
```

### Chainable

```python
self.play(
    mob.animate
    .shift(RIGHT * 2)
    .scale(0.5)
    .set_color(BLUE)
    .rotate(PI/4)
)
```

### Common .animate Methods

```python
# Position
mob.animate.shift(direction)
mob.animate.move_to(point_or_mob)
mob.animate.next_to(other, direction)
mob.animate.align_to(other, direction)

# Size
mob.animate.scale(factor)
mob.animate.scale_to_fit_width(width)
mob.animate.scale_to_fit_height(height)
mob.animate.stretch(factor, dim)  # dim: 0=x, 1=y

# Rotation
mob.animate.rotate(angle)
mob.animate.rotate(angle, about_point=point)

# Appearance
mob.animate.set_color(color)
mob.animate.set_fill(color, opacity)
mob.animate.set_stroke(color, width)
mob.animate.set_opacity(value)

# Arrangement
mob.animate.arrange(direction)
mob.animate.arrange_in_grid(rows, cols)
```

## Animation Modifiers

### Run Time

```python
self.play(Create(mob), run_time=3)  # 3 seconds
```

### Rate Functions

Control animation timing curve. Rate functions define progress based on relative runtime.

```python
from manim import *

# Commonly used (exported, use directly)
self.play(Create(mob), rate_func=linear)           # Constant speed
self.play(Create(mob), rate_func=smooth)           # Default, smooth ease (sigmoid)
self.play(Create(mob), rate_func=rush_into)        # Slow start, fast end
self.play(Create(mob), rate_func=rush_from)        # Fast start, slow end
self.play(Create(mob), rate_func=there_and_back)   # Go and return (good for emphasis)
self.play(Create(mob), rate_func=wiggle)           # Wiggle motion
self.play(Create(mob), rate_func=double_smooth)    # Extra smooth

# Standard easing (need import)
from manim.utils import rate_functions
self.play(Create(mob), rate_func=rate_functions.ease_in_sine)
self.play(Create(mob), rate_func=rate_functions.ease_out_sine)
self.play(Create(mob), rate_func=rate_functions.ease_in_out_sine)
# Also: ease_in_quad, ease_out_quad, ease_in_cubic, etc.
# Full list: https://easings.net/
```

**Note:** Default rate_func varies by animation:
- `Write`: uses `linear`
- Most others: use `smooth`

### Lag Ratio

Stagger animations in a group.

```python
group = VGroup(*[Circle() for _ in range(5)])
self.play(Create(group, lag_ratio=0.5))  # Each starts as previous is 50% done
```

## Simultaneous Animations

### Multiple in One Play

```python
self.play(
    Create(circle),
    Write(text),
    FadeIn(arrow),
    run_time=2
)
```

### AnimationGroup

Base class for combining animations with `lag_ratio` control.

```python
from manim import AnimationGroup

# lag_ratio controls timing:
# 0 = all start together
# 1 = each starts when previous ends
# 0.5 = each starts when previous is 50% done
self.play(AnimationGroup(
    Create(circle),
    Write(text),
    FadeIn(arrow),
    lag_ratio=0.5
))

# Nested groups with different timings
self.play(AnimationGroup(
    AnimationGroup(FadeIn(a), FadeIn(b), lag_ratio=0),  # Simultaneous
    AnimationGroup(FadeIn(c), FadeIn(d), lag_ratio=1),  # Sequential
    lag_ratio=0.5
))
```

### LaggedStart

Same as `AnimationGroup` but with default `lag_ratio=0.05`.

```python
from manim import LaggedStart

self.play(LaggedStart(
    *[FadeIn(mob) for mob in group],
    lag_ratio=0.2  # Override default
))
```

### LaggedStartMap

Shorthand for applying the same animation to all items.

```python
from manim import LaggedStartMap

# Instead of: LaggedStart(*[FadeIn(m) for m in group])
self.play(LaggedStartMap(FadeIn, group))

# With animation kwargs
self.play(LaggedStartMap(FadeIn, group, shift=UP, lag_ratio=0.1))

# With Indicate
self.play(LaggedStartMap(Indicate, items, run_time=4, rate_func=linear))
```

### Succession

Sequential animations (like `AnimationGroup` with `lag_ratio=1`).

```python
from manim import Succession

# Each animation starts after the previous ends
self.play(Succession(
    Create(circle),
    Write(text),
    FadeIn(arrow)
))

# With run_time, the total time is divided among animations
self.play(Succession(
    Create(circle),
    Write(text),
    run_time=4  # 2 seconds each
))
```

## Timing Control

### Wait

```python
self.wait()       # Default 1 second
self.wait(2)      # 2 seconds
self.wait(0.5)    # Half second
```

### Add (No Animation)

Add without animation.

```python
self.add(mobject)
```

### Remove (No Animation)

Remove without animation.

```python
self.remove(mobject)
```

## Updaters

### Always Updating

```python
# Follow another object
label.add_updater(lambda m: m.next_to(circle, UP))

# Update based on time
def update_opacity(mob, dt):
    mob.set_opacity(mob.get_opacity() + dt * 0.1)
circle.add_updater(update_opacity)

# Remove updater
circle.clear_updaters()
```

### ValueTracker

Animate a value.

```python
tracker = ValueTracker(0)

number = DecimalNumber(0).add_updater(
    lambda m: m.set_value(tracker.get_value())
)

self.play(tracker.animate.set_value(10), run_time=3)
```

## Common Patterns

### Fade and Replace

```python
self.play(
    FadeOut(old_content),
    FadeIn(new_content)
)
```

### Transform with Emphasis

```python
self.play(Indicate(source))
self.wait(0.5)
self.play(Transform(source, target))
```

### Sequential Highlight

```python
for item in items:
    self.play(Indicate(item), run_time=0.5)
```

### Staged Appearance

```python
self.play(FadeIn(header))
self.wait(0.3)
self.play(LaggedStart(*[FadeIn(item, shift=LEFT) for item in items]))
```

### Save State and Restore

Save a mobject's state, modify it, then animate back to the saved state.

```python
# Save current state
circle = Circle(color=BLUE)
circle.save_state()

# Make changes
self.play(circle.animate.scale(2).set_color(RED).shift(RIGHT))
self.wait()

# Animate back to saved state
self.play(Restore(circle))
```

**Use cases:**
- Temporary highlighting then returning to original
- Comparison animations (before/after)
- Camera zoom and restore (with `self.camera.frame.save_state()`)

### ChangingDecimal

Animate a DecimalNumber through values based on a function.

```python
from manim import DecimalNumber, ChangingDecimal

num = DecimalNumber(0)
self.add(num)

# Function receives alpha (0 to 1 during animation)
self.play(
    ChangingDecimal(num, lambda alpha: alpha * 100),
    run_time=3
)
# num goes from 0 to 100 over 3 seconds
```
