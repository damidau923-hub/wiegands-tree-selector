# Wiegand's Michigan Tree Finder — POC v8

## New match system
- Removes the artificial percentage match score.
- **FULL MATCH** = meets every selected requirement.
- **PARTIAL MATCH** = meets some, but not all, selected requirements.
- Partial-match cards explicitly show both what matches and what does not.
- A selected tree type remains the search category, preventing unrelated tree types from flooding partial results.
- Height, width, flowering, and sun determine Full vs. Partial Match.
- Trees that meet none of the selected requirements are not shown.
- Wiegand's priority status can influence ordering, but never changes Full vs. Partial Match.
- The results control is now **Results per section**.

Photo/reference behavior from v7 is retained.
