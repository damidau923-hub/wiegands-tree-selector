# Wiegand's Michigan Tree Finder — POC v3

## v3 fix
Sun exposure now uses overlapping horticultural ranges instead of exact text matching.

Examples:
- Partial Sun can match trees listed for Full Sun, Partial Sun, or Partial Shade.
- Partial Shade can match trees listed for Partial Sun, Partial Shade, or Shade.
- Shade remains more restrictive.

This specifically fixes cases like Redbud returning no matches when the user chooses Partial Sun.

## Update the live Streamlit app
Replace the existing repository files with:
- app.py
- tree_database.csv
- requirements.txt
- README.md

Commit the changes. Streamlit should redeploy the same app URL automatically.
