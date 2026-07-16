# ruff: noqa: FIX002, TD002, TD003, TD005
"""Module for handling all CRUD operations."""

import json
from pathlib import Path

"""
TODO:
- implement custom Exception classes

"""

DATA_DIR = Path("data_dir")
FILE_PATH = DATA_DIR / "data.json"


def get_movies() -> dict[str, dict]:
    """Return the movies information from the database.

    The function loads the information from the JSON
    file and returns the data as a dict of dicts.

    Expects the JSON data file to exist.

    For example, the function may return:
    {
      "Titanic": {
        "rating": 9,
        "year": 1999
      },
      "..." {
        ...
      },
    }
    """
    with Path(FILE_PATH).open("r") as file:
        return json.load(file)


def save_movies(movies: dict[str, dict]) -> bool | Exception:
    """Get all your movies as an argument and saves them to JSON."""
    with Path(FILE_PATH).open("w") as file:
        json.dump(movies, file, indent=4)
    return True


def add_movie(title: str, year: int, rating: float) -> bool | Exception:
    """Add a movie to the movies database."""
    # TODO:
    #   - Allow for multiple names with different release years

    movies = get_movies()
    if title in movies:
        raise ValueError("add_already_exists")
    movies[title] = {"rating": rating, "release": year}
    save_movies(movies)
    return True


def delete_movie(title: str) -> bool | Exception:
    """Delete a movie from the movies database.

    Loads the information from the JSON, deletes the movie,
    and saves it. The function doesn't need to validate the input.
    """
    movies = get_movies()
    if title not in movies:
        raise ValueError("del_doenst_exist")

    del movies[title]
    save_movies(movies)
    return True


def update_movie(title: str, rating: float) -> bool | Exception:
    """Update a movie from the movies database.

    Loads the information from the JSON file, updates the movie,
    and saves it. The function doesn't need to validate the input.
    """
    movies = get_movies()
    if title not in movies:
        raise ValueError("upd_doenst_exist")

    movies[title]["rating"] = rating
    save_movies(movies)
    return True
