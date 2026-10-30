# Aesthetic refinement for explanatory animation

Use when a user asks for beautiful, refined, polished or premium-looking results.
Treat this as a separate design objective alongside explanatory correctness. A successful
render, many effects, a dark palette or high resolution does not establish visual quality.

## Choose a direction before styling

Write a short art-direction sentence in working notes: subject, intended feeling,
primary visual object, type roles, palette roles and motion character. For example:
“An editorial field study of interference: warm paper, ink result, blue/coral inputs,
large result amplitude, stable plots and deliberate phase changes.” This is the direction
of `examples/interference_study.py`, not a default skin for every topic.

Choose a language that supports the content:

| Direction | Useful devices | Common failure |
|---|---|---|
| Editorial / scientific | Asymmetric grid, generous margins, serif title + plain annotations, thin rules | Tiny labels or decorative magazine furniture overpower the experiment |
| Technical / instrument | Dark field, precise grid, tabular values, restrained luminous accent | Every item glows; panels obscure the actual relationships |
| Geometric / playful | Strong shapes, few saturated colors, responsive motion | Bounce and overshoot imply false intermediate values |

Borrow principles from references, not an entire signature. Record whether you inspected
source code, a still or moving footage. A homepage screenshot supports observations
about layout and hierarchy, not conclusions about its animation pacing.

## Design three states, then their transitions

Lay out the opening, densest state and conclusion before building the full timeline.
At the actual delivery size, check:

1. **Hierarchy:** One clear first read, a supporting relationship, then annotation.
   Assign visual weight with size, contrast and position. Do not make all labels equally loud.
2. **Typography:** Give each size a role. Use a small consistent set of sizes and
   explicit font families. Keep titles, values and supporting copy distinct. Check fallback
   fonts, Chinese glyph coverage, punctuation, digit alignment and line breaks in rendered frames.
3. **Spacing:** Use shared anchors and a repeatable spacing unit. Align labels optically
   with their objects. Reserve room for widest values and full motion paths, including extrema.
4. **Color:** Define background, primary ink, secondary ink and semantic accents. Keep an
   object's identity across shots. Inspect without relying on hue alone; weak contrast is
   not refinement. A restrained palette still needs readable secondary text.
5. **Surface:** Use line weight and a quiet fill to separate data from scaffolding.
   Add texture, shadows or glow only if they express material, depth or attention. Do not
   add random particles behind an explanation just to fill negative space.
6. **Motion:** Establish the subject, change it, then let the consequence register.
   Stable labels and axes reduce visual noise. Match start/stop character across shots;
   use continuous motion for continuous state. Change unrelated text sequentially if
   crossfading makes two lines overlap.
7. **Finish:** Check cramped edges, near-tangencies, jittering numbers, inconsistent strokes,
   one-frame jumps and premature exits. These small defects can undermine an otherwise good layout.

Do not enlarge a result curve independently when viewers compare amplitudes. Emphasize it
with stroke, placement or a measured value while preserving the common scale. For an
unequal pair of opposing waves, show the nonzero remainder rather than a false flat line.

When force arrows represent magnitudes, use one length scale for all compared
forces. A statement that two forces are equal conflicts with visibly unequal
arrows unless the drawing is explicitly schematic. For a quasi-static lever,
keep the load and its arm fixed, move the effort position continuously, and derive
its force from the same balance relation. Put dimension lines and their labels
in channels clear of the support. State the idealized balance conditions; arbitrary
tilting is not a substitute for a consistent dynamical model. These checks address
observed failures in a Chinese lever-generation trial, not a requirement to add a
physics engine or force diagram to every animation.

## Compare and refine

For a multi-beat lesson, keep a short shot contract: the question, the visible evidence,
the quantity held fixed, and the conclusion for each beat. Reuse the same alignment
anchors, colors and object scales so chapter changes do not require relearning the
diagram. Give each beat one job; a longer clip needs more evidence, not repeated holds.
`examples/damping_story.py` establishes a release, compares two systems with the same
initial conditions, then freezes at a labeled time to explain energy remaining.

Distinguish physical time from presentation time. Use linear progression while showing
a physical simulation. A reset for a controlled comparison should be explicit (hide,
reset, re-establish both starts), not an unexplained jump in position. If the concluding
shot freezes a system that would keep moving, label the snapshot time. Motion styling
must not silently change the experiment's initial velocity, damping or measured energy.

Keep a baseline. Compare the same semantic state, not merely the same timestamp or the
most flattering frame from each version. State what changed and what tradeoff it introduces.
The editorial interference example shares the wave experiment's 1.00/0.75 inputs and
0 → half-cycle → full-cycle phase trajectory. It emphasizes amplitude; the original
`wave_superposition.py` spends time explaining pointwise addition with a probe. It is a
related art-direction study, not a controlled experiment isolating styling alone.

Review at intended playback size, then inspect full-resolution details. Sample motion
midpoints and neighborhoods around text changes, as well as settled states. Fix the most
visible defect and rerender before adding more effects. Keep a small before/after record:
what looked wrong, what changed, what frames were checked, and what remains uncertain.

Aesthetic acceptance should distinguish composition, legibility, motion rhythm and
explanatory value. Record concrete observations and human preference where available.
Do not invent a universal “premium score” or treat automated decode tests as taste validation.

## Inspect at the delivery width

A large contact sheet can hide a legibility failure. In addition to full-resolution frames,
produce a second sheet at the intended display width. For example:

```bash
python scripts/video_inspection.py scene.mp4 --at 2 --at 6 --at 12 \
  --preview-width 360 --columns 1 --output verification/phone
```

The preview preserves the video's aspect ratio, including portrait; saved source frames
remain full resolution. Review the image at native pixel size. Distinguish essential
labels from optional metadata. If essential labels shrink beyond comfortable reading,
shorten them, increase their hierarchy or recompose the shot. Raising export resolution
alone leaves their apparent size unchanged. Preview pixel width is a diagnostic, not a
physical-device, eyesight or accessibility certification.

For example, the data-count scene's first preview made category names too small. The
revision enlarges categories, gives the count bars more height, and shortens the footer.
The Chinese cache trial similarly needed larger item identities and shorter location labels.

Revisit earlier “polished” examples at the same delivery width. The first editorial
interference study used 14–19 point supporting text that looked orderly in a large
frame but was too small at 360px. Its later revision removed ornamental running
headers/footers, shortened secondary copy, enlarged input and phase labels, and kept
the data, scales and timeline unchanged for a direct comparison. Preserve what a
number measures when shortening copy: “Sum amplitude” is clearer than “Amplitude”.

## Let typography carry a precise claim

Large type can be the primary graphic when a short claim is the point. Keep the
unit or role next to the large numeral: “2× the side” and “4× the area” are distinct
quantities. Stage the visible proof between them, and change the headline after the
geometry establishes it. Preserve a physical anchor during growth so the viewer can
compare sizes. `examples/area_scale_story.py` keeps the square's lower-left corner,
expands the outline and fills it with four equal unit squares.

Treat word-level motion as semantic emphasis. Use the subject's meaningful phrases
as groups rather than automatically staggering every glyph, especially Chinese text.
Coldtype's [timed-word example](https://github.com/coldtype/coldtype/blob/main/examples/animations/ascii_words.py)
illustrates grouping text and styling timed spans; its engine/font assets are not needed
for this CE example. Browser samples of HyperFrames' kinetic-type showcase also show
large differences of scale and word/object pairing; sampled stills alone do not establish
its timing or suitability for a technical explanation.
