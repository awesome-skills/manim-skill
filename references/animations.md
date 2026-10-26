# Animation choices and object identity

## Core operations

- `Create`: draw strokes/geometry; `Write`: reveal text paths; `FadeIn`/`FadeOut`: introduce/remove content without implying shape correspondence.
- `Transform(source, target)`: source remains the live scene object with the target's geometry.
- `ReplacementTransform(source, target)`: source leaves and target becomes the live object.
- `TransformMatchingTex` / `TransformMatchingShapes`: use when meaningful parts should correspond. Inspect grouping and matching; matching syntax does not guarantee a clear explanation.

```python
circle = Circle()
self.play(Create(circle))
square = Square()
self.play(Transform(circle, square))
self.play(circle.animate.shift(RIGHT))  # circle is still the live reference
```

A transformed object may retain its original Python type; avoid assuming a `Transform` changes its class. Use replacement when downstream behavior needs the target's type.

## Formula correspondence

Choose matching according to the meaning of the change:

| Case | Approach |
|---|---|
| LaTeX terms with unambiguous string identity | Split `MathTex` deliberately and use `TransformMatchingTex`; inspect repeated terms |
| Same-looking shapes whose geometry is the intended correspondence | `TransformMatchingShapes`; visual similarity does not establish mathematical identity |
| Repeated terms with different roles, or Typst subexpressions | Give each occurrence a label and map disjoint selections explicitly with `ReplacementTransform` |
| One expression contributes to several result terms | Use `TransformFromCopy` for the intended copies, then introduce any new operators explicitly |

`TransformMatchingTex` expects LaTeX objects/parts; it is not a generic adapter for `MathTypst`. In CE 0.22, Typst's named captures and `select` provide a public alternative. The complete example is `examples/typst_derivation.py`; selection and ownership details are in [mobjects](mobjects.md#math-backends).

Make the algebraic operation visible: to move an additive term across an equality, first show the same subtraction on both sides and then cancel. Clear cancellation marks before retained terms move through their former position; otherwise a moving term can appear falsely crossed out. A smooth path alone does not explain the change of sign. Treat this as an explanatory choice for the intended audience, not a requirement to expand every elementary step in an expert presentation.

## Timing and simultaneous mutations

```python
self.play(FadeIn(title), Create(axes), run_time=0.8)
self.play(LaggedStart(*[FadeIn(node) for node in nodes], lag_ratio=0.15))
self.play(dot.animate.shift(RIGHT).set_color(GREEN), run_time=1, rate_func=linear)
self.wait(0.5)
```

Chain transformations of one object on one `.animate` builder. Two animations writing the same object's geometry or style in the same `play` can conflict; combine them or sequence them. A group animation and an animation of its child can also overlap ownership.

Choose timing to communicate causality: establish the state, show the action, then hold the result. More simultaneous motion is not inherently clearer. Use `linear` for constant-speed traversal and ease curves for emphasis. Compare pacing at the final playback speed, not just in a contact sheet.

## Moving along a path

```python
path = ArcBetweenPoints(start, end, angle=PI / 3)
dot = Dot(path.get_start(), color=YELLOW)
self.play(FadeIn(dot))
self.play(MoveAlongPath(dot, path), run_time=1.2, rate_func=linear)
```

Start the marker on the path. If the conceptual origin/destination is a node center but the path terminates at its boundary, animate center-to-boundary and boundary-to-center explicitly, or keep the indicator on the edge. Otherwise it visibly teleports between transitions.

## Live values

```python
tracker = ValueTracker(0)
dot = Dot()
dot.add_updater(lambda mob: mob.move_to([tracker.get_value(), 0, 0]))
self.add(dot)
self.play(tracker.animate.set_value(3), run_time=2)
dot.clear_updaters()
```

An updater runs only when the object participates in scene updates. For elapsed-time motion use an updater accepting `(mob, dt)`; for derived geometry use `always_redraw`. Avoid rebuilding expensive text or a whole diagram on every frame unless it is necessary.

Since 0.20, `dot.always.next_to(square, UP)` is a convenience for maintaining a relationship. Standard `add_updater` remains useful for custom logic. Clear obsolete updaters before reusing objects.

For numeric readouts without TeX, use `Text` labels and update only when the displayed string changes. `DecimalNumber` is convenient when the chosen math backend is available, but is not a universal TeX-free substitute.

## Semantics before effects

A sorting animation must preserve the values and show correct comparisons/swaps; a process animation must not mark unfinished steps complete. Choose one meaning per color and reinforce it with labels. `Indicate`/`Circumscribe` emphasize existing content; flashing everything adds noise rather than explanation.

Use `self.next_section("name")` to label meaningful phases. Separate section video output requires `--save_sections`; naming sections alone does not promise separate files. Do not confuse sections with animation indices used by `-n`.

For API details, consult the [0.22 animation reference](https://docs.manim.community/en/v0.22.0/reference_index/animations.html).
