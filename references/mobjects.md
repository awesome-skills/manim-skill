# Manim Mobjects Reference

Complete reference for Manim Community Edition Mobjects.

## Text Objects

### Text

Plain text rendering using Pango library. Ideal for non-LaTeX text, especially non-English alphabets.

```python
from manim import *

# Basic text
text = Text("Hello World")

# With styling
text = Text("Styled", font_size=72, color=BLUE, font="Arial")

# Gradient text
text = Text("Gradient", gradient=(RED, BLUE))

# Text-to-X mappings (selective styling)
text = Text(
    "Hello World styled",
    t2c={"Hello": RED, "World[0:2]": BLUE},  # text-to-color (supports slicing)
    t2f={"styled": "Courier New"},            # text-to-font
    t2s={"World": ITALIC},                    # text-to-slant
    t2w={"Hello": BOLD},                      # text-to-weight
    t2g={"World": (RED, BLUE)},               # text-to-gradient
)

# Line spacing
text = Text("Line 1\nLine 2", line_spacing=1.5)

# Disable font warning
text = Text("Hello", warn_missing_font=False)
```

**Note:** Text is an SVGMobject, so you can use VMobject methods like `set_stroke()`, `set_fill()`, etc.

### MarkupText

HTML-like formatting for rich text.

```python
text = MarkupText(
    '<span foreground="red">Red</span> and <b>bold</b> and <i>italic</i>'
)
```

### Tex and MathTex

LaTeX rendering for mathematical expressions.

```python
# Tex: general LaTeX (not auto math mode)
tex = Tex(r"\LaTeX\ is great", font_size=72)

# MathTex: auto-wrapped in align* environment (math mode)
math = MathTex(r"E = mc^2")

# Multi-line math (align* allows & for alignment)
equation = MathTex(
    r"f(x) &= x^2 + 2x + 1 \\",
    r"&= (x+1)^2"
)

# Colored parts (by index) - each string becomes a submobject
math = MathTex(r"a", r"+", r"b", r"=", r"c")
math[0].set_color(RED)    # 'a' is red
math[2].set_color(BLUE)   # 'b' is blue

# Using substrings_to_isolate for targeting
math = MathTex(
    r"e^{i\pi} + 1 = 0",
    substrings_to_isolate=["e", r"\pi"]
)
math.set_color_by_tex("e", RED)
math.set_color_by_tex(r"\pi", BLUE)

# Double braces {{ }} also isolate substrings
math = MathTex(r"{{a}} + {{b}} = {{c}}")

# Custom TeX template for special packages
from manim import TexTemplate
template = TexTemplate()
template.add_to_preamble(r"\usepackage{amssymb}")
math = MathTex(r"\mathbb{R}", tex_template=template)

# Font templates
from manim import TexFontTemplates
tex = Tex("Comic Sans", tex_template=TexFontTemplates.comic_sans)
```

**Important:** Always use raw strings `r"..."` for LaTeX to avoid backslash escape issues.

## Code Objects

### Code (v0.19+)

Syntax-highlighted code display. Completely rewritten in v0.19.

```python
# From string (use code_string parameter!)
code = Code(
    code_string="""def hello():
    print("Hello, World!")
    return 42""",
    language="python",           # Specify explicitly (auto-detect can fail)
    background="rectangle",      # or "window" (macOS-style window)
    formatter_style="monokai",   # pygments style
    tab_width=4,
    add_line_numbers=True,
    line_numbers_from=1,
)

# From file
code = Code(
    code_file="path/to/file.py",
    language="python",
)

# With custom styling
code = Code(
    code_string="print('hello')",
    language="python",
    background="window",
    background_config={"stroke_color": WHITE},
    paragraph_config={"font": "Noto Sans Mono"},
)

# Available styles
styles = Code.get_styles_list()
# ['monokai', 'vim', 'native', 'fruity', 'vs', 'emacs', ...]
```

**Note:** Use `code_string` not `code`. The `code` parameter was removed in v0.19.

## Geometric Shapes

### Basic Shapes

