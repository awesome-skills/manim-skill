# Manim Skill

Create explanatory animations with an AI coding agent and **Manim Community Edition**. Describe the concept; the skill guides scene authoring, low-quality previews, visual inspection, and final delivery.

[简体中文](README.zh-CN.md) · [Skill instructions](SKILL.md) · [Manim 0.22 documentation](https://docs.manim.community/en/v0.22.0/)

## Scope

Use for mathematical explanations, algorithm animations, animated technical diagrams, videos, and GIFs. A static chart or an interactive website does not need Manim by default. This skill targets **ManimCE 0.22.x and Python 3.11+**; it preserves an existing project's engine/version rather than silently migrating it.

## Install the skill

Copy this repository's skill folder into the skill directory used by your agent, or use an installer that accepts a GitHub repository root:

```bash
git clone https://github.com/awesome-skills/manim-skill.git
```

Install the folder containing `SKILL.md`, `references/`, `examples/`, and `scripts/`. Codex discovers `~/.codex/skills/manim-skill/SKILL.md`; other agents can use the same Markdown instructions. If you already use a shared skill directory, install there and retain your existing agent symlinks. Installing the skill does **not** install the rendering environment.

Example request:

> Use Manim to explain a three-step validation pipeline. Make a readable 10-second MP4, preview it at low quality, inspect the intermediate states, and return the editable Python scene and final video.

## Rendering environment

Follow the [official native dependency instructions](https://docs.manim.community/en/stable/installation.html), then run from the cloned repository:

```bash
uv sync --python 3.13 --extra typst
uv run python -m manim --version
uv run python -m manim checkhealth
uv run python -m manim render -ql examples/basic_scene.py BasicScene
```

The project constrains Manim to `>=0.22,<0.23`; `uv.lock` pins the resolved environment for reproducibility. Typst is optional. Install without `--extra typst` for non-Typst scenes. `MathExample` additionally needs an external TeX toolchain; the other basic examples use Pango text.

PyAV handles normal encoding, so a standalone FFmpeg executable is not a core Manim requirement. Native text dependencies and fonts still matter. ManimCE and ManimGL are different engines; their imports and APIs are not interchangeable.

## Examples

| File | Scenes / purpose |
|---|---|
| `examples/basic_scene.py` | Basic geometry, syntax-highlighted code, optional TeX math, TeX-free graph |
| `examples/flowchart.py` | Linear/branching processes and progress highlighting |
| `examples/state_diagram.py` | State transitions, index mismatch, cycles |
| `examples/quicksort.py` | Computed Lomuto-partition events and sorting animation |
| `examples/typst_scene.py` | Optional formula typesetting without a TeX distribution |
| `examples/typst_derivation.py` | Optional Typst derivation: explicit term identity, stable equals sign, subtraction and cancellation |
| `examples/advanced_scene.py` | Cairo camera focus and 3D orbit |
| `examples/visual_story.py` | Original head-to-tail vector story: composition, correspondence, staged revelation; no TeX |

The quicksort showcase is longer than a short blog loop; choose a smaller input or a narrower explanation for a short embed.

## Output

```bash
# Final video
uv run python -m manim render -qh --format mp4 examples/basic_scene.py BasicScene
# Animated GIF
uv run python -m manim render -qm --format gif examples/basic_scene.py BasicScene
# Last-frame PNG (does not verify the full timeline)
uv run python -m manim render -ql --format png examples/basic_scene.py BasicScene
# Optional Typst formula
uv run python -m manim render -ql examples/typst_scene.py TypstFormula
```

Add `-p` to open the completed artifact. In 0.22 this differs from the OpenGL `--live-preview` window. See [migration notes](references/setup-and-migration.md) for removed flags, output selection, and configuration timing.

## Development and verification

```bash
uv sync --locked --extra typst
uv run python -m unittest discover -s tests -v
uv run python scripts/smoke.py --include-typst
# Optional, when TeX is installed:
uv run python scripts/smoke.py --include-tex --include-typst
# Focused iteration:
uv run python scripts/smoke.py --scene BasicScene --scene CodeExample
```

Inspect specific transition times in an existing MP4 without rerendering (replace the video and times):

```bash
uv run python scripts/video_inspection.py scene.mp4 --at 6.8 --at 8 --columns 2 --output verification/review
```

The inspector saves full-resolution sampled PNGs, a multirow contact sheet and a JSON report with actual presentation times and the input hash. It selects the frame displayed at each requested time, including irregular frame intervals, and decodes the full clip. Timestamps are seconds from the first frame; the duration endpoint selects the last frame. It does not evaluate appearance or playback.

The runner renders every selected scene as a 640×360 / 15 fps Cairo MP4, decodes every frame, checks positive duration and dimensions, and writes per-scene logs/contact sheets plus `verification/report.json`. It records the interpreter, Manim version, source hashes, commands, failures, and optional-backend skips. Generated evidence is ignored by Git. Use a new output directory when comparing runs.

**Rendering is not visual approval.** Inspect contact sheets for missing glyphs, clipping, overlap, and wrong states; play the videos to evaluate timing and continuity. The report deliberately leaves `visual_review` as `not performed`; record actual review separately. Tests check quicksort data invariants and timestamp sampling against encoded videos, including irregular presentation times and CLI output.

CI renders with Typst on Python 3.11 and 3.13, additionally installs TeX for `MathExample` on 3.13, and uploads evidence even on failure. OpenGL and platform-specific font coverage require separate checks; Cairo results do not establish those claims.

## Reference layout

- [Visual direction](references/visual-direction.md): shot design, hierarchy, choreography and visual iteration; includes primary study references.

- [Setup and migration](references/setup-and-migration.md): environment, 0.20–0.22 changes, math backends, output flags.
- [Mobjects](references/mobjects.md): text, formulas, code, layout, constructor pitfalls.
- [Animations](references/animations.md): identity, timing, paths, updaters.
- [Advanced](references/advanced.md): camera, 3D, programmatic rendering, diagnosis.
- [Storytelling](references/blog-patterns.md): choose a progression and review the explanation.

References are loaded by task, not all at once. Runnable examples are the source of truth for complete patterns; documentation avoids maintaining duplicate copies of those scenes.

[Project research and adoption decisions](docs/research/animation-projects-2026-10-26.md) records which upstream ideas we adopted or deferred. See also [formula mechanisms](docs/research/formula-and-preview-projects-2026-10-26.md) and [preview feedback](docs/research/preview-feedback-projects-2026-10-26.md).

[Render-feedback research](docs/research/render-feedback-evaluation-2026-10-26.md) and a [fresh-session heap-repair trial](docs/evaluations/heap-repair-20261026/review.md) separate a concrete generated result from unmeasured general quality claims.

## License

MIT. See [LICENSE](LICENSE).
