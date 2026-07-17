# ruff: noqa: FIX002, TD002, TD003, TD005
"""Module for handling all CRUD operations."""

import json
from pathlib import Path

from app_config.app_config import DATA_FILE_PATH

"""
TODO:
- implement custom Exception classes
- provide cached versions of db in different formats:
  lower:Upper case titles, sorted by rating

"""


def assure_db_exists() -> None:
    """Check if db exists.

    Creates empty if not.
    """
    if not Path.exists(DATA_FILE_PATH):
        _save_movies({})


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
    with Path(DATA_FILE_PATH).open("r") as file:
        return json.load(file)


def _save_movies(movies: dict[str, dict]) -> None:
    """Save whats given as argument and save to JSON."""
    # TODO: - add save handling of fail cases, f.e. missing permissions
    with Path(DATA_FILE_PATH).open("w") as file:
        json.dump(movies, file, indent=4)


def add_movie(title: str, year: int, rating: float) -> None:
    """Add a movie to the movies database.

    Loads the latest file, adds and saves.
    Validates for existence in db and raises ValueError with
    custom Message to be handled by caller.
    """
    # TODO:
    #   - Allow for multiple names with different release years

    movies = get_movies()
    if title in movies:
        error_msg = f'Movie "{title}" already exists'
        raise ValueError(error_msg)
    movies[title] = {"rating": rating, "release": year}
    _save_movies(movies)


def delete_movie(title: str) -> None:
    """Delete a movie from the movies database.

    Loads the latest file, deletes and saves.
    Validates for existence in db and raises ValueError with
    custom Message to be handled by caller.
    """
    movies = get_movies()
    if title not in movies:
        error_msg = f'Movie "{title}" doesn`t exist!'
        raise ValueError(error_msg)

    del movies[title]
    _save_movies(movies)


def update_movie(title: str, rating: float) -> None:
    """Update a movie from the movies database.

    Loads the latest file, updates and saves.
    Validates for existence in db and raises ValueError with
    custom Message to be handled by caller.
    """
    movies = get_movies()
    if title not in movies:
        error_msg = f'Movie "{title}" doesn`t exist!'
        raise ValueError(error_msg)

    movies[title]["rating"] = rating
    _save_movies(movies)
