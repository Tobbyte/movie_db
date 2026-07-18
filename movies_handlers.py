# ruff: noqa: FIX002, TD002, TD003, S311
"""Handlers for the actual program features."""

from random import randint
from statistics import mean as mean_statistics
from statistics import median as median_statistics

from app_config.app_config import DATA_DIR_PATH
from data_handling import (
    add_movie as db_add_movie,
)
from data_handling import (
    delete_movie as db_delete_movie,
)
from data_handling import (
    get_movies as db_get_movies,
)
from data_handling import (
    update_movie as db_update_movie,
)
from data_handling.data_provider import (
    get_as_list_filtered,
    get_as_list_sorted_by_rating,
    get_as_list_sorted_by_release,
    get_extremes,
)
from data_handling.movie_search import movie_search
from helpers.helpers import construct_filter_output, output
from helpers.histogram import create_histogram
from user_input.user_input import (
    get_ab_choice,
    get_file_name,
    get_movie_filters,
    get_movie_name,
    get_movie_rating,
    get_movie_release,
)


def list_movies() -> None:
    """Return a list of all movies."""
    movies_data: dict[str, dict] = db_get_movies()
    output(f"{len(movies_data)} movies in total:\n", space_before=True)

    for name, info in movies_data.items():
        rating = info["rating"]
        release = info["release"]
        output(f"{name} ({release}): {rating}")


def list_movies_by_rating() -> None:
    """Return a list of all movies by rating."""
    output("Movies by rating:\n", space_before=True)

    for name, info in get_as_list_sorted_by_rating(descending=True):
        release = info["release"]
        rating = info["rating"]
        output(f"{name} ({release}): {rating}")


def list_movies_by_release() -> None:
    """Return a list of movies by release year.

    Asks user for preferred sorting order.
    """
    prompt = "\nDo you want to order the movies (a)scending or (d)escending? "
    sort_ascending = get_ab_choice(prompt, "a", "d")

    order = "ascending" if sort_ascending else "descending"

    output(f"Movies by release ({order}):\n", space_before=True)

    for name, info in get_as_list_sorted_by_release(
        descending=not sort_ascending,
    ):
        release = info["release"]
        rating = info["rating"]
        output(f"{name} ({rating}): {release}")


def list_movies_by_filter() -> None:
    """List filtered movies by user input.

    Asks for rating, start and end year,
    lists accordingly.
    """
    filter_rating, filter_release_start, filter_release_end = (
        get_movie_filters()
    )

    if (
        filter_rating is None
        and filter_release_start is None
        and filter_release_end is None
    ):
        output(
            "No filters provided. Here are all movies:",
            space_before=True,
        )
        list_movies()
    else:
        output(
            construct_filter_output(
                filter_rating,
                filter_release_start,
                filter_release_end,
            ),
            space_before=True,
        )

        filtered_results = get_as_list_filtered(
            filter_rating,
            filter_release_start,
            filter_release_end,
        )

        if not filtered_results:
            output("No movies match your filters.")

        for name, info in sorted(filtered_results):
            release = info["release"]
            rating = info["rating"]
            output(f"{name} ({release}): {rating}")


def random_movie() -> None:
    """Return random movie."""
    movies_data: dict[str, dict] = db_get_movies()
    name, info = list(movies_data.items())[randint(0, len(movies_data) - 1)]
    output(
        f"Your movie for tonight: {name} ({info['release']}), "
        f"it's rated {info['rating']}",
        space_before=True,
    )


def search_movie() -> None:
    """Search for movies by title."""
    data: dict[str, dict] = db_get_movies()

    query = get_movie_name("\nEnter part of movie name: ")
    try:
        results = movie_search(data, query)

        if len(results) == 1:
            name, info = results[0]
            output(
                f"{name} ({info['release']}), {info['rating']}",
                space_before=True,
            )
        else:
            output(
                f'No movie titled "{query}" found. Did you mean:\n',
                space_before=True,
            )
            for res in results:
                name, info = res
                output(f"• {name} ({info['release']}), {info['rating']}")

    except ValueError:
        output(
            f'No Movie name similar to "{query}" '
            "(remember that at least the first letter has to match)\n",
            color="red",
            space_before=True,
        )


def ratings_histogram() -> None:
    """Create movie ratings histogram and save to disc."""
    # TODO: - returns on fail to menu, should retry

    data = db_get_movies()
    filename = get_file_name(
        "\nEnter filename (saved as png unless otherwise specified): ",
    )
    try:
        full_filename = create_histogram(data, filename)
        output(
            f'File "{filename}" successfully saved to '
            f".{DATA_DIR_PATH}/{full_filename}.",
            space_before=True,
        )
    except ValueError as err_msg:
        output(str(err_msg), color="red", space_before=True)


def add_movie() -> None:
    """Add a movie to movies collection."""
    # TODO: - check if already exists early directly after input of name

    name = get_movie_name("\nEnter new movies name: ")

    release = get_movie_release("Enter new movies year of release: ")

    rating = get_movie_rating("Enter new movies rating (0-10): ")

    try:
        db_add_movie(name, release, rating)
    except ValueError as movie_exists_error:
        output(
            f"{movie_exists_error}",
            space_before=True,
            color="red",
        )
    else:
        output(
            f'Movie "{name}" ({release}) with '
            f"rating {rating} successfully added",
            space_before=True,
        )


def remove_movie() -> None:
    """Remove a movie from movies collection."""
    # TODO: - check if already exists early directly after input of name

    name = get_movie_name("\nEnter (exact) movie name to delete: ")

    try:
        db_delete_movie(name)

    except ValueError as movie_doesnt_exist_error:
        output(
            f"{movie_doesnt_exist_error}",
            space_before=True,
            color="red",
        )
    else:
        output(
            f'Movie "{name}" successfully deleted',
            space_before=True,
        )


def update_movie() -> None:
    """Update a movies rating in movies collection."""
    # TODO: - check if already exists early directly after input of name

    name = get_movie_name("\nEnter (exact) movie name to update: ")

    rating = get_movie_rating("Enter new movies rating (0-10): ")

    try:
        db_update_movie(name, rating)
    except ValueError as movie_doesnt_exist_error:
        output(
            f"{movie_doesnt_exist_error}",
            space_before=True,
            color="red",
        )
    else:
        output(
            f'Movie "{name}" successfully updated to rating: {rating}',
            space_before=True,
        )


def list_statistics() -> None:
    """Get statistics.

    - average
    - median
    - top-ranked items
    - bottom-ranged items
    """
    # TODO: - sort best / worst if multiple by name
    movies_data: dict[str, dict] = db_get_movies()
    val_list = [info["rating"] for info in movies_data.values()]
    avg = mean_statistics(val_list)
    median = median_statistics(sorted(val_list))
    rated_best = get_extremes()
    rated_worst = get_extremes(descending=False)

    output(f"Average rating: {avg:.1f}", space_before=True)
    output(f"Median rating: {median:.1f}")
    output("Best rated movie(s):")
    for best_name, best_info in rated_best:
        best_rating = best_info["rating"]
        best_release = best_info["release"]
        output(f'   "{best_name}" ({best_release}), {best_rating}')
    output("Worst rated movie(s):")
    for worst_name, worst_info in rated_worst:
        worst_rating = worst_info["rating"]
        worst_release = worst_info["release"]
        output(f'   "{worst_name}" ({worst_release}), {worst_rating}')
