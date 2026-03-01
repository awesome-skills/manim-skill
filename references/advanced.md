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

### add_updater vs always_redraw

| Method | Behavior | Use Case |
|--------|----------|----------|
| **add_updater** | Modifies existing mobject in place | Simple property changes (position, color) |
| **always_redraw** | Recreates mobject from scratch each frame | Structure changes (Brace resize, Line endpoints) |

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

Create `manim.cfg` in the project directory:

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

## Scene Sections

Divide a scene into sections for separate video files or presentation systems.

```python
class MyScene(Scene):
    def construct(self):
        # First section (auto-created)
        self.play(Create(circle))

        # Create a new section
        self.next_section("intro")  # Named section
        self.play(Write(text))

        # Section with custom type (for presentation systems)
        self.next_section(section_type="loop")
        self.play(Indicate(text))

        # Skip rendering a section (code still runs)
        self.next_section(skip_animations=True)
        self.play(FadeOut(text))  # Only final frame computed

        # Resume normal rendering
        self.next_section()
        self.play(Create(square))
```

**Note:** Each section produces a separate video file, then they're concatenated. Final output is the same as without sections.

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

**Slow rendering:**
- Use `-ql` during development
- Prefer `Text` over `Tex` when possible
- Check for complex shapes with many points

**Memory issues:**
- Split long scenes into multiple shorter scenes
- Clear unused mobjects: `self.remove(mob)`

## Common Beginner Mistakes

### Version Confusion

**ManimCE vs 3b1b/manim:**
- ManimCE (`pip install manim`) - community maintained, recommended
- 3b1b/manim (`pip install manimgl`) - Grant Sanderson's version, experimental
- Installation instructions are NOT interchangeable

### Avoid `manim init project`

The `manim init project` command creates a `manim.cfg` that can distort the default coordinate system. **Skip this command** and create scenes directly.

### Text vs Tex Performance

| Type | Speed | Use When |
|------|-------|----------|
| `Text` | Fast | Regular text, non-English alphabets |
| `Tex`/`MathTex` | Slow (LaTeX compilation) | Mathematical formulas only |

### Transform Reference Confusion

```python
# WRONG: Using target object after Transform
self.play(Transform(square, circle))
self.play(circle.animate.shift(UP))  # circle hasn't changed!

# CORRECT: Use original object reference
self.play(Transform(square, circle))
self.play(square.animate.shift(UP))  # square now looks like circle
```

### 3D Coordinate Type Error

```python
# WRONG: Integer coordinates can cause errors
Arrow3D(ORIGIN, [2, 1, 1])

# CORRECT: Use floats
Arrow3D(ORIGIN, [2.0, 1.0, 1.0])
```

## LaTeX Troubleshooting

### Common LaTeX Errors

**"LaTeX Error: Missing $ inserted":**
- Math symbols must be in math mode
- Use `MathTex` instead of `Tex` for equations
- Or wrap in `$...$`: `Tex(r"The value is $x^2$")`

**"Undefined control sequence":**
- Missing package - add to preamble
- Wrong command name
- Use raw strings: `r"\frac{a}{b}"` not `"\frac{a}{b}"`

**Raw Strings Required:**
```python
# CORRECT - raw string
tex = MathTex(r"\frac{a}{b}")

# WRONG - backslash escaping issues
tex = MathTex("\frac{a}{b}")  # Will fail!
```

### LaTeX Distribution Issues

**dvisvgm version too old:**
```bash
# Check version (need 2.4+)
dvisvgm --version

# On macOS with Homebrew
brew install --cask mactex  # Full TeX Live
# or
brew install basictex && brew install dvisvgm
```

**MiKTeX vs TeX Live:**
- TeX Live recommended on macOS/Linux
- MiKTeX common on Windows
- Both work, but TeX Live has better package management

**Windows `FileNotFoundError: [WinError 2]` during render:**
- Usually means TeX tooling is missing while using `Tex`, `MathTex`, or number mobjects that depend on TeX.
- Install MiKTeX/TeX Live, or switch those labels to `Text(str(value))` for a TeX-free path.

**Custom Preamble:**
```python
# Add packages for special symbols
myTemplate = TexTemplate()
myTemplate.add_to_preamble(r"\usepackage{amssymb}")
tex = MathTex(r"\mathbb{R}", tex_template=myTemplate)
```

