"""Module for handling all CRUD operations."""


def get_movies() -> dict[str, dict]:
    """Return the movies information from the database.

    The function loads the information from the JSON
    file and returns the data as a dict of dicts.

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
    return {"empty": {"a": 1}}


def save_movies(movies: dict[str, dict]) -> bool | Exception:
    """Get all your movies as an argument and saves them to JSON."""
    return True


def add_movie(title: str, year: int, rating: float) -> bool | Exception:
    """Add a movie to the movies database.

    Loads the information from JSON, add the movie,
    and saves it. The function doesn't need to validate the input.
    """
    return True


def delete_movie(title: str) -> bool | Exception:
    """Delete a movie from the movies database.

    Loads the information from the JSON, deletes the movie,
    and saves it. The function doesn't need to validate the input.
    """
    return True


def update_movie(title: str, rating: float) -> bool | Exception:
    """Update a movie from the movies database.

    Loads the information from the JSON file, updates the movie,
    and saves it. The function doesn't need to validate the input.
    """
    return True
