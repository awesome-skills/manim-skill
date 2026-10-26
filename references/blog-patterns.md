# Storytelling patterns for technical animations

Use animation when the order or change explains something that a still cannot. A standalone video may need a title and a conclusion; a blog illustration can rely on nearby prose. Match the destination rather than imposing one universal format.

## Choose a pattern

| Explanation | Pattern | Starting point |
|---|---|---|
| Input becomes output | Nodes appear in causal order, then highlight progress | `examples/flowchart.py`: `SimpleFlow`, `ProcessHighlight` |
| A condition selects a branch | Show the condition, emphasize the taken branch, distinguish failure | `examples/flowchart.py`: `BranchingFlow` |
| State evolves | Stable node positions, labeled transitions, a readable active marker | `examples/state_diagram.py`: `SimpleStates`, `StateWithLabels` |
| Position determines identity | Aligned rows, explicit indices, contrasting mismatch labels | `examples/state_diagram.py`: `LinkedListMismatch` |
| Algorithm changes data | Separate algorithm events from visual objects; replay correct states | `examples/quicksort.py`: `QuickSortBars` |
| Formula or curve changes | Stable axes/terms, trackers, meaningful correspondence | `examples/basic_scene.py`: `GraphExample`; `examples/typst_scene.py` |
| Focus moves within a larger system | Establish whole composition, zoom, return | `examples/advanced_scene.py`: `CameraFocus` |

Use the runnable example as the source of truth. Copy only the relevant scene and its helpers; this file intentionally avoids maintaining a second copy of each implementation.

## Plan the visual progression

- Start with the minimum context needed to interpret the action.
- Give the viewer time to locate the changing object before moving it.
- Keep stable objects still; motion should express change, correspondence, or focus.
- End with an interpretable result and a short hold. If looping, make the reset explicit or connect it smoothly.
- Prefer a few meaningful colors with text/symbol reinforcement. Color alone should not carry success, failure, or active state.

For algorithm examples, derive events from computation rather than typing a plausible sequence by hand. Verify the data/result independently of the animation. Choose a small input for a short embed; the quicksort showcase deliberately uses a longer example and should not be treated as a default duration.

## Layout and delivery

At the target size, text must be readable without fullscreen playback. Put related labels near their objects, reserve margins, and keep connector paths unambiguous. If the composition is too dense, split the explanation rather than shrinking every label.

A browser-friendly MP4 often provides better quality per byte than a GIF. Use GIF when the destination requires it; inspect its size, palette, and loop behavior. Transparent video needs a compatible format and player; do not promise that all platforms will display alpha correctly.

Inspect more than the last frame. Useful checkpoints include:

1. First meaningful state after the intro.
2. A transition with the most simultaneous motion.
3. The densest/intermediate state.
4. The final result.

A contact sheet helps find clipping and missing labels; playback is still needed to judge pacing and smoothness. If only screenshots were inspected, say so. Deliver source plus reproducible render command, not just a video with no way to edit it.