## Font Handling

### Checking Available Fonts

```python
# List all available fonts
import manimpango
fonts = manimpango.list_fonts()
print(fonts)  # ['Arial', 'Courier New', ...]
```

### Font Issues

**Font not found:**
```python
# Check if font exists
import manimpango
if "My Font" in manimpango.list_fonts():
    text = Text("Hello", font="My Font")
else:
    text = Text("Hello")  # Use default
```

**Case sensitivity:**
- Font names are case-sensitive on some systems
- `"Arial"` ≠ `"arial"`

**Custom Fonts:**
```python
from manim import *

# Register a custom font file
register_font("/path/to/MyFont.ttf")

# Then use it
text = Text("Hello", font="MyFont")
```

### Fallback Strategy

```python
def safe_text(content, preferred_font="SF Pro", fallback_font="Arial"):
    """Create text with font fallback."""
    import manimpango
    fonts = manimpango.list_fonts()

    if preferred_font in fonts:
        return Text(content, font=preferred_font)
    elif fallback_font in fonts:
        return Text(content, font=fallback_font)
    else:
        return Text(content)  # System default
```

## Jupyter Notebook Usage

### Basic Magic Command

```python
%%manim -qm -v WARNING MyScene

class MyScene(Scene):
    def construct(self):
        circle = Circle()
        self.play(Create(circle))
```

### Common Parameters

| Flag | Description |
|------|-------------|
| `-qm` | Medium quality (720p30) |
| `-ql` | Low quality (480p15) - fastest |
| `-qh` | High quality (1080p60) |
| `-v WARNING` | Reduce log verbosity |
| `-s` | Output last frame only (image) |
| `--disable_caching` | Force re-render |

### Full Example

```python
# In Jupyter cell
%%manim -qm -v WARNING --disable_caching CircleDemo

class CircleDemo(Scene):
    def construct(self):
        c = Circle(color=BLUE)
        self.play(Create(c))
        self.play(c.animate.shift(RIGHT * 2))
        self.wait()
```

### Tips for Jupyter

- Use `-v WARNING` to reduce output noise
- Use `--disable_caching` when iterating quickly
- Class name in magic must match scene class name
- Multiple scenes in one notebook: define each with different names

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

## v0.18 Changes

### ManimColor System

v0.18 replaced the `colour` library with `ManimColor`:

```python
from manim import ManimColor, RED, BLUE

# Create from hex
color = ManimColor.from_hex("#FF5733")

# Convert between formats
rgb = color.to_rgb()        # [0-1, 0-1, 0-1]
rgba = color.to_rgba()      # [0-1, 0-1, 0-1, 0-1]
int_rgb = color.to_int_rgb() # [0-255, 0-255, 0-255]
hex_str = color.to_hex()     # "#FF5733"

# Create from RGB
color = ManimColor.from_rgb([1.0, 0.5, 0.2])
color = ManimColor.from_rgba([1.0, 0.5, 0.2, 0.8])
```

### Health Check Command

```bash
# Check installation is correct
manim checkhealth
```

## v0.19 Breaking Changes

**IMPORTANT:** These changes may break existing code when upgrading.

### Parameter Renames

```python
# ManimColor.from_hex: hex → hex_str
# OLD (broken): ManimColor.from_hex(hex="#FFFFFF")
# NEW (correct):
ManimColor.from_hex(hex_str="#FFFFFF")

# Scene.next_section: type → section_type
# OLD (broken): self.next_section(type="intro")
# NEW (correct):
self.next_section(section_type="intro")
```

### SurroundingRectangle Positional Args

```python
# v0.19 now accepts *mobjects, so positional args after first must be keywords
# OLD (broken): SurroundingRectangle(mob, RED, 0.3)
# NEW (correct):
SurroundingRectangle(mob, color=RED, buff=0.3)

# Multiple mobjects now supported
SurroundingRectangle(mob1, mob2, mob3, color=YELLOW)
```

### Sector Constructor

```python
# inner_radius and outer_radius removed from Sector
# OLD (broken): Sector(inner_radius=0.5, outer_radius=1)
# NEW: Use AnnularSector for ring sectors
from manim import AnnularSector
sector = AnnularSector(inner_radius=0.5, outer_radius=1, angle=PI/3)

# For simple sectors, use radius and angle
from manim import Sector
sector = Sector(outer_radius=1, angle=PI/3)
```

