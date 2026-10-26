---
name: manim
description: Create and edit programmatic explanatory animations, videos, and GIFs with Manim Community Edition. Use for mathematical animation, algorithm animation, animated technical diagrams, or an explicit Manim request. Static diagrams, ordinary charts, and interactive web UI do not need this skill unless the user chooses Manim.
metadata:
  version: "2.1.0"
---

# Manim animations

Use Manim Community Edition (CE), not `manimgl` / `manimlib`, unless the user explicitly requests that engine. Preserve an existing project's engine and dependency constraints; migration is a separate choice.

This edition targets **ManimCE 0.22.x, Python 3.11+**. Check `python --version` and `python -m manim --version` in the project's environment before writing version-sensitive code. For an older project, read the matching official docs rather than silently upgrading it. See [setup and migration](references/setup-and-migration.md) for installation, optional math backends, output changes, and troubleshooting.

## Workflow

1. Establish the explanation: what changes over time, what the viewer should understand, and the requested output (video/GIF/still, duration, aspect ratio, language). Infer sensible defaults for unspecified presentation choices; ask only when the answer changes the work materially.
2. Before coding a new animation or improving its appearance, read [visual direction](references/visual-direction.md). Choose a focal object and sketch a short shot list: question, visible action, insight, timing. Make the changing geometry carry the explanation; use captions to support it. Use explicit labels as well as color to convey state.
3. Write a runnable scene in the user's project, keeping output media separate from source. Use public scene APIs. Configure resolution, renderer, and output **before** constructing a scene; use CLI flags or `tempconfig` rather than changing global config after `super().__init__()`.
4. Render a low-quality **video** first. Inspect opening, intermediate, and final frames, and review transitions for pacing and semantic correctness. A last-frame PNG or a successful command alone does not verify an animation. Fix clipping, unreadable labels, overlaps, wrong states, and unexpected jumps before increasing quality.
5. Render the requested artifact and verify it exists, decodes, and has the intended dimensions, duration, and format. Deliver the source path, artifact path, exact render command, environment version, and any verification limits. Do not claim visual acceptance when only syntax or rendering was checked.

For a blog embed, a short 16:9 MP4 is a reasonable starting point; GIF is useful when required but can be larger and less efficient. Follow the user's duration and style rather than imposing a fixed length or banning titles.

## Small starting point

```python
from manim import BLUE, Circle, Create, Scene, Text, VGroup, DOWN

class Explain(Scene):
    def construct(self):
        circle = Circle(color=BLUE)
        label = Text("Input", font_size=32).next_to(circle, DOWN)
        group = VGroup(circle, label)
        self.play(Create(group))
        self.wait(1)
```

Run from the environment containing Manim:

```bash
python -m manim render -ql scene.py Explain
python -m manim render -qh --format mp4 scene.py Explain
python -m manim render -qm --format gif scene.py Explain
python -m manim render -ql --format png scene.py Explain
```

`-p` opens the completed artifact; omit it in headless runs. `--format png` writes only the last frame. For all frames use `png-sequence`; `--format none` evaluates without producing media. `--dry_run` remains supported, but is not visual verification. Standard presets: `-ql` 480p15, `-qm` 720p30, `-qh` 1080p60, `-qk` 2160p60. See [setup and migration](references/setup-and-migration.md) for 0.22 output semantics.

## Read only what the scene needs

| Need | Reference / runnable starting point |
|---|---|
| Composition, visual storytelling, choreography, appearance review | [visual direction](references/visual-direction.md); `examples/visual_story.py`: `VectorStory` |
| Labels, formulas, code, axes, graphs, layout | [mobjects](references/mobjects.md); `examples/basic_scene.py` |
| Transforms, timing, live values, object identity | [animations](references/animations.md) |
| Camera, 3D, updaters, programmatic rendering | [advanced](references/advanced.md); `examples/advanced_scene.py` |
| Formula without a TeX installation, including labeled derivations | [mobjects: math backends](references/mobjects.md#math-backends); `examples/typst_scene.py`, `examples/typst_derivation.py` |
| Process, state, comparison, algorithm explanation | [storytelling patterns](references/blog-patterns.md); `examples/flowchart.py`, `examples/state_diagram.py`, `examples/quicksort.py` |
| Installation or older Manim code | [setup and migration](references/setup-and-migration.md) |

## Reliability notes

- Text uses Pango and installed fonts. Check glyph coverage for the requested language; inspect rendered text for missing characters. `Text` does not require TeX. Some convenience objects (including default numeric labels) do; choose `Text` labels when avoiding TeX.
- In 0.22, formulas can use `Tex`/`MathTex` (external TeX tools) or `Typst`/`MathTypst` (optional `manim[typst]` dependency). Typst math uses its own syntax, not LaTeX syntax.
- Use `Code(code_string=..., language=..., formatter_style=...)`. Syntax and line-number colors come from Pygments, not `paragraph_config["color"]`.
- `Transform(source, target)` changes the source; keep animating the source variable. `ReplacementTransform` replaces it with the target. Avoid two simultaneous animations mutating the same mobject.
- Frame dimensions are scene units, distinct from output pixels. Fit the complete composition inside `config.frame_width` / `frame_height` with margins, including arrowheads, labels, and motion extrema. Inspect portrait layouts separately.
- Use Cairo for a portable starting point. OpenGL requires a functioning display/graphics environment and has different camera APIs; test it explicitly when requested.

## Repository checks

For changes to this skill or its examples, follow [the contributing checks](README.md#development-and-verification). The smoke runner renders examples, probes media, and extracts contact sheets. Its report distinguishes skipped optional backends and rendering success from human visual review.

Official references: [versioned 0.22 docs](https://docs.manim.community/en/v0.22.0/), [changelog](https://docs.manim.community/en/stable/changelog.html), [source](https://github.com/ManimCommunity/manim).
