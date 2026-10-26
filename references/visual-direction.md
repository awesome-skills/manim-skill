# Visual direction for explanatory animation

Read before storyboarding a new animation or improving its appearance. Use the user's style when specified. Otherwise choose a composition suited to the concept, rather than reproducing the same dashboard for every topic.

## Storyboard the insight

Write a compact shot list in the working notes: viewer question → visible action → insight → approximate duration. This is an authoring aid, not a mandatory approval gate. Design the hardest transition first; if the explanation needs a paragraph beside it, try a simpler visual action.

- **Reveal:** establish a question or an informative contrast with a concrete object, then reveal only the context needed for the next action.
- **Correspondence:** keep the same value, term or geometric object recognizable as its role changes. Move/copy it between representations; preserve its color and label. A copy communicates correspondence, not a second algorithm operation.
- **Consequence:** hold the resulting state long enough to see why the action mattered. On repeated operations, explain one fully and accelerate later repetitions while preserving correct states. A full tutorial may need every step at normal speed.
- **Resolution:** return to the question and show the answer in the objects themselves. A summary can reinforce it; it should not be the first place the explanation becomes clear.

For heap sort, a useful sequence is: reveal why a maximum belongs at the end → show the root/last swap → isolate the violated parent-child relation → visibly repair it → pull back to the shrinking heap and growing sorted suffix. Explain the heap property and build phase where the intended audience needs them. Avoid leaving every status label and rule visible throughout.

## Art direction

Choose a restrained palette, a type hierarchy, margins and a focal object before coding. Dark backgrounds and pastel accents are one option, not a required signature.

- Make the explanatory object dominant. Use nearby labels or a brief caption instead of a permanent wall of prose. Panels earn space when they help compare representations, not simply to fill the frame.
- Keep secondary geometry quieter: thin connectors, subdued grids and small annotations; keep essential structure legible. Reserve the strongest accent for the action the viewer should follow.
- Use color consistently across a diagram, its values and related formulas. Reinforce meaning through labels, position or shape. Color variety is not hierarchy.
- Compose the opening, the densest state and the conclusion deliberately. If content does not fit at readable size, reveal it in another shot instead of shrinking it all.
- Keep text crisp and stable. Fade between unrelated sentences; use matching transforms only for meaningful correspondence. Moving Chinese glyph fragments rarely helps explain an algorithm.

## Choreography

Attention moves before geometry: establish or emphasize the operands, perform the action, then let the result settle. Timings depend on novelty and reading load; avoid uniform durations for every beat.

- Animate related objects together only when their simultaneous change is the point. Otherwise stagger causally, using a small `LaggedStart` or separate `play` calls.
- Preserve object identity across shots. Prefer transforming an established diagram over clearing the whole scene and redrawing it. Keep spatial anchors still while the viewer tracks a change.
- Plan motion lanes as well as resting positions. For swaps, inspect the halfway frame and the widest separation; arc height can grow with distance and collide with index labels even when both endpoints fit.
- Let camera movement explain scale or focus. Establish the whole, move to a local relation, then return when the global effect matters. Use a static camera when the composition already explains the relationship.
- Use easings for deliberate starts/stops; constant-speed traversal when speed itself has meaning. Reserve flourishes, glows and flashes for a purpose the viewer can name.

`examples/visual_story.py` is an original, TeX-free CE example: two vectors start at the same origin, one moves head-to-tail, and the resultant emerges from the resulting endpoint. It demonstrates stable geometry, color correspondence, restrained layering and staged revelation, not a universal template.

## Editable timing

For a multi-beat scene, name the meaningful beats with CE `self.next_section("head_to_tail")`, as the example does. Keep the action for each beat together so changing its hold does not require editing unrelated choreography. Sections label the timeline; they do not implement audio synchronization. Use `--save_sections` only when separate clips/metadata are useful.

[Motion Canvas time events](https://motioncanvas.io/docs/time-events/) illustrate the value of naming semantic cues instead of scattering absolute timestamps. Adopt that authoring principle using CE sections; do not recreate its editor or install a TypeScript renderer. When narration is actually requested, consider [Manim Voiceover](https://voiceover.manim.community/en/stable/quickstart.html) for duration trackers and word bookmarks after checking the project environment and speech-service requirements. Silent scenes retain the existing dependencies.

## Visual iteration

Render the hardest few seconds cheaply before polishing the whole timeline. Inspect settled frames AND transition midpoints. At intended playback size ask:

- Can I immediately identify what to follow, and read its label?
- Does the transition show the claimed relationship without teleportation or false intermediate data?
- Do text, arrowheads, values and motion paths stay clear of each other?
- Does each pause allow the new idea to register, and do repetitions advance the explanation?

Use `python scripts/video_inspection.py scene.mp4 --at 6.8 --at 8 --columns 2 --output verification/review` to inspect chosen transition times in an existing rendered MP4 (replace the video and times). It decodes the same artifact rather than rerunning the scene, saves full-resolution PNGs and a multirow contact sheet, and records requested/actual presentation times, indices and the input hash. It selects the frame displayed at the requested time, not a future frame or an index estimated from average fps. The duration endpoint selects the last frame; out-of-range requests fail. Omit `--at` for five overview samples. Read `report.json` alongside the images; the tool deliberately leaves visual review unperformed.

Fix the most distracting failure, render that segment again, then review the whole video at normal speed when playback is available. Higher resolution fixes neither pacing nor composition. Record whether review covered still frames, sampled transition frames or actual playback; appearance remains a human judgment, not a render-test result.

## Studying 3Blue1Brown

Useful primary references:

- [ManimGL example scenes](https://github.com/3b1b/manim/blob/master/example_scenes.py): geometry-as-transformation, matched terms, trackers and live labels.
- [Video production workflow](https://github.com/3b1b/videos#workflow): interactive checkpoints and short iteration loops.
- [Laplace derivative scenes](https://github.com/3b1b/videos/blob/master/_2025/laplace/derivatives.py): study sequencing, term correspondence and changes in focus in the source. Source inspection alone does not establish the appearance or pacing of the rendered video.

The guidance above is our synthesis for CE. Reimplement the explanatory idea with public CE APIs; ManimGL imports, camera methods and matching APIs are not drop-in CE code. Keep experiments in the existing project's engine. These references do not require installing a second engine.

The ManimGL engine is MIT; the `videos` repository states CC BY-NC-SA 4.0 for its contents. Keep that boundary explicit when reusing upstream material. This skill's example is original and contains no upstream video code or assets; do not package those under this repository's MIT license or assume a link grants reuse rights.
