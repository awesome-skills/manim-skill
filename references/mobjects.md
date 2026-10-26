# Mobjects, text, and layout

Use [the versioned API](https://docs.manim.community/en/v0.22.0/reference.html) for uncommon constructors rather than guessing from ManimGL examples. This reference covers choices that commonly affect generated scenes.

## Text and glyphs

```python
from manim import *

label = Text("Input", font_size=32)
status = Text("Ready", color=GREEN, font_size=28)
rich = MarkupText('<b>Step 1</b>: parse', font_size=28)
```

Choose an installed font with glyph coverage for the requested language; list candidates with `manimpango.list_fonts()`. For Chinese, verify that the selected CJK font actually exists. Avoid hardcoding a platform-specific font without checking it. A font that exists can still lack a particular symbol; inspect the artifact.

`Text` character indexing omits whitespace in some cases; do not assume Python string offsets map directly to submobject indices. Separate semantic labels when highlighting them is important.

## Math backends

TeX:

```python
formula = MathTex(r"E = mc^2", font_size=56)
identity = MathTex(r"a^2", "+", r"b^2", "=", r"c^2")
identity.set_color_by_tex("c", GREEN)
```

For selecting subexpressions, prefer explicit grouping or public selection methods over undocumented numeric indices. The 0.20 MathTex rewrite changed splitting behavior; verify transforms with the installed version.

Typst (optional extra, runnable scene in `examples/typst_scene.py`):

```python
from manim import Typst, MathTypst

heading = Typst("A formula without TeX", font_size=36)
formula = MathTypst("sum_(k=1)^n k = (n(n+1))/2", font_size=48)
```

For a derivation, use named captures such as `MathTypst("{{ a^2 : left_a }} = {{ c^2 : right_c }}")` and `formula.select("left_a")`. Give repeated occurrences distinct names (for example, `left_b`, `subtract_left_b`, `subtract_right_b`) so matching preserves their roles. A repeated label selects all its occurrences, which is useful for collective styling but ambiguous for a one-to-one move.

Keep the full formula's typeset layout, select disjoint semantic groups, and animate those groups with explicit `ReplacementTransform` mappings. If adding the selected groups directly to the scene, keep their parent formula out of the scene so each glyph has one animation owner. Align successive formulas by a stable anchor such as the equals sign. See `examples/typst_derivation.py`: `TypstDerivation` for a runnable subtraction-on-both-sides and cancellation sequence using the existing optional Typst extra.

Typst has its own language: passing LaTeX commands such as `\frac` is not a drop-in migration. Use `manim[typst]` and inspect font/math output. Plain numeric labels can use `Text(str(value))`; `Integer`, `DecimalNumber`, `Variable`, axes numbers, and default graph labels may otherwise invoke TeX. Pass explicit `Text` labels when creating a TeX-free graph:

```python
axes = Axes(x_range=[-3, 3, 1], y_range=[0, 9, 3], x_length=7, y_length=4)
curve = axes.plot(lambda x: x**2, color=BLUE)
x_label = axes.get_x_axis_label(Text("x", font_size=28))
curve_label = axes.get_graph_label(curve, label=Text("x²", font_size=28))
```

## Code

```python
code = Code(
    code_string="def square(x):\n    return x * x",
    language="python",
    formatter_style="monokai",
    background="rectangle",
    paragraph_config={"font_size": 24},
)
```

For a file use `code_file=...`, not `code=...`. Explicit `language` avoids ambiguous detection. `Code.get_styles_list()` lists available style names. In 0.21+, syntax and line-number foreground colors come from the selected Pygments style; do not set `paragraph_config["color"]`. A custom Pygments `Style` can define tokens and `line_number_color`; backgrounds can use `background_config={"fill_color": ...}`. See the installed [Code API](https://docs.manim.community/en/v0.22.0/reference/manim.mobject.text.code_mobject.Code.html) for a complete style example.

## Geometry and groups

```python
node = VGroup(
    RoundedRectangle(width=2, height=1, corner_radius=0.15, fill_opacity=0.2),
    Text("Parse", font_size=24),
)
node[1].move_to(node[0])
sector = Sector(radius=1, angle=PI / 3)
ring = AnnularSector(inner_radius=0.5, outer_radius=1, angle=PI / 3)
```

`Sector` takes `radius`; `outer_radius` belongs to `AnnularSector`. Mixing them can pass the same underlying argument twice.

Use `VGroup` for vector objects, `Group` when mixing non-vector objects such as `ImageMobject`. `SurroundingRectangle(*mobjects, color=..., buff=...)` accepts multiple objects, so style arguments should be keywords.

For images, 0.20 removed `lanczos`/`antialias`, `box`, and `hamming` resampling modes; consult the current `RESAMPLING_ALGORITHMS` rather than copying removed names.

## Layout

```python
nodes = VGroup(node_a, node_b, node_c).arrange(RIGHT, buff=0.8)
arrows = VGroup(*[
    Arrow(nodes[i].get_right(), nodes[i + 1].get_left(), buff=0.1)
    for i in range(len(nodes) - 1)
])
composition = VGroup(nodes, arrows)
composition.scale_to_fit_width(config.frame_width - 1)
composition.move_to(ORIGIN)
```

Arrange nodes before computing connectors. If scaling the full composition, include labels and arrows so they stay attached. Avoid scaling tiny text down to make an overfull diagram fit; reduce content or split scenes instead.

- Pixel resolution controls raster detail; `frame_width` and `frame_height` control scene geometry.
- Use `next_to`, `align_to`, `arrange`, and `arrange_in_grid` for relationships; use absolute coordinates for deliberate composition.
- Keep label width within its container, use multiline labels when useful, and allow space for arrowheads and movement.
- Test both the initial and changing layout. A static final image cannot reveal overlaps during transitions.
- Tables with plain strings may default to `MathTex`; set `element_to_mobject=Text` for a TeX-free text table.

Graphs can use `Graph`/`DiGraph`; choose a layout intentionally, position nodes before labels/edges, and verify directionality. For state explanations, use the runnable scenes rather than turning every graph into a generic topology animation.
