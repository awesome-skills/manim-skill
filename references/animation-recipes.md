# Animation craft recipes

Read the matching branch when choosing a visual language, choreographing a specific
relationship, or adapting an explanation to portrait. These are CE-native patterns,
not a fixed skin. Complete runnable sources live in `examples/`.

## Choose the visual language from the subject

Before rendering, choose background/ink, a quiet structural color, semantic accents,
type sizes, and margins in the scene. Keep these as a few named values; an application
theme framework is unnecessary for a single clip.

| Subject | Useful starting composition | Runnable example |
|---|---|---|
| Discrete values, comparisons, reorderings | Light editorial canvas; outlined cards; color tied to origin; stable source and destination rows | `merge_step.py`: `MergeStep` |
| Waves, functions, continuous change | Dark field; subdued axes; aligned traces; one bright result; fixed scales | `wave_superposition.py`: `WaveSuperposition` |
| Requests, flows, dependency chains | Clear route with a small moving token; destination responds on arrival; brief local emphasis | `packet_journey.py`: `PacketJourney` |
| Geometric correspondence | Large central geometry; subdued reference/ghost; labels travel with the represented object | `visual_story.py`: `VectorStory` |
| Algebraic derivation | Stable equals sign; separately identified repeated terms; add, cancel, then reflow | `typst_derivation.py`: `TypstDerivation` |

For typography, explicitly choose an installed font or a Pango generic family
(`sans-serif`/`serif`, with `warn_missing_font=False` for generic families). Inspect
the resolved glyphs. A font name is not a distributed font. Set text size for the
actual playback size: if a paragraph needs shrinking, split the shot or shorten it.
Choose color and type to fit the user's style; the sample palettes are alternatives.

## Discrete items: move identity, not just appearance

For sorting, queues, caches or matching, separate the data event from its depiction.
Store a mobject by stable item ID; its array position is not its identity. Repeated
values need separate IDs. Move the whole card (shape + value + identifying label)
along one path, then update the logical position. A changed value or replacement
object is a different operation and should be animated accordingly.

In `MergeStep`, `(source_run, source_index)` identifies each card. `merge_trace`
computes the stable merge, and cards physically travel into output slots. This is
different from morphing each slot's numeral to the next snapshot. Use the latter
only when the visual claim is a changing value at a fixed location.

If the explanation claims stability, include equal values in the actual scene.
`MergeStep` uses a 5 in each run, retains L/R origin labels, and pauses on the tie
before taking the left item. Here the left run precedes the right run in the
original sequence. The final adjacent 5s retain that order. A sorted result with
only distinct values cannot demonstrate stability. Keep decision text still
until the decision changes, rather than replaying the same transition each step.

Reserve a motion lane between rows. For a cubic path, place its two control points
inside that lane, then inspect the card's full bounding box at intermediate times.
Plan for labels and arrowheads, not only the center. After the operation completes,
bring the result into the focal area instead of leaving an empty source region dominant.

For a bar swap, move the existing bar and its numeral together without changing
height. `QuickSortBars.move_swap` uses shallow offset paths, then reorders the
mobject references to match the event positions. Role colors may change with
the algorithm state; they do not identify an immutable item. Inspect crossings
for occlusion and leave space above and below the baseline. Replace a discrete
decision sentence directly instead of morphing unrelated letters into each other.

For elimination or search, mark the remaining interval or count, and place the
ordering/constraint that justifies exclusion beside the discarded region. Dimming
items shows what changed; the visible relationship explains why it is valid.

For a geometric explanation, let the ending add information. `VectorStory`
keeps the head-to-tail action, states the input coordinates, and resolves them
into `(4, 3)` instead of ending with the tautology `a + b = a + b`. Arrow endpoints,
projection guides, and displayed coordinates come from the same input tuples.
Keep the geometric proof visible while the numeric result appears; the formula
should reinforce the action rather than replace it with an unrelated title card.

## Separate the clock from the motion curve

`examples/motion_timing.py` uses one linear four-second tracker for two equal
paths. One row maps progress directly; the other uses cubic Hermite progress
`3t² - 2t³`, with zero endpoint velocity and no overshoot. Its replay leaves marks
at equal half-second intervals, making the speed difference visible through spacing.
Do not apply a second easing to the tracker: that would alter both the shared clock
and the intended position curve. An explicit fade/reset separates the two trials.

