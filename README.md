# Wiegand's Tree Sales Assistant — POC v15

## Fixes the broad-choice crash

The v14 broad-choice screen accidentally read from the pre-evaluation `candidates` table. Match fields such as `match_status` exist only after candidates are evaluated.

v15 now:
- builds match results in `evaluated`;
- reads broad choices from `evaluated`;
- keeps the required match columns even when a search returns zero candidates;
- retains the criteria → broad choices → cultivar review workflow.
