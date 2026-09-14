# Wiegand's Michigan Tree Finder — POC v8.1

## Dimension display fix
- Mature height and width now use a dedicated formatter instead of Streamlit metric widgets.
- Every result card shows the complete range, for example **15 to 25 ft**.
- This prevents the upper bound from being visually truncated.
- Partial-match explanations now use the same wording: maximum mature height/width versus the customer's limit.
- All 45 database rows were validated for missing or reversed height/width bounds.

The Full Match / Partial Match logic from v8 is unchanged.