Use gentle acceleration for a positional handoff when speed has no physical meaning.
Keep physical simulation time linear; motion style must not distort measured speed,
energy or event timing. A soft endpoint is a design choice, not a universal quality
upgrade, and these equally spaced time marks are explanatory evidence rather than
particles added for decoration.

## Continuous state: derive the whole frame from one value

For a Bézier construction, expose the successive interpolations instead of morphing
the control polygon into the final curve. In `bezier_construction.py`, two points
take the same fraction along adjacent guides; a third point takes that fraction on
the line joining them. One tracker drives both levels and the partial trace. The
control point remains visible as a handle, not a point the curve must pass through.
The displayed fraction is a curve parameter, not distance traveled: linear parameter
progress does not generally give constant speed along the path. Use arc-length-based
sampling when constant spatial speed is actually part of the requested behavior.

For a phase, time, angle or interpolation parameter, use a `ValueTracker` and derive
all dependent geometry from it. Freeze coordinate scales and comparison baselines.
In `WaveSuperposition`, one phase controls B and A+B; the probe uses one x for all
three traces. The sum is computed from the same samples, including transition frames.

Choose a mathematically valid intermediate state. A rigid rotation should use
rotation throughout; interpolating vertex positions can shrink the object. A
monotone counter or progress bar should not overshoot. If animation shows a physical
time variable, use `linear`; ease a parameter only when speed carries no physical claim.
Clear updaters once their dynamic relationship is no longer needed.

## Causality: route, travel, arrival, response

For a pipeline, establish endpoints and the route first. Move a token along that
route, then emphasize the destination or reveal its result. Simultaneously flashing
all nodes makes a sequential dependency look parallel. `PacketJourney` starts the
destination's emphasis after arrival; it does not claim a measured network latency.

For a fan-out that really is parallel, stagger only the introduction of branches;
execute the parallel work together. Explain what a token means (request, value,
signal) before reusing the same visual for another meaning.

## Timing: distinguish delay from duration

### Carry a visual anchor across scenes

For a connected explanation, choose what the viewer should keep tracking: an object,
a coordinate, or a relationship. Hold its state while moving the composition into
the next layout, then reveal the new representation. In `circle_to_wave.py`, the
same orbit and point move left after one turn; their phase is held during the move.
Only then does a second point record the orbit's height against phase. A shared
tracker keeps the projection horizontal throughout the recording.

This is a change of representation, so retain enough of the source to explain the
mapping. A decorative full-screen wipe is better suited to an actual chapter break;
do not use it to hide a missing correspondence. Clear the old heading before the
new one appears, and check transition midpoints for the anchor's full bounds.
Thin relationship lines can disappear at phone size even when readable in the
master render. Axis labels belong outside the entire moving curve envelope.

Choose timings by action: an entrance can be brief, a comparison needs a readable
hold, a first transfer needs tracking time, repeated transfers can accelerate.
These are starting ranges to preview, not delivery constraints:

| Beat | Starting range | Motion |
|---|---|---|
| Label entrance / replacement | 0.2–0.5 s | Fade or small translation; stable final baseline |
| First meaningful transfer | 0.8–1.4 s | Smooth start/stop, visible path |
| Repeated familiar transfer | 0.4–0.8 s | Same motion language, shorter hold |
| New conclusion | 1–2 s or longer for reading | Hold the geometry that proves it |

When unrelated captions occupy the same baseline, use a short `Succession(FadeOut(old),
FadeIn(new))` or separate plays. Check its midpoint: simultaneous crossfades can
superimpose readable glyphs even when both endpoint frames are clean.

Use `rate_functions.ease_out_cubic` for an arriving object's deceleration,
`smooth` for a deliberate transfer, and `linear` for steady traversal. Bounce is
appropriate for an elastic subject or a small decorative response; keep measured
values and comparison geometry exact. Preview the shape of the motion, not just its endpoints.

CE `LaggedStart(..., lag_ratio=r)` expresses a **relative** start offset, not a delay
in seconds. For n equal animations of duration d with no outer rescaling, total time
is `d * (1 + (n - 1) * r)`. An explicit outer `run_time` rescales the group. Choose
reveal order to match reading or causal order; center-out is useful for symmetric
geometry, not automatically for a numbered process. Use sections with semantic names
so a later timing adjustment has a clear home.

## Portrait is a different composition

