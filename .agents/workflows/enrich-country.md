---
description: Optional. Add artist home country via MusicBrainz to answer domestic vs international
---
1. Ask me two things before starting: my contact email for the MusicBrainz User-Agent, and how many top artists to look up (suggest 100 by appearances, then check what share of credits that covers).
2. Ask me to confirm the definition of domestic: artist's MusicBrainz country is the United Kingdom. Groups with mixed or missing data are `Unknown`.
3. Write `src/enrich_country.py`: read the artist list from the clean data, skip artists already in `data/external/artist_country.csv`, query MusicBrainz at no more than one request per second, store artist name, matched MusicBrainz name, country code, match score, source and lookup date. Handle timeouts and retry politely.
4. Add a review file `data/external/artist_country_review.csv` listing every low-confidence or ambiguous match so I can correct them by hand.
5. After my review, compute the domestic, international and unknown share of credits overall and for the Top 10, with the coverage (share of credits with a known country) shown next to every percentage. Write it to `outputs/tables/country_mix.csv`.
6. If coverage is below 80 percent of credits, tell me and recommend stating the result as indicative only.
