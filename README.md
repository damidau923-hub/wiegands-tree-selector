# Wiegand's Michigan Tree Finder — POC v2

## Improvements in v2
- Cleaner Wiegand's-style interface.
- Hard maximum-height filter.
- Hard maximum-width filter.
- Tree type, flowering, and sun filters act as real requirements.
- Recommendation cards are ready for real photo URLs.
- Separate categories remain for Hydrangea on Standard and Lilac on Standard.
- Wiegand's priority status is only a ranking tie-breaker, not a fake availability claim.

## To update the live Streamlit app
Replace these files in the same GitHub repository:
- app.py
- tree_database.csv
- requirements.txt

Commit the changes. Streamlit should automatically redeploy the same app URL.

## Next major step
Connect the actual Wiegand's tree product list and populate the image_url column with approved product/tree photographs.
