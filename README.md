# Wiegand's Tree Sales Assistant — POC v12

## Mature-size match logic

Height and width now use three states:

- **Fits** — the entire expected mature range is within the customer's maximum.
- **May Fit** — the lower end is within the customer's maximum, but the upper end exceeds it.
- **Exceeds** — even the lower end exceeds the customer's maximum.

Examples:
- Customer max height 30 ft; tree 20–30 ft → Fits.
- Customer max height 30 ft; tree 30–40 ft → May Fit and appears as a Partial Match.
- Customer max height 30 ft; tree 35–45 ft → Exceeds for height.

The same logic applies to mature width.

A Full Match still requires every selected criterion to fully fit. Borderline May Fit cases remain visible as useful Partial Matches.
