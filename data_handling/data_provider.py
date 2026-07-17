"""Module to provide data."""
def _get_as_list_sorted_by_rating(
    dic: dict[str, dict],
    *,
    descending: bool = False,
) -> list[tuple]:
    """Sort movies by rating.

    Return a list of (name, info) tuples for movies in db
    in ascending order of rating.
    """
    return sorted(
        dic.items(),
        key=lambda item: item[1]["rating"],
        reverse=descending,
    )


def _get_as_list_sorted_by_release(
    dic: dict[str, dict],
    *,
    descending: bool = False,
) -> list[tuple]:
    """Sort movies by release year.

    Return a list of (name, info) tuples for movies in db
    in ascending order of release year.
    """
    return sorted(
        dic.items(),
        key=lambda item: item[1]["release"],
        reverse=descending,
    )


def _get_as_list_filtered(
    dic: dict[str, dict],
    rating: float | None = None,
    start: int | None = None,
    end: int | None = None,
) -> list[tuple[str, dict]]:
    """Return a list of all movies matching provided filters."""
    return [
        (title, info)
        for title, info in dic.items()
        if (rating is None or info["rating"] >= rating)
        and (start is None or info["release"] >= start)
        and (end is None or info["release"] <= end)
    ]


def _get_extremes(
    db: dict[str, dict],
    *,
    descending: bool = True,
) -> list[tuple[str, dict]]:
    """Get the extreme values:[num] of dict."""
    sorted_by_rating = _get_as_list_sorted_by_rating(db, descending=descending)

    # take rating of first item of sorted movies
    _, info = sorted_by_rating[0]
    extr_rating = info["rating"]

    return [
        (name, info)
        for (name, info) in sorted_by_rating
        if info["rating"] == extr_rating
    ]