### Code Mobject Rewrite

The Code mobject was completely rewritten. Use `code_string` not `code`:

```python
# OLD (broken): Code(code="print('hello')")
# NEW (correct):
Code(code_string="print('hello')", language="python")
```

### Square.side_length Property

`side_length` is now a property, not just an attribute:

```python
square = Square(side_length=2)
current = square.side_length  # Getter
square.side_length = 3        # Setter (updates geometry)
```

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

## v0.19.1 Updates

### ValueTracker Arithmetic Operators

New operators for ValueTracker math operations:

```python
tracker = ValueTracker(10)

# Floor division
result = tracker // 3  # Returns ValueTracker with value 3

# Modulo
result = tracker % 3   # Returns ValueTracker with value 1

# Power
result = tracker ** 2  # Returns ValueTracker with value 100

# Multiplication
result = tracker * 2   # Returns ValueTracker with value 20

# Division
result = tracker / 2   # Returns ValueTracker with value 5.0
```

### HSV Color Class

Create colors using HSV (Hue, Saturation, Value):

```python
from manim import HSV

# Create color from HSV values (h: 0-1, s: 0-1, v: 0-1)
color = HSV(0.5, 1.0, 1.0)  # Cyan

# Animate through rainbow
class RainbowDemo(Scene):
    def construct(self):
        tracker = ValueTracker(0)
        circle = Circle()
        circle.add_updater(
            lambda m: m.set_color(HSV(tracker.get_value(), 1, 1))
        )
        self.add(circle)
        self.play(tracker.animate.set_value(1), run_time=3)
```

### Random Color with Seed

Generate reproducible random colors:

```python
# Reproducible random color
color1 = random_color(seed=42)
color2 = random_color(seed=42)  # Same as color1

# Random without seed (different each time)
color3 = random_color()
```

### SurroundingRectangle Buff Tuple

Control horizontal and vertical padding separately:

```python
text = Text("Hello")

# Same padding all sides
rect1 = SurroundingRectangle(text, buff=0.2)

# Different horizontal/vertical padding (new in v0.19.1)
rect2 = SurroundingRectangle(text, buff=(0.5, 0.2))  # (horizontal, vertical)
```

### Other v0.19.1 Fixes
- Fixed `Code` mobject line number alignment
- Improved SVG parsing for complex paths
- Better error messages for common mistakes
- Performance improvements for large scenes

## Manim Plugins

Community-developed extensions for specialized features.

### manim-voiceover

Add AI-generated voiceovers with per-word timing.

```bash
pip install manim-voiceover[azure]  # or [gtts], [elevenlabs]
```

```python
from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.azure import AzureService

class VoiceoverDemo(VoiceoverScene):
    def construct(self):
        self.set_speech_service(AzureService())

        circle = Circle()
        with self.voiceover(text="Here is a circle") as tracker:
            self.play(Create(circle), run_time=tracker.duration)
```

**Supported services:** Azure, ElevenLabs, gTTS, OpenAI, Coqui

### manim-slides

Create interactive presentations from Manim animations.

```bash
pip install manim-slides
```

```python
from manim import *
from manim_slides import Slide

class MySlides(Slide):
    def construct(self):
        circle = Circle()
        self.play(Create(circle))
        self.next_slide()  # Wait for click/key before continuing

        self.play(circle.animate.shift(RIGHT))
        self.next_slide()
```

```bash
# Render then present
manim -qh slides.py MySlides
manim-slides MySlides  # Opens presentation viewer
```

### manim-physics

Physics simulations with rigid body dynamics.

```bash
pip install manim-physics
```

```python
from manim import *
from manim_physics import *

class FallingBalls(SpaceScene):
    def construct(self):
        ground = Line(LEFT * 4, RIGHT * 4).shift(DOWN * 2)
        balls = [Circle(radius=0.2).shift(UP * i) for i in range(3)]

        self.make_static_body(ground)
        for ball in balls:
            self.make_rigid_body(ball)

        self.add(ground, *balls)
        self.wait(5)  # Physics runs automatically
```

### Plugin Installation Notes

Most plugins work with ManimCE v0.18+. Check compatibility before upgrading Manim versions.

```bash
# Install plugins
pip install manim-voiceover manim-slides manim-physics

# Check installed plugins
pip list | grep manim
```