Initialize matching scene-unit dimensions before the camera is constructed, then
measure the camera's actual frame. In Cairo, changing only pixel resolution keeps
frame width and adjusts camera height; global `config.frame_height` may still reflect
the original frame. `PacketJourney.__init__` uses a scoped `tempconfig` to establish
the intended frame width before `super().__init__`, without leaking global changes.
Switch horizontal chains to vertical routes, reduce simultaneous context and wrap
captions into short lines. Keep readable type instead of scaling a full landscape
canvas down. `PacketJourney` demonstrates both compositions. `MotionTiming` also
supports 16:9 and 9:16: it retains two stacked comparison tracks, derives their
length from available width, breaks title/captions into meaningful lines, and
adjusts dot/mark sizes so nearby endpoint samples remain distinguishable. Its
normalized progress and four-second timing remain the same. Other recipes need
deliberate recomposition for portrait; arbitrary aspect ratios are not validated.

```bash
uv run python -m manim render -qm --resolution 720,1280 examples/packet_journey.py PacketJourney
uv run python -m manim render -qm --resolution 720,1280 examples/motion_timing.py MotionTiming
```

## Review the transitions that can fail

Pick times from the shot list or actual clip. For a transfer, inspect departure,
midpoint, arrival and nearby frames; for a loop, inspect both sides of the seam.
The inspector's `--around` samples a neighborhood in the existing encoded video:

```bash
uv run python scripts/video_inspection.py scene.mp4 --around 4.2 --radius 0.3 --samples 5 --output verification/transition
```

The radius must stay within the clip; invalid times fail rather than silently clamp.
Open `review.html` to seek bookmarks and play the same video at 1×. Native browser
seeking is a navigation aid; PNG/JSON samples record decoded presentation timestamps.
Record issues as `time → visible problem → change → recheck`, keeping a before/after
artifact when claiming an improvement. Review a final full-quality render as well:
fonts, aspect ratio or timing changes can invalidate a draft review.

## Provenance

These CE recipes are original implementations informed by [the 30-project study](../docs/research/animation-craft-2026-10-29.md).
Specific mechanisms studied include [Motion Canvas sequencing](https://github.com/motion-canvas/motion-canvas/blob/main/packages/core/src/flow/sequence.ts),
[Anime.js stagger origins](https://github.com/juliangarnier/anime/blob/master/src/utils/stagger.js),
[Motion shared-element identity](https://github.com/motiondivision/motion/blob/main/dev/html/public/animate-layout/shared-element-basic.html),
and [JAnim sub-timelines](https://github.com/jkjkil4/JAnim/blob/main/doc/source/tutorials/sub_timeline.rst).
These are conceptual translations, not API compatibility or copied implementations.

## Data becoming a summary

For counts, preserve each observation through grouping and aggregation. Give records
stable IDs independent of their value or category. Group first, then stack equal-height
units on a shared baseline; label counts after the units settle. Preserve ordering within
each group so records do not unnecessarily cross. If changing position and shape together
causes overlap, arrange the units first and change their width afterward. A `Transform` from each
record to its own unit makes the connection visible. Generate labels and winners from
the data, and identify invented demonstration data on screen.

`examples/data_to_decision.py` demonstrates 24 original synthetic records, grouped into
6 / 10 / 8 and stacked into count bars. Units remain visible in the conclusion. This is
an instructional count visualization; moving many points is not a useful default for
an already-understood dashboard. For a mean, sum or proportion, design the corresponding
operation rather than reusing count stacking with a different caption.

This mechanism was informed by [Datamations grouping](https://github.com/microsoft/datamations/blob/main/R/prep_specs_group_by.R)
and [count decomposition](https://github.com/microsoft/datamations/blob/main/R/prep_specs_count.R):
its group state retains record IDs and count separates grouping from summarizing.
The CE scene is an original implementation without the R/JavaScript runtime.

## Metaphors must preserve operations

A visual analogy can make a technical topic approachable, but check what each visible
action teaches. In a cache-read explanation, returning data normally means copying it:
keep the cached item while its response travels. Identify a different requested key when
contrasting hit and miss. Show cache fill as the selected policy, not an inevitable property
of all caches. Moving the only book off a shelf accidentally teaches a destructive read.
This was an observed failure in a fresh Chinese cache-animation trial, corrected after review.

Apply the same question to other metaphors: does the action copy, move, consume, merge or
reference the object? Use separate identities for copies and retain the correct source state.
