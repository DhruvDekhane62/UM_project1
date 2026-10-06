"""Known band/group names containing delimiters ('&', ',', '+', etc.) that should not be split into multiple artists."""

BAND_EXCEPTIONS = {
    "years & years",
    "florence + the machine",
    "florence and the machine",
    "earth, wind & fire",
    "hall & oates",
    "simon & garfunkel",
    "mumford & sons",
    "bob marley & the wailers",
    "brooks & dunn",
    "dan + shay",
    "maroon 5",
    "iron & wine",
    "kc and the sunshine band",
    "gladys knight & the pips",
    "toots & the maytals",
    "sly & the family stone",
    "hugh masekela",
}


def is_band_exception(artist_name: str) -> bool:
    """Check if normalized artist name is a known band exception."""
    return artist_name.strip().lower() in BAND_EXCEPTIONS
