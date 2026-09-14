# Wiegand's Michigan Tree Finder — POC v5.1

## v5.1 reliability fix
The app now checks the CSV schema when it starts.

If GitHub or Streamlit temporarily serves an older tree_database.csv that does not yet contain:
- preferred_soil
- fall_color
- growth_rate
- native_status
- moisture_notes
- photo/source fields

the app will fill safe placeholder values instead of crashing with a KeyError.

## Recommended update
Upload all four files from this package to the existing GitHub repository:
- app.py
- tree_database.csv
- requirements.txt
- README.md

Then commit the changes. Streamlit should redeploy automatically.