```python
# Circle
circle = Circle(radius=1, color=BLUE, fill_opacity=0.5)
circle = Circle().surround(other_mobject)  # Surround another object

# Dot
dot = Dot(point=ORIGIN, radius=0.08, color=WHITE)

# Square
square = Square(side_length=2, color=RED)

# Rectangle
rect = Rectangle(width=4, height=2, color=GREEN)
rect = Rectangle(height=2).set_width(4, stretch=True)

# RoundedRectangle
rounded = RoundedRectangle(
    width=3, height=1.5,
    corner_radius=0.25,
    fill_color=BLUE,
    fill_opacity=0.3,
    stroke_color=WHITE
)

# Ellipse
ellipse = Ellipse(width=4, height=2, color=YELLOW)

# Polygon
triangle = Polygon(UP, DL, DR, color=RED)
hexagon = RegularPolygon(n=6, color=PURPLE)

# Star
star = Star(n=5, outer_radius=2, inner_radius=1, color=GOLD)
```

### Lines and Arrows

```python
# Line
line = Line(start=LEFT, end=RIGHT, color=WHITE)
line = Line(ORIGIN, UP * 2 + RIGHT * 3)

# DashedLine
dashed = DashedLine(LEFT, RIGHT, dash_length=0.2, dashed_ratio=0.5)

# Arrow with all options
arrow = Arrow(
    start=LEFT, end=RIGHT,
    buff=0.1,                           # Distance from start/end points
    stroke_width=3,
    max_tip_length_to_length_ratio=0.2, # Tip scales with arrow length
    max_stroke_width_to_length_ratio=5, # Stroke scales with arrow length
)

# Keep tip size when scaling
arrow.scale(2, scale_tips=True)  # Tip scales too
arrow.scale(2)                   # Only tail scales (default)

# DoubleArrow
double = DoubleArrow(LEFT, RIGHT)

# CurvedArrow (angle in radians, counter-clockwise)
curved = CurvedArrow(LEFT, RIGHT, angle=PI/2)

# CurvedDoubleArrow
curved_double = CurvedDoubleArrow(LEFT, RIGHT, angle=PI/4)

# Vector (arrow from origin)
vector = Vector(direction=UP + RIGHT)

# Custom arrow tips
from manim import ArrowTriangleFilledTip, StealthTip
arrow = Arrow(LEFT, RIGHT, tip_shape=StealthTip)
```

### Arcs and Curves

```python
# Arc
arc = Arc(radius=1, start_angle=0, angle=PI/2, color=RED)

# ArcBetweenPoints
arc = ArcBetweenPoints(start=LEFT, end=RIGHT, angle=PI/4)

# CubicBezier
bezier = CubicBezier(
    start_anchor=LEFT,
    start_handle=LEFT + UP,
    end_handle=RIGHT + UP,
    end_anchor=RIGHT
)

# AnnularSector (pie slice)
sector = AnnularSector(
    inner_radius=1, outer_radius=2,
    angle=PI/3, start_angle=0, color=BLUE
)
```

### Braces and Brackets

```python
# Brace around a mobject
brace = Brace(mobject, direction=DOWN)
label = brace.get_tex("width")      # LaTeX label
text_label = brace.get_text("width") # Text label

# BraceBetweenPoints (direction auto-computed)
brace = BraceBetweenPoints(LEFT, RIGHT)
brace = BraceBetweenPoints(LEFT, RIGHT, direction=UP)  # Manual direction

# BraceLabel (brace + label combined)
from manim import BraceLabel
bl = BraceLabel(mobject, "label text", brace_direction=DOWN)

# BraceText (uses Text instead of MathTex)
from manim import BraceText
bt = BraceText(mobject, "plain text", brace_direction=DOWN)

# ArcBrace for curved objects
from manim import ArcBrace
arc = Arc(angle=PI/2)
arc_brace = ArcBrace(arc)

# Combined
group = VGroup(rect, brace, label)
```

## Graphs and Coordinate Systems

### Axes

