"""Module to provide data."""

from data_handling.movie_storage import get_movies as db_get_movies


def get_movies_count() -> int:
    """Return the count of movies in the db."""
    return len(db_get_movies())


def get_as_list_sorted_by_rating(
    *,
    descending: bool = False,
) -> list[tuple]:
    """Sort movies by rating.

    Return a list of (name, info) tuples for movies in db
    in ascending order of rating.
    """
    db: dict[str, dict] = db_get_movies()
    return sorted(
        db.items(),
        key=lambda item: item[1]["rating"],
        reverse=descending,
    )


def get_as_list_sorted_by_release(
    *,
    descending: bool = False,
) -> list[tuple]:
    """Sort movies by release year.

    Return a list of (name, info) tuples for movies in db
    in ascending order of release year.
    """
    db: dict[str, dict] = db_get_movies()
    return sorted(
        db.items(),
        key=lambda item: item[1]["release"],
        reverse=descending,
    )


def get_as_list_filtered(
    rating: float | None = None,
    start: int | None = None,
    end: int | None = None,
) -> list[tuple[str, dict]]:
    """Return a list of all movies matching provided filters."""
    db: dict[str, dict] = db_get_movies()
    return [
        (title, info)
        for title, info in db.items()
        if (rating is None or info["rating"] >= rating)
        and (start is None or info["release"] >= start)
        and (end is None or info["release"] <= end)
    ]


def get_extremes(
    *,
    descending: bool = True,
) -> list[tuple[str, dict]]:
    """Get the extreme values:[num] of dict."""
    sorted_by_rating = get_as_list_sorted_by_rating(descending=descending)

    # take rating of first item of sorted movies
    _, info = sorted_by_rating[0]
    extr_rating = info["rating"]

    return [
        (name, info)
        for (name, info) in sorted_by_rating
        if info["rating"] == extr_rating
    ]
