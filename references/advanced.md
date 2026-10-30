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

## Camera-led explanation

Use a camera move when changing the visible scale reveals something the wide shot cannot.
`examples/local_linearity.py` preserves one curve and tangent through two close views,
then restores the overview. It uses `MovingCameraScene` under Cairo and ordinary public
frame animations; no second scene or substitute geometry is introduced.

- Establish the wide view and the target before moving. A brief framing rectangle can
  connect the forthcoming close view to the overview.
- Save the overview frame once. Pan/zoom to the same world-space target and use `Restore`
  to return to that exact context rather than estimating the old position.
- Place annotations for the current view. Wide-shot text can leave before the move;
  introduce local labels after the camera settles, then remove them before changing scale.
  To keep their apparent size, scale world text by `current_frame_width / overview_width`.
  This is for labels created at a settled camera state, not a screen-fixed text API.
- Check the smallest frame bounds as well as the transition midpoint. Geometry may
  intentionally extend beyond a close crop; essential labels and focal objects should fit.
- Keep what is being measured fixed. A camera zoom must not rescale a curve independently
  of its tangent, or move the point while claiming to examine the same neighborhood.

CE `self.camera.auto_zoom(group, margin=...)` fits a group using its bounding box and the
current frame aspect. Include essential labels in the group if they must remain visible.
In the inspected 0.22 implementation, margin is added to the chosen fitted dimension;
it is not an explicit per-edge padding parameter. It applies to unrotated XY geometry.
For a deliberate constant target and two known scales, direct frame animation is clearer.

Source comparisons: [Motion Canvas Camera](https://github.com/motion-canvas/motion-canvas/blob/main/packages/2d/src/lib/components/Camera.ts)
separates center, zoom and reset and converts world coordinates to its scene; [CE moving-camera examples](https://github.com/ManimCommunity/manim/blob/main/manim/scene/moving_camera_scene.py)
show save/restore and group fitting. Their APIs differ; borrow the continuity principle,
not the engine-specific calls. This example uses original CE code.

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

For an explanatory 3D composition, establish the assembled object before separating
parts. `examples/exploded_layers.py` uses opaque equal-sized prisms, moves only their
centers, changes the camera angle while they are separated, and returns them to the
same stack. Text and the color legend remain in screen space. Keep a comparable
assembled view at both ends so an exploded diagram does not imply resized parts.

Check projected bounds at every planned camera angle. The first exploded-layer draft
overlapped its bottom legend after the camera turned; moving the legend to the side
resolved this without shrinking the main object. A world-space bounding box alone
does not catch that overlap. Use transparency only when it conveys something needed,
and inspect intersecting surfaces in the actual renderer. Pygfx's transparency demo
explicitly exercises intersecting planes where sorting is insufficient; that engine's
blend modes are not an API or guarantee supplied by Manim Cairo.

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
