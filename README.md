# Acme Nursery Tree Sales Assistant — POC v35

## Full Screen Comparison correction
The Find a Tree area is implemented as the Streamlit sidebar, not the right-side criteria panel. In Full Screen Comparison mode v35 now explicitly removes:
- the entire Find a Tree sidebar
- the sidebar collapse control
- the Acme Nursery hero/header area
- Streamlit header/tool chrome where possible
- extra page margins

The Quick Comparison remains with the red Back to Tree Types and Exit Full Screen controls and receives the full available application width.
