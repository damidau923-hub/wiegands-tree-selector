# Wiegand's Tree Sales Assistant — POC v11

## Michigan/regional mature-size audit

This version begins the cultivar-by-cultivar mature-size verification requested for the sales tool.

- All 45 entries now carry `size_basis`, `size_confidence`, and source fields.
- 12 entries have been updated/verified against Michigan or cold-climate/regional authoritative references.
- Remaining entries retain their starter dimensions but are explicitly marked **Needs verification** rather than being presented as Michigan-verified facts.
- Result cards now say **Expected Mature Height** and **Expected Mature Width**.
- Full/Partial Match calculations use the same expected mature-size values displayed on the card.
- The app identifies whether the size is researched or still a starter estimate.

This avoids pretending that a national nursery size is automatically a Michigan mature size. The next database pass should verify the remaining cultivars, ideally against Wiegand's supplier specifications plus Michigan/Upper Midwest references.
