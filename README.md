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
| `examples/quicksort.py` | Computed Lomuto events; persistent bars and numerals move during swaps |
| `examples/typst_scene.py` | Optional formula typesetting without a TeX distribution |
| `examples/typst_derivation.py` | Optional Typst derivation: explicit term identity, stable equals sign, subtraction and cancellation |
| `examples/advanced_scene.py` | Cairo camera focus and 3D orbit |
| `examples/visual_story.py` | Original head-to-tail vector story: coordinate inputs, continuous translation and a numeric result; no TeX |
| `examples/merge_step.py` | Light editorial merge; stable card identity, equal-value tie handling and clear motion lanes |
| `examples/wave_superposition.py` | Dark continuous plot; one phase drives both inputs and their sum |
| `examples/interference_study.py` | Editorial art direction: hierarchy, same-scale waves and measured result amplitude |
| `examples/data_to_decision.py` | Original records persist through grouping into count bars; delivery-width review |
| `examples/area_scale_story.py` | Bold typographic geometry: double the side, then prove four times the area |
| `examples/local_linearity.py` | Camera-led local/global comparison; stable geometry and view-sized annotations |
| `examples/circle_to_wave.py` | Continuous scene handoff; one tracked point connects an orbit to its sine trace |
| `examples/damping_story.py` | Three-beat physical story; equal starting conditions, analytic motion and energy |
| `examples/bezier_construction.py` | Graphic curve study; two interpolation levels construct a quadratic Bézier trace |
| `examples/exploded_layers.py` | Opaque 3D exploded view; fixed-size parts and screen-space annotations |
| `examples/motion_timing.py` | Landscape/portrait timing study; a shared clock and equal-time marks reveal easing |
| `examples/packet_journey.py` | Causal request flow; separate landscape and portrait compositions |

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
# Inspect a transition neighborhood and open verification/transition/review.html:
uv run python scripts/video_inspection.py scene.mp4 --around 4.2 --radius 0.3 --samples 5 --output verification/transition
```

The inspector saves full-resolution sampled PNGs, a multirow contact sheet and a JSON report with actual presentation times and the input hash. It selects the frame displayed at each requested time, including irregular frame intervals, and decodes the full clip. Timestamps are seconds from the first frame; the duration endpoint selects the last frame. It does not evaluate appearance or playback.

The CLI also creates a local `review.html` player with timestamp bookmarks and playback-speed controls. Keep the video at its original relative path. Browser seeking aids review; the PNG/JSON samples provide decoded-frame evidence. `--around` samples both sides of a transition (odd `--samples` of at least 3); out-of-range times fail. No video is uploaded and no additional runtime dependency is needed.

For a portrait example, run `uv run python -m manim render -qm --resolution 720,1280 examples/packet_journey.py PacketJourney`. This scene initializes the camera's scene-unit dimensions before construction and recomposes the route vertically; changing pixels alone does not adapt arbitrary scenes. `MotionTiming` also supports this resolution with shorter tracks and multiline type: use `examples/motion_timing.py MotionTiming` in the same command.

The runner renders every selected scene as a 640×360 / 15 fps Cairo MP4, decodes every frame, checks positive duration and dimensions, and writes per-scene logs/contact sheets plus `verification/report.json`. It records the interpreter, Manim version, source hashes, commands, failures, and optional-backend skips. Generated evidence is ignored by Git. Use a new output directory when comparing runs.

**Rendering is not visual approval.** Inspect contact sheets for missing glyphs, clipping, overlap, and wrong states; play the videos to evaluate timing and continuity. The report deliberately leaves `visual_review` as `not performed`; record actual review separately. Tests check algorithm identity and ordering, geometric and physical relations, portrait camera sizing, and timestamp sampling against encoded videos, including irregular presentation times and CLI output.

CI renders with Typst on Python 3.11 and 3.13, additionally installs TeX for `MathExample` on 3.13, and uploads evidence even on failure. OpenGL and platform-specific font coverage require separate checks; Cairo results do not establish those claims.

## Reference layout

- [Aesthetic refinement](references/aesthetic-refinement.md): art direction, typography, spacing and motion finish; [before/after study](docs/evaluations/art-direction-20261029/review.md).
- [Visual direction](references/visual-direction.md): shot design, hierarchy, choreography and visual iteration; includes primary study references.
- [Animation recipes](references/animation-recipes.md): visual-language choices, persistent items, continuous state, causal flow, timing and portrait composition.

- [Setup and migration](references/setup-and-migration.md): environment, 0.20–0.22 changes, math backends, output flags.
- [Mobjects](references/mobjects.md): text, formulas, code, layout, constructor pitfalls.
- [Animations](references/animations.md): identity, timing, paths, updaters.
- [Advanced](references/advanced.md): camera, 3D, programmatic rendering, diagnosis.
- [Storytelling](references/blog-patterns.md): choose a progression and review the explanation.

References are loaded by task, not all at once. Runnable examples are the source of truth for complete patterns; documentation avoids maintaining duplicate copies of those scenes.

[Project research and adoption decisions](docs/research/animation-projects-2026-10-26.md) records which upstream ideas we adopted or deferred. See also [formula mechanisms](docs/research/formula-and-preview-projects-2026-10-26.md) and [preview feedback](docs/research/preview-feedback-projects-2026-10-26.md).

[Render-feedback research](docs/research/render-feedback-evaluation-2026-10-26.md) and a [fresh-session heap-repair trial](docs/evaluations/heap-repair-20261026/review.md) separate a concrete generated result from unmeasured general quality claims.

The [30-project animation craft study](docs/research/animation-craft-2026-10-29.md) records this round's sources and concrete integrations. Its [verification record](docs/evaluations/animation-craft-20261029/review.md) distinguishes tested mechanisms and sampled frames from general aesthetic or teaching effectiveness.


The [2026-10-30 local regression](docs/evaluations/full-craft-regression-20261030/report.json) rendered and decoded 28 scenes, including Typst; the optional TeX scene was skipped. It covers Cairo on the recorded local environment, not general visual acceptance.

## Inspect the refinements

These records include source snapshots and sampled before/after frames. They show specific improvements, not a general aesthetic benchmark or proof that every generated animation will match them.

| Mechanism | Concrete review |
|---|---|
| Readable waves at small playback width | [Interference typography and hierarchy](docs/evaluations/interference-phone-20261029/review.md) |
| Identity during sorting | [Equal-value merge](docs/evaluations/merge-stability-20261030/review.md), [moving quicksort bars](docs/evaluations/quicksort-craft-20261030/review.md) |
| Geometric explanation with a useful conclusion | [Vector coordinates](docs/evaluations/vector-craft-20261030/review.md), [area scaling](docs/evaluations/continuous-craft-20261029/review.md) |
| Continuous handoff and 3D composition | [Circle to wave](docs/evaluations/continuous-transition-20261029/review.md), [exploded layers](docs/evaluations/three-d-craft-20261029/review.md) |
| New-task transfer and its remaining gaps | [Aperture first pass and revision](docs/evaluations/aperture-forward-20261029/review.md) |

[Source evidence and license audit](docs/research/source-evidence-audit-2026-10-30.md) records checked upstream license files and the migration of raw research responses to ignored local archives.

## License

MIT. See [LICENSE](LICENSE).
