# Wiegand's Michigan Tree Finder — POC

This is a small Streamlit proof of concept.

## What it does
- Lets a user choose tree type, mature height, mature width, flowering preference, and sun needs.
- Ranks the best matches from a starter Michigan tree database.
- Shows a match percentage and explains why each recommendation fits.
- Separates the data (`tree_database.csv`) from the application (`app.py`).
- Includes separate categories for **Hydrangea on Standard** and **Lilac on Standard**.
- Includes a rule-based natural-language request helper as a placeholder for a future AI parser.

## Run locally
1. Install Python 3.10 or newer.
2. In this folder, run:
   `pip install -r requirements.txt`
3. Start the app:
   `streamlit run app.py`

## Deploy
These same files can be deployed to Streamlit Community Cloud or another Python web host.

## Next steps
- Replace provisional Wiegand's availability with the actual Wiegand's tree product database.
- Add real tree photos/image URLs.
- Add more cultivars and attributes.
- Connect a true AI parser for natural-language requests.
- Later connect to live inventory and/or the landscape designer.
