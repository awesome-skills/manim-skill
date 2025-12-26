# Manim Advanced Topics Reference

Advanced features including camera control, 3D scenes, dynamic animations, and configuration.

## Camera Control

### MovingCameraScene

Scene with a movable camera that can pan and zoom.

```python
from manim import *

class CameraDemo(MovingCameraScene):
    def construct(self):
        square = Square().shift(LEFT * 3)
        circle = Circle().shift(RIGHT * 3)
        self.add(square, circle)

        # Zoom to square
        self.play(
            self.camera.frame.animate.move_to(square).set(width=square.width * 2)
        )
        self.wait(0.5)

        # Pan to circle
        self.play(
            self.camera.frame.animate.move_to(circle).set(width=circle.width * 2)
        )
        self.wait(0.5)

        # Reset to full view
        self.play(self.camera.frame.animate.move_to(ORIGIN).set(width=14))
```

### Save and Restore Camera State

```python
class CameraSaveRestore(MovingCameraScene):
    def construct(self):
        self.camera.frame.save_state()

        # Zoom in
        self.play(self.camera.frame.animate.scale(0.5).move_to(LEFT * 2))
        self.wait()

        # Restore original view
        self.play(Restore(self.camera.frame))
```

### Auto Zoom

```python
# Automatically zoom to fit mobjects
self.camera.auto_zoom([mob1, mob2, mob3], margin=0.5)
```

### ZoomedScene (Picture-in-Picture)

For displaying a zoomed portion while showing the full scene.

```python
from manim import *

class ZoomDemo(ZoomedScene):
    def construct(self):
        dot = Dot()
        self.add(dot)

        # Activate zoom
        self.activate_zooming()
        self.play(self.zoomed_camera.frame.animate.move_to(dot))
```

## 3D Scenes

### ThreeDScene Basics

```python
from manim import *

class ThreeD(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes()
        sphere = Sphere(radius=1, color=BLUE)

        # Set initial camera orientation
        self.set_camera_orientation(phi=60 * DEGREES, theta=-45 * DEGREES)

        self.add(axes, sphere)
        self.wait()
```

### Camera Methods

```python
# Set camera orientation
self.set_camera_orientation(
    phi=60 * DEGREES,    # Polar angle (0=top, 90=side)
    theta=-45 * DEGREES, # Azimuthal angle (rotation around Z)
    gamma=0,             # Roll angle
    zoom=1,
)

# Animate camera movement
self.move_camera(phi=30 * DEGREES, theta=0, run_time=2)

# Continuous rotation
self.begin_ambient_camera_rotation(rate=0.1)  # radians per second
# ... animations ...
self.stop_ambient_camera_rotation()

# 3D illusion rotation
self.begin_3dillusion_camera_rotation()
```

### Fixed Elements

Keep elements fixed relative to camera (like HUD).

```python
# Fixed in frame (doesn't rotate with camera)
label = Text("Fixed Label")
self.add_fixed_in_frame_mobjects(label)
label.to_corner(UL)

# Fixed orientation (moves but doesn't tilt)
self.add_fixed_orientation_mobjects(another_label)
```

## ValueTracker and Updaters

### ValueTracker Basics

Animate a numeric value that other objects can track.

```python
from manim import *

class ValueTrackerDemo(Scene):
    def construct(self):
        tracker = ValueTracker(0)

        # Number display that follows tracker
        number = DecimalNumber(0).add_updater(
            lambda m: m.set_value(tracker.get_value())
        )

        self.add(number)
        self.play(tracker.animate.set_value(10), run_time=3)
```

### always_redraw

Continuously regenerate a mobject.

```python
class AlwaysRedrawDemo(Scene):
    def construct(self):
        tracker = ValueTracker(0)

        # Line that always connects origin to tracked point
        line = always_redraw(
            lambda: Line(ORIGIN, RIGHT * tracker.get_value(), color=BLUE)
        )

        self.add(line)
        self.play(tracker.animate.set_value(3), run_time=2)
```

### add_updater

Add custom update functions to mobjects.

```python
class UpdaterDemo(Scene):
    def construct(self):
        dot = Dot()
        label = Text("Follow").next_to(dot, UP)

        # Label always follows dot
        label.add_updater(lambda m: m.next_to(dot, UP))

        self.add(dot, label)
        self.play(dot.animate.shift(RIGHT * 3))

        # Remove updater when done
        label.clear_updaters()
```

