# Data integrity rules

- `data/raw/` is read-only. Never edit, overwrite or re-save the original CSV. All cleaning happens in code and writes to `data/processed/`.
- Never invent, estimate or "fill in" values. Every number in the dashboard or paper must come from code in `src/` and be saved to `outputs/tables/` under a filename that says what it is.
- Inspect the real file before trusting the brief. If the data disagrees with `docs/data_dictionary.md` (column names, encodings, value ranges), update the dictionary, log it in `docs/decisions.md`, and tell me.
- Validation reports problems; it does not silently fix them. Every row dropped and every value changed is counted in `docs/data_quality.md`.
- Parse `is_explicit` explicitly. Values may be strings such as "True" and "False", and `astype(bool)` turns every non-empty string into True.
- Artist splitting: look at which delimiters actually occur before choosing a rule. Keep band names that contain a delimiter (for example "Years & Years") in `src/artist_exceptions.py`, and report how many rows the rule changed.
- Never guess an artist's nationality from a name. Country comes only from the MusicBrainz lookup in the `/enrich-country` workflow, cached in `data/external/artist_country.csv` with the lookup date. Unresolved artists are labelled `Unknown`.
- MusicBrainz etiquette: at most one request per second and a descriptive User-Agent that includes my contact email. Ask me for the email; never invent one.
- No other external API calls or downloads without asking me first.
- Do not commit the raw dataset to a public repository without asking me; the brief does not state its licence.