```python
axes = Axes(
    x_range=[-5, 5, 1],      # [min, max, step]
    y_range=[-3, 3, 1],
    x_length=10,
    y_length=6,
    axis_config={
        "color": BLUE,
        "include_numbers": True,
        "numbers_to_include": [-4, -2, 0, 2, 4],
    },
    x_axis_config={
        "numbers_to_include": range(-4, 5, 2),
    },
    tips=True,  # Arrow tips on axes
)

# Plot a function
graph = axes.plot(lambda x: x**2, color=WHITE, x_range=[-2, 2])

# Plot with discontinuity
graph = axes.plot(
    lambda x: 1/x,
    color=RED,
    discontinuities=[0],
    dt=0.01
)

# Add graph label
label = axes.get_graph_label(graph, label="f(x) = x^2", x_val=2)

# Coordinate labels
coords = axes.get_axis_labels(x_label="x", y_label="y")

# Add to scene
self.add(axes, graph, label, coords)
```

### NumberLine

```python
number_line = NumberLine(
    x_range=[-5, 5, 1],
    length=10,
    include_numbers=True,
    include_tip=True,
)

# Add a dot at position
dot = Dot(number_line.n2p(3))  # number to point
```

### NumberPlane

```python
plane = NumberPlane(
    x_range=[-5, 5, 1],
    y_range=[-3, 3, 1],
    background_line_style={
        "stroke_color": BLUE_D,
        "stroke_width": 1,
        "stroke_opacity": 0.5,
    }
)
```

## Tables

```python
# Basic Table (strings become Text mobjects)
table = Table(
    [["A", "B", "C"],
     ["1", "2", "3"],
     ["X", "Y", "Z"]],
    row_labels=[Text("R1"), Text("R2"), Text("R3")],
    col_labels=[Text("C1"), Text("C2"), Text("C3")],
    include_outer_lines=True,
    h_buff=0.5,  # Horizontal buffer
    v_buff=0.5,  # Vertical buffer
)

# Highlight cell
table.add_highlighted_cell((2, 3), color=YELLOW)

# Get specific cell
cell = table.get_cell((1, 2))

# MathTable (LaTeX rendering)
from manim import MathTable
math_table = MathTable(
    [[r"\pi", r"e", r"\phi"],
     ["3.14", "2.72", "1.62"]]
)

# IntegerTable (auto-converts to integers, rounds decimals)
from manim import IntegerTable
int_table = IntegerTable([[1, 2, 3], [4, 5, 6]])

# DecimalTable (formatted decimals)
from manim import DecimalTable
dec_table = DecimalTable(
    [[1.234, 2.567], [3.891, 4.123]],
    element_to_mobject_config={"num_decimal_places": 2}
)

# MobjectTable (each cell is already a Mobject)
from manim import MobjectTable
mob_table = MobjectTable([
    [Circle(), Square()],
    [Triangle(), Star()]
])
```

## Network Graphs

Graph theory visualizations (not to be confused with plotting graphs).

```python
from manim import Graph, DiGraph

# Undirected graph
vertices = [1, 2, 3, 4, 5]
edges = [(1, 2), (2, 3), (3, 4), (4, 5), (5, 1), (1, 3)]
graph = Graph(vertices, edges)

# With labels
graph = Graph(vertices, edges, labels=True)

# Custom layout
graph = Graph(
    vertices, edges,
    layout="circular",  # or "tree", "planar", "random", "shell", "spectral", "spiral", "partite"
    layout_scale=2,
)

# Directed graph
digraph = DiGraph(
    [1, 2, 3],
    [(1, 2), (2, 3), (3, 1)],
    labels=True,
)

# Custom vertex mobjects
vertex_config = {
    1: {"fill_color": RED},
    2: {"fill_color": BLUE},
}
graph = Graph(vertices, edges, vertex_config=vertex_config)

# Custom edge config
edge_config = {
    (1, 2): {"stroke_color": RED},
}
graph = Graph(vertices, edges, edge_config=edge_config)

# From NetworkX
import networkx as nx
G = nx.petersen_graph()
graph = Graph.from_networkx(G)
```