### Time-based Updaters

```python
def update_func(mob, dt):
    """dt = time since last frame"""
    mob.rotate(dt * PI)  # Rotate continuously

circle.add_updater(update_func)
```

### ComplexValueTracker

For 2D motion tracking.

```python
tracker = ComplexValueTracker(complex(0, 0))
dot = Dot()
dot.add_updater(lambda m: m.move_to([tracker.get_value().real, tracker.get_value().imag, 0]))

self.play(tracker.animate.set_value(complex(3, 2)))
```

## MarkupText

HTML-like text formatting (alternative to Text with t2c).

```python
from manim import *

class MarkupDemo(Scene):
    def construct(self):
        # Basic formatting
        text = MarkupText(
            '<b>Bold</b> and <i>italic</i> and <u>underline</u>'
        )

        # Colors
        text2 = MarkupText(
            '<span foreground="red">Red</span> and <span foreground="#00FF00">Green</span>'
        )

        # Font mixing
        text3 = MarkupText(
            'Normal <span font_family="monospace">monospace</span> text'
        )

        # Size
        text4 = MarkupText(
            '<big>Big</big> normal <small>small</small>'
        )

        # Subscript/superscript
        text5 = MarkupText(
            'H<sub>2</sub>O and x<sup>2</sup>'
        )
```

**When to use MarkupText over Text:**
- Inline font mixing
- Complex nested styling
- Avoiding ligature issues with colors

## Configuration

### manim.cfg File

Create `manim.cfg` in your project directory:

```ini
[CLI]
# Quality
quality = low_quality

# Output
output_file = my_animation
format = gif

# Styling
background_color = WHITE

# Frame
frame_rate = 30
pixel_height = 1080
pixel_width = 1920
```

### Programmatic Configuration

```python
from manim import *

# Set config before scene class
config.background_color = WHITE
config.frame_rate = 60
config.pixel_height = 1080
config.pixel_width = 1920

class MyScene(Scene):
    def construct(self):
        # Access config
        print(config.frame_width)
        print(config.frame_height)
```

### Per-Scene Configuration

```python
from manim import *

class HighQualityScene(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        config.pixel_height = 2160
        config.pixel_width = 3840
```

## Debugging Tips

### Quick Preview

```bash
# Last frame only (fastest)
manim -pql -s scene.py SceneName

# Specific animations
manim -pql -n 2,5 scene.py SceneName  # Animations 2-5 only

# Dry run (no output)
manim --dry_run scene.py SceneName
```

### Verbose Output

```bash
manim -v DEBUG scene.py SceneName
```

### Common Issues

**Scene class not found:**
- Check spelling of class name
- Ensure file is saved

**LaTeX errors:**
- Test LaTeX expressions outside Manim first
- Check for missing packages
- Use raw strings: `r"\frac{a}{b}"`

**Slow rendering:**
- Use `-ql` during development
- Prefer `Text` over `Tex` when possible
- Check for complex shapes with many points

**Memory issues:**
- Split long scenes into multiple shorter scenes
- Clear unused mobjects: `self.remove(mob)`

### Caching

Manim caches partial renders in `media/videos/.../partial_movie_files/`.

```bash
# Disable cache
manim --disable_caching scene.py SceneName

# Clear cache
manim --flush_cache scene.py SceneName
```

## Special Scene Types Summary

| Scene Type | Use Case |
|------------|----------|
| `Scene` | Default 2D animations |
| `MovingCameraScene` | Pan and zoom |
| `ZoomedScene` | Picture-in-picture zoom |
| `ThreeDScene` | 3D animations |
| `VectorScene` | Vector field visualizations |

## v0.19 New Features

### New Mobjects
- `ConvexHull`, `ConvexHull3D`
- `Label`, `LabeledPolygram`

### New Color Methods
```python
color = RED
darker = color.darker()
lighter = color.lighter()
contrasting = color.contrasting()
```

### Coordinate Shorthand
```python
# @ shorthand for coords_to_point and point_to_coords
point = axes @ (2, 3)       # Same as axes.c2p(2, 3)
coords = axes @ point       # Same as axes.p2c(point)
```

### Add Animation
```python
# Instant add without animation (run_time=0)
self.play(Add(mobject))
```
