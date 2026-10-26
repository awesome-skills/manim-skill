# Camera, 3D, and programmatic rendering

Read only the relevant section. For output flags and environment issues use [setup and migration](setup-and-migration.md).

## Moving camera (Cairo)

`self.camera.frame` belongs to `MovingCameraScene`, not ordinary `Scene`.

```python
from manim import *

class Focus(MovingCameraScene):
    def construct(self):
        square = Square().shift(LEFT * 2)
        dot = Dot().shift(RIGHT * 2)
        self.add(square, dot)
        self.camera.frame.save_state()
        self.play(self.camera.frame.animate.move_to(dot).set(width=3))
        self.wait(0.5)
        self.play(Restore(self.camera.frame))
```

Keep text readable at both zoom levels. Zooming changes which scene-unit bounds are visible; checks against the initial frame alone are insufficient. Use `ZoomedScene` for an inset, and verify that the inset does not cover important content.

## 3D

```python
class Orbit(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=65 * DEGREES, theta=-45 * DEGREES)
        axes = ThreeDAxes()
        sphere = Sphere(radius=1, resolution=(12, 24), color=BLUE)
        self.add(axes, sphere)
        label = Text("Orbit", font_size=30).to_corner(UL)
        self.add_fixed_in_frame_mobjects(label)
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(2)
        self.stop_ambient_camera_rotation()
```

Start with modest surface resolution. Use `add_fixed_in_frame_mobjects` for screen-space labels. `ThreeDScene` and OpenGL camera APIs differ; do not substitute a ManimGL camera snippet into a CE scene. Cairo 3D is a useful portable check, not proof of OpenGL behavior.

## Derived geometry

```python
tracker = ValueTracker(0)
axes = Axes(x_range=[0, 4, 1], y_range=[0, 4, 1])
dot = always_redraw(lambda: Dot(axes.c2p(tracker.get_value(), tracker.get_value())))
self.add(axes, dot)
self.play(tracker.animate.set_value(3), run_time=2)
dot.clear_updaters()
```

Use trackers as the source of truth. Ensure a dependent curve, label, and marker use the same coordinates. Avoid caching a connector endpoint before moving its target.

## Programmatic rendering

```python
from manim import tempconfig
from examples.basic_scene import BasicScene

with tempconfig({"quality": "low_quality", "media_dir": "media", "format": "mp4"}):
    scene = BasicScene()
    scene.render()
    artifact = scene.renderer.file_writer.final_file_path
```

Set frame/pixel dimensions, renderer, and output before scene creation. For portrait video set both pixel aspect and scene frame aspect (for example 1080×1920 pixels and 4.5×8 scene units), then recompose the content. Increasing resolution does not fix clipping.

In 0.22 a `Manager` coordinates rendering. Prefer public scene APIs rather than patching renderers/file writers or overriding `render`. Ordinary `setup`, `construct`, and `tear_down` overrides remain supported.

## Notebook and sections

```python
%%manim -ql NotebookExample
class NotebookExample(Scene):
    def construct(self):
        self.play(Create(Circle()))
```

The cell magic is for notebooks, not Python files. Keep generated media out of source control. Render named sections with `--save_sections` when separate clips are required; inspect the section files as well as the full output.

## Performance and reproducibility

Use a low quality preview before production resolution. Choose `--seed` for random examples. Keep deterministic input data when comparing renders. Manim caches partial movies; `manim cache clear scene.py SceneName` is the 0.22 cache command. Use `--disable_caching` when diagnosing a stale render, not as an unconditional production setting.

Parallel encoding (`--max-inflight-encoders`, `--encoder-queue-size`) trades memory for overlap with rendering. Measure first. Avoid recommending large values on every task.

## Diagnosis

| Symptom | First check |
|---|---|
| Missing `manim` | Correct interpreter/environment; `python -m manim --version` |
| Pango/Cairo build failure | Native dependencies and pkg-config search path |
| TeX executable missing | Select/install requested math backend; do not remove formulas silently |
| Blank/missing glyphs | Font coverage, actual rendered characters |
| `camera.frame` missing | Scene type and renderer |
| Blank last-frame PNG | Scene may intentionally end with FadeOut; inspect earlier frames |
| Unexpected output directory | CLI/config precedence; use `--media_dir` |
| No separate section files | `--save_sections`, section names, and animation calls |
| Render passes but explanation looks wrong | Inspect timeline, object identities, positions, and actual states |

When reporting a failure, include the exact command, version, relevant traceback, and what could/could not be verified. Avoid modifying unrelated global configuration to fix a local scene.