## Groups

### VGroup (Vector Group)

```python
# Create group
group = VGroup(circle, square, triangle)

# Arrange horizontally
group.arrange(RIGHT, buff=0.5)

# Arrange vertically
group.arrange(DOWN, buff=0.3)

# Arrange in grid
group.arrange_in_grid(rows=2, cols=3, buff=0.5)

# Access by index
group[0].set_color(RED)

# Add to group
group.add(new_mobject)
```

### Group Operations

```python
# Scale entire group
group.scale(0.5)

# Move group
group.shift(UP * 2)

# Set group color
group.set_color(BLUE)

# Copy group
group_copy = group.copy()
```

## SVG and Images

### SVGMobject

```python
# Basic SVG import
svg = SVGMobject("icon.svg")
svg.set_color(WHITE)
svg.scale(0.5)

# With height control
svg = SVGMobject("icon.svg", height=2)  # 2 Manim units

# No scaling (original size)
svg = SVGMobject("icon.svg", height=None, width=None)

# Access submobjects (each SVG path is a submobject)
svg[0].set_color(RED)   # First path
svg[1].set_color(BLUE)  # Second path

# Disable caching for dynamic SVGs
svg = SVGMobject("icon.svg", use_svg_cache=False)
```

**Note:** SVGMobject is a VMobject, so animations like `Create`, `Write`, `DrawBorderThenFill` work.

### ImageMobject

```python
# Basic image
image = ImageMobject("photo.png")
image.scale(2)

# Set dimensions
image.set(width=4)
image.set(height=3)

# Resampling for pixel art
from manim import RESAMPLING_ALGORITHMS
image.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
```

**Note:** ImageMobject is NOT a VMobject. Use `FadeIn`/`FadeOut`, not `Create`/`Write`.

## Special Mobjects

### SurroundingRectangle

```python
# Basic surrounding rectangle (v0.19+ syntax)
surround = SurroundingRectangle(
    mobject,
    color=YELLOW,
    buff=0.2,
    corner_radius=0.1
)

# Multiple mobjects (v0.19+)
surround = SurroundingRectangle(mob1, mob2, mob3, color=RED)

# Horizontal/vertical buff tuple (v0.19.1+)
surround = SurroundingRectangle(
    mobject,
    buff=(0.5, 0.2)  # (horizontal, vertical)
)

# IMPORTANT: v0.19 breaking change!
# Old (broken): SurroundingRectangle(mob, RED, 0.3)
# New (correct): SurroundingRectangle(mob, color=RED, buff=0.3)
```

### BackgroundRectangle

```python
# Add background to text
bg = BackgroundRectangle(text, color=BLACK, fill_opacity=0.8)
group = VGroup(bg, text)
```

### Cross

```python
# X mark over something
cross = Cross(mobject, stroke_color=RED, stroke_width=6)
```

### Underline

```python
underline = Underline(text, color=YELLOW)
```

## Common Patterns

### Labeled Diagram Node

```python
def make_node(label, color=BLUE):
    rect = RoundedRectangle(
        width=2, height=1,
        corner_radius=0.15,
        fill_color=color,
        fill_opacity=0.3,
        stroke_color=color,
    )
    text = Text(label, font_size=20)
    text.move_to(rect)
    return VGroup(rect, text)

node = make_node("Server", GREEN)
```

### Flowchart Connection

```python
def connect_nodes(node1, node2, label=None):
    arrow = Arrow(
        node1.get_right(),
        node2.get_left(),
        buff=0.1,
        color=GRAY
    )
    if label:
        text = Text(label, font_size=14)
        text.next_to(arrow, UP, buff=0.1)
        return VGroup(arrow, text)
    return arrow
```

### State with Index

```python
def create_state(label, index, color=BLUE):
    circle = Circle(radius=0.5, color=color, fill_opacity=0.3)
    text = Text(label, font_size=18).move_to(circle)
    idx = Text(str(index), font_size=14, color=GRAY)
    idx.next_to(circle, UP, buff=0.1)
    return VGroup(circle, text, idx)
```
