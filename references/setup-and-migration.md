# Setup and migration

## Environment

Target: ManimCE 0.22.x on Python 3.11+. Retain an existing project's pinned version unless upgrading is part of the request. Use that version's documentation for API decisions.

For this repository:

```bash
uv sync --python 3.13 --extra typst
uv run python -m manim --version
uv run python -m manim checkhealth
```

For a separate new project, create an isolated environment and install the chosen version:

```bash
uv venv --python 3.13
uv pip install --python .venv/bin/python "manim>=0.22,<0.23"
.venv/bin/python -m manim checkhealth
```

On Windows use `.venv\Scripts\python.exe` instead. PowerShell can locate uv with `Get-Command uv`. A one-off run is `uv run --python 3.13 --with "manim==0.22.0" python -m manim --version`; it still needs the platform's native dependencies.

PyAV handles ordinary media encoding; a standalone FFmpeg executable is not required for core Manim rendering since 0.19. This does **not** eliminate Cairo/Pango, fonts, optional TeX tools, or graphics requirements for OpenGL. FFmpeg/ffprobe can still be useful for external conversion and inspection.

When native dependency installation is necessary, use the [official OS-specific instructions](https://docs.manim.community/en/stable/installation.html). On macOS the common prerequisites are `brew install cairo pango pkg-config`; on Ubuntu `libcairo2-dev libpango1.0-dev pkg-config` and build tools are common prerequisites. Diagnose the actual error before adding dependencies. A successful `checkhealth` does not verify all optional formula/font backends.

## Math choices

- `Text` / `MarkupText`: Pango; use for prose and simple numeric labels.
- `Tex` / `MathTex`: require a working TeX toolchain, including the selected compiler and `dvisvgm`. Keep raw strings for LaTeX.
- `Typst` / `MathTypst`: install `manim[typst]`; a full TeX distribution is unnecessary. Use Typst syntax. Current 0.22 public names are `Typst` and `MathTypst` (not `TypstMath`).

For non-math scenes, missing TeX need not block work. For requested formulas, prefer a working supported backend rather than replacing mathematical typesetting with unreadable plain text.

## Output in 0.22

Choose one primary artifact with `--format`:

| Format | Result |
|---|---|
| `auto` | Default MP4; transparent output uses MOV; a scene with no animation can produce PNG |
| `mp4`, `mov`, `webm` | Explicit video; use `auto`, `mov`, or `webm` for transparent output |
| `gif` | Animated GIF |
| `png` | Last frame only |
| `png-sequence` | Every frame |
| `none` | Evaluate scene without writing media |

`-p` previews the completed artifact with either renderer. `-l` / `--live-preview` is an OpenGL live window. OpenGL now writes files by default, so do not assume it only displays a window. An explicit video format requires `play` or `wait` calls. GIF does not support audio.

Migration from older switches:

| Old use | 0.22 replacement |
|---|---|
| `--write_to_movie` / `write_to_movie=True` | `format=auto` or an explicit video format |
| `write_to_movie=False` | `format=none` |
| `-g` / `--save_pngs` | `--format png-sequence` |
| `-i` / `--save_as_gif` | `--format gif` |
| `save_last_frame` in config file | `format=png`; CLI `-s` still works |
| `--force_window` | `--live-preview` |
| `--flush_cache` | `manim cache clear scene.py SceneName` |
| `--custom_folders` / `[custom_folders]` | Set individual output directory options under `[CLI]` |

Do not combine replacement formats as if they were independent flags. Use a separate render for a second artifact. `--dry_run` is still available; it does not prove encoding or visual quality.

Use explicit `--media_dir` for predictable output roots. In programmatic rendering, configure before creating the scene:

```python
from manim import tempconfig
from examples.basic_scene import BasicScene

with tempconfig({"quality": "low_quality", "media_dir": "media", "format": "mp4"}):
    scene = BasicScene()
    scene.render()
    print(scene.renderer.file_writer.final_file_path)
```

Scene output settings are captured at construction. Changing resolution after `super().__init__()` is too late. Avoid reaching into renderer/file-writer internals for lifecycle control: 0.22 introduced a `Manager`; public `Scene.play`, `render`, `next_section`, and sound APIs remain the supported interface.

## Relevant changes since 0.19

- 0.20 rewrote MathTex grouping/splitting, introduced `Mobject.always` and `--seed`, and removed some ImageMobject resampling modes. Review code relying on formula subobject indices or those image modes.
- 0.21 made Pygments authoritative for `Code` foreground/line-number colors. Use a custom Pygments `Style` when needed; `background_config` can still override background color. It added optional Typst and parallel encoding controls.
- 0.22 unified output selection, introduced the render `Manager`, and updated ManimPango to 0.7 for small-font kerning. Ordinary `construct` scenes do not need rewriting.

Performance claims from release notes are benchmark-specific. First reduce unnecessary geometry/updaters and render at low quality; try `--max-inflight-encoders` only when encoding is the measured bottleneck and memory allows it.

Sources: [0.20](https://docs.manim.community/en/stable/changelog/0.20.0-changelog.html), [0.21](https://docs.manim.community/en/stable/changelog/0.21.0-changelog.html), [0.22](https://docs.manim.community/en/stable/changelog/0.22.0-changelog.html).
