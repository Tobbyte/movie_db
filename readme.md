# 🎬 Movie Database App

A command-line tool to manage a personal movie collection: list, sort, filter,
fuzzy-search, and rate your movies and visualize stats.

## Features

- List all movies, sorted by rating or by release year (asc/desc)
- Filter by minimum rating and/or a release-year range
- Fuzzy title search — custom Levenshtein-distance implementation, no external libs
- Pick a random movie for tonight
- Add, update, delete movies
- Stats: average & median rating, best- and worst-rated movie(s)
- Generate a ratings histogram and save it to disk (matplotlib)

## Installation

```bash
git clone https://github.com/Tobbyte/movie_db.git
cd movie_db
pip install -r requirements.txt
```

Requires Python 3.10+ (uses `X | None` type hints).

## Usage

```bash
python movies.py
```

Navigate with the on-screen menu (0–11).

## Project structure

```
movies.py                 # entry point, CLI menu loop
app_config/
  app_config.py            # constants: menu items, colors, rating bounds, file paths
data_handling/
  movie_storage.py          # CRUD against the JSON "database"
  data_provider.py          # sorting & filtering
  movie_search.py           # search orchestration (exact + fuzzy)
  my_fuzzy_search.py        # custom Levenshtein-distance fuzzy matcher
helpers/
  helpers.py                 # input validation & formatted output
  histogram.py                # matplotlib ratings histogram
user_input/
  user_input.py               # all prompts + validation loops
data_dir/data.json         # the "database" (title -> {rating, release})
```

## Data format

```json
{
  "Movie Title": {
    "rating": 9.5,
    "release": 1991
  }
}
```

## Known limitations

(documented in the code as intentionally out of scope for this version)

- No existence-check before add/update/delete — e.g. adding an existing title
  just raises an error instead of offering to update it
- Fuzzy search is only used for the search menu, not for update/delete
- "Clear screen" is a print-based hack, not a real terminal clear

Fuzzy search specifically:
( *--> __unchanged from movie phase 1__ <--* )
- Naive Levenshtein distance, computed against every DB entry — no indexing
  or other optimization
- A match requires at least one word in the search term and the compared
  title to share a first letter; otherwise it's excluded even if it's within
  the distance threshold
- Only "the" is filtered out as a filler word (excluded_terms); the list
  isn't configurable/extensible yet
- Searching for a filler word itself (e.g. "the") won't reliably return every
  title containing it, since the edit-distance threshold still applies

## Notes

Built with ❤️ and without AI code generation or autocomplete (aside from IntelliSense).<sup>*</sup>

<sup>*</sup> ... except a draft of this readme.