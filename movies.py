# ruff: noqa: FIX002, TD002, TD003, S311

"""A simple interface to interact with an dummy movie "db"."""

import sys
from random import randint
from statistics import mean as mean_statistics
from statistics import median as median_statistics

from app_config import (
    CURRENT_YEAR,
    FIRST_MOVIE_RELEASE,
    MENU_ITEMS,
    MOVIE_MAX_RATING,
    MOVIE_MIN_RATING,
    OUTPUT_COLORS,
)
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
from histogram import create_histogram
from movie_search import movie_search

"""


TODO: (but out of scope of this exercise):
  - unify user input and validation across all features:
    - probably some prompt_validator that takes a list of tests
      for that specific input to pass. Too early for now.
  - add movie: check if already exists, present option to update
  - update movie: check if not existing, present option to add
  - update / delete movie: fuzzy search
  - delete movie: present list and let choose by inputting number
  - fix fail on empty db
  - add real clear terminal
  - implement fname from matplotlib instead naive str as filename
  -  pretty align movie outputs


Version 1.1.0 <- submitted
"""

"""
 ~ Made with ❤️ and without ai or code completion (except intelliSense) ~
"""


def main() -> None:
    """Run app."""
    run()


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

def _get_yes_no_choice(prompt: str) -> bool:
    """Ask user to choose between Yes or No.

    Returns True for Yes,
    returns False for No.
    """
    while True:
        name = _get_user_input_colored(prompt).strip()
        if name not in ("Y", "Yes", "y", "N", "No", "n"):
            _output("Choose (Y)es or (N)o: ", color="yellow")
        else:
            break

    return name in {"Y", "y"}


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


def list_movies_by_release() -> None:
    """Return a list of movies by release year.

    Asks user for preferred sorting order.
    """
    db: dict[str, dict] = db_get_movies()
    prompt = (
        "\nDo you want to order the movies in descending order?\n"
        "Choose (Y)es or (N)o: "
    )
    sort_descending = _get_yes_no_choice(prompt)

    order = "descending" if sort_descending else "ascending"

    _output(f"Movies by release ({order}):\n", space_before=True)

    for name, info in _get_as_list_sorted_by_release(
        db,
        descending=sort_descending,
    ):
        release = info["release"]
        rating = info["rating"]
        _output(f"{name} ({rating}): {release}")


def list_movies() -> None:
    """Return a list of all movies."""
    db: dict[str, dict] = db_get_movies()
    _output(f"{len(db)} movies in total:\n", space_before=True)

    for name, info in db.items():
        rating = info["rating"]
        release = info["release"]
        _output(f"{name} ({release}): {rating}")


def list_movies_by_rating() -> None:
    """Return a list of all movies by rating."""
    db: dict[str, dict] = db_get_movies()
    _output("Movies by rating:\n", space_before=True)

    for name, info in _get_as_list_sorted_by_rating(db, descending=True):
        release = info["release"]
        rating = info["rating"]
        _output(f"{name} ({release}): {rating}")


def _is_num(inp: str) -> bool:
    """Validate if a sting input is a valid number."""
    if inp == "":
        return False
    try:
        float(inp)
    except ValueError:
        return False
    return True


def _is_int(inp: str) -> bool:
    """Validate if a sting input is a valid int."""
    if inp == "" or "." in inp:
        return False
    try:
        int(inp)
    except ValueError:
        return False
    return True


def _rating_in_range(inp: str) -> bool:
    """Validate if a rating is in allowed range."""
    return MOVIE_MIN_RATING <= float(inp) <= MOVIE_MAX_RATING


def _get_user_input_colored(promt: str) -> str:
    """Ask for user input, now in technicolor."""
    try:
        return input(OUTPUT_COLORS["yellow"] + promt)
    finally:
        # reset input coloring, also at EOF
        print("" + OUTPUT_COLORS["end"], end="")


def _strip_leading_zero(num: str | float) -> str | int | float:
    """Strip leading "0"s in input, returns same format."""
    res = str(num)
    while res[0] == "0" and len(res) > 1:
        res = res[1:]

    if isinstance(num, int):
        return int(res)
    if isinstance(num, float):
        return float(res)
    return res


def _get_movie_name(prompt: str) -> str:
    """Ask user to input a valid movies name."""
    # TODO: tbd: check for implausible names like *?
    while True:
        name = _get_user_input_colored(prompt).strip()
        if name == "":
            _output("Name required", color="red")
        else:
            break
    return name


def _get_movie_release(prompt: str) -> int:
    """Ask user to input a valid movie release year."""
    while True:
        release = _get_user_input_colored(prompt).strip()
        if release == "":
            _output("Year required", color="red")
        else:
            release = _validate_release(release)
            if release is not None:
                return int(release)


def _validate_release(release: str) -> int | None:
    """Validate release input.

    Returns release as int or None
    """
    if not _is_num(release):
        _output("Year must be a number", color="red")
        return None
    if not _is_int(release):
        _output("Year must be valid int", color="red")
        return None
    if int(release) < FIRST_MOVIE_RELEASE:
        _output(
            "Nice try. The first movie was released in "
            f"{FIRST_MOVIE_RELEASE}.",
            color="red",
        )
        return None
    if int(release) > CURRENT_YEAR:
        _output(
            "Real futuristic movie - a rating from the future!",
            color="red",
        )
        return None
    return int(release)


def _get_movie_release_optional(prompt: str) -> int | None:
    """Ask user to input a valid movie release, or leave empty."""
    while True:
        release = _get_user_input_colored(prompt).strip()
        if release == "":
            return None
        release = _validate_release(release)
        if release is not None:
            return release


def _get_movie_rating(prompt: str) -> float:
    """Ask user to input a valid movies rating."""
    while True:
        rating = _get_user_input_colored(prompt).strip()
        if rating == "":
            _output("Rating required", color="red")
        rating = _validate_rating(rating)
        if rating is not None:
            return rating


def _validate_rating(rating: str) -> float | None:
    """Validate rating input.

    Returns rating as float or None
    """
    if not _is_num(rating):
        _output("Rating must be a number", color="red")
        return None
    if not _rating_in_range(rating):
        _output("Rating must be between 0 - 10", color="red")
        return None
    return float(rating)


def _get_movie_rating_optional(prompt: str) -> float | None:
    """Ask user to input a valid movie rating, or leave empty."""
    while True:
        rating = _get_user_input_colored(prompt).strip()
        if rating == "":
            return None
        rating = _validate_rating(rating)
        if rating is not None:
            return rating


def add_movie() -> None:
    """Add an item to db."""
    # TODO: - check if already exists early directly after input of name

    name = _get_movie_name("\nEnter new movies name: ")

    release = _get_movie_release("Enter new movies year of release: ")

    rating = _get_movie_rating("Enter new movies rating (0-10): ")

    try:
        db_add_movie(name, release, rating)
    except ValueError as movie_exists_error:
        _output(
            f"{movie_exists_error}",
            space_before=True,
            color="red",
        )
    else:
        _output(
            f'Movie "{name}" ({release}) with '
            f"rating {rating} successfully added",
            space_before=True,
        )

def _get_movie_filters() -> tuple[float | None, int | None, int | None]:
    filter_rating = _get_movie_rating_optional(
        "\nEnter minimum rating (leave blank for no minimum rating): ",
    )

    filter_release_start = _get_movie_release_optional(
        "Enter start year of range (leave blank for no start year): ",
    )

    while True:
        filter_release_end = _get_movie_release_optional(
            "Enter end year of range (inclusive) (leave blank "
            "for no end year): ",
        )
        if (
            filter_release_start
            and filter_release_end
            and (filter_release_start > filter_release_end)
        ):
            _output("Start hast do be before end", color="red")
        else:
            break
    return (filter_rating, filter_release_start, filter_release_end)

def _construct_filter_output(
    rating: float | None,
    start: int | None,
    end: int | None,
) -> str:
    """Construct output based on provided filters."""
    outp_start = "Movies filtered by "
    outp_if_rating = f"rating ({rating})" if rating else ""
    connector = " and " if rating and start else ""
    outp_if_start = f"year start ({start})" if start else ""
    connector2 = " and " if end else ""
    outp_if_end = f"year end ({end})" if end else ""
    outp_end = ":\n"

    return (
        outp_start
        + outp_if_rating
        + connector
        + outp_if_start
        + connector2
        + outp_if_end
        + outp_end
    )


def list_movies_by_filter() -> None:
    """List filtered movies by user input.

    Asks for rating, start and end year,
    lists accordingly.
    """
    db: dict[str, dict] = db_get_movies()

    filter_rating, filter_release_start, filter_release_end = (
        _get_movie_filters()
    )

    if (
        not filter_rating
        and not filter_release_start
        and not filter_release_end
    ):
        _output(
            "No filters provided. Here are all movies:",
            space_before=True,
        )
        list_movies()
    else:

        _output(
            _construct_filter_output(
                filter_rating,
                filter_release_start,
                filter_release_end,
            ),
            space_before=True,
        )

        filtered_results = _get_as_list_filtered(
            db,
            filter_rating,
            filter_release_start,
            filter_release_end,
        )

        _output("No movies match your filters.")

        for name, info in sorted(filtered_results):
            release = info["release"]
            rating = info["rating"]
            _output(f"{name} ({release}): {rating}")


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

def remove_movie() -> None:
    """Remove an item from db."""
    # TODO: - check if already exists early directly after input of name

    name = _get_movie_name("\nEnter (exact) movie name to delete: ")

    try:
        db_delete_movie(name)

    except ValueError as movie_doesnt_exist_error:
        _output(
            f"{movie_doesnt_exist_error}",
            space_before=True,
            color="red",
        )
    else:
        _output(
            f'Movie "{name}" successfully deleted',
            space_before=True,
        )


def update_movie() -> None:
    """Update movie rating."""
    # TODO: - check if already exists early directly after input of name

    name = _get_movie_name("\nEnter (exact) movie name to update: ")

    rating = _get_movie_rating("Enter new movies rating (0-10): ")

    try:
        db_update_movie(name, rating)
    except ValueError as movie_doesnt_exist_error:
        _output(
            f"{movie_doesnt_exist_error}",
            space_before=True,
            color="red",
        )
    else:
        _output(
            f'Movie "{name}" successfully updated to rating: {rating}',
            space_before=True,
        )


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


def list_statistics() -> None:
    """Get statistics.

    - average
    - median
    - top-ranked items
    - bottom-ranged items
    """
    # TODO: - sort best / worst if multiple by name
    db: dict[str, dict] = db_get_movies()
    val_list = [info["rating"] for info in db.values()]
    avg = mean_statistics(val_list)
    median = median_statistics(sorted(val_list))
    rated_best = _get_extremes(db)
    rated_worst = _get_extremes(db, descending=False)

    _output(f"Average rating: {avg:.1f}", space_before=True)
    _output(f"Median rating: {median:.1f}")
    _output("Best rated movie(s):")
    for best_name, best_info in rated_best:
        best_rating = best_info["rating"]
        best_release = best_info["release"]
        _output(f'   "{best_name}" ({best_release}), {best_rating}')
    _output("Worst rated movie(s):")
    for worst_name, worst_info in rated_worst:
        worst_rating = worst_info["rating"]
        worst_release = worst_info["release"]
        _output(f'   "{worst_name}" ({worst_release}), {worst_rating}')


def random_movie() -> None:
    """Return random movie."""
    db: dict[str, dict] = db_get_movies()
    name, info = list(db.items())[randint(0, len(db) - 1)]
    _output(
        f"Your movie for tonight: {name} ({info['release']}), "
        f"it's rated {info['rating']}",
        space_before=True,
    )


def search_movie() -> None:
    """Search for movies by title."""
    data: dict[str, dict] = db_get_movies()

    query = _get_movie_name("\nEnter part of movie name: ")
    try:
        results = movie_search(data, query)

        if len(results) == 1:
            name, info = results[0]
            _output(
                f"{name} ({info['release']}), {info['rating']}",
                space_before=True,
            )
        else:
            _output(
                f'No movie titled "{query}" found. Did you mean:\n',
                space_before=True,
            )
            for res in results:
                name, info = res
                _output(f"• {name} ({info['release']}), {info['rating']}")

    except ValueError:
        _output(
            f'No Movie name similar to "{query}" '
            "(remember that at least the first letter has to match)\n",
            color="red",
            space_before=True,
        )


def _get_file_name(prompt: str) -> str:
    """Ask user to input a valid movies rating."""
    while True:
        filename = _get_user_input_colored(
            prompt,
        ).strip()
        if filename == "":
            _output("Filename required", color="red")
        elif not filename.replace(".", "").isalnum():
            _output("Filename must be alphanumeric", color="red")
        else:
            break
    return filename


def ratings_histogram() -> None:
    """Create movie ratings histogram and save to disc."""
    # TODO: - returns on fail to menu, should retry

    data = db_get_movies()
    filename = _get_file_name(
        "\nEnter filename (saved as png unless otherwise "
        "specified) in your current working directory: ",
    )
    try:
        create_histogram(data, filename)
        _output(
            f'File "{filename}" successfully saved to disk.',
            space_before=True,
        )
    except ValueError as err_msg:
        _output(str(err_msg), color="red", space_before=True)


def _idle_after_input() -> None:
    """Idle with prompt to continue."""
    _get_user_input_colored("\npress Enter to continue ")


def _menu_selection_in_range(
    selection: str,
    max_range: int,
    min_range: int = 0,
) -> bool:
    try:
        int(selection)
    except ValueError:
        return False
    else:
        return min_range <= int(selection) <= max_range + 1


def present_menu(menu_items: list[str]) -> int:
    """Print the menu to the user, asks for input."""
    """ Options:
        0:  Exit
        1:  List movies
        2:  List movies rating
        3:  List movies release
        4.  List movies by filter
        5:  Search movie
        6:  Random movie
        7:  Add movie
        8:  Update movie
        9:  Delete movie
        10:  Stats
        11. Create ratings histogram
    """

    _output("")

    for item in menu_items:
        _output(item, color="blue")

    insist_to_quit = False

    while True:
        selection = _get_user_input_colored(
            "\nEnter choice (0-11): ",
        ).strip()

        if selection == "" and insist_to_quit:
            _quit_program()
        elif (
            selection is not selection.isdecimal()
            and not _menu_selection_in_range(selection, len(MENU_ITEMS))
        ):
            _output(
                "Invalid input (Enter 0 - 11. Try again).\n"
                "Or press ENTER again to quit",
                color="red",
            )
            insist_to_quit = True
        else:
            break

    return int(selection)


def _quit_program() -> None:
    """Quit with farewell."""
    _output("Bye!")
    sys.exit()


def _clear_screen() -> None:
    """Clear console hack."""
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")


def _output(
    inp: str,
    color: str = "",
    *,
    space_after: bool = False,
    space_before: bool = False,
) -> None:
    """Print what's given. Optionally adds gap or color."""
    if space_before:
        print("\n \n")
    if color:
        if color == "red":
            print(OUTPUT_COLORS["red"] + inp + OUTPUT_COLORS["end"])
        if color == "blue":
            print(OUTPUT_COLORS["blue"] + inp + OUTPUT_COLORS["end"])
        if color == "yellow":
            print(OUTPUT_COLORS["yellow"] + inp + OUTPUT_COLORS["end"])
    else:
        print(inp)

    if space_after:
        print("\n \n")


def run() -> None:
    """Print welcome and loop menu."""
    first_run = True
    _clear_screen()
    _output(
        "********** My Movies Database **********",
        color="blue",
    )

    menu_dispatch = {
        1: list_movies,
        2: list_movies_by_rating,
        3: list_movies_by_release,
        4: list_movies_by_filter,
        5: search_movie,
        6: random_movie,
        7: add_movie,
        8: update_movie,
        9: remove_movie,
        10: list_statistics,
        11: ratings_histogram,
        # 0: quit_program handled separately
    }

    while True:
        if not first_run:
            _clear_screen()
        first_run = False

        selection = present_menu(MENU_ITEMS)

        if selection == 0:
            _quit_program()
        else:
            _clear_screen()
            _output(
                f"~~~~~~~~~~\nSelected menu item:"
                f"{MENU_ITEMS[selection + 1]}\n"
                "~~~~~~~~~~",
                color="yellow",
            )

            menu_dispatch[selection]()

            _idle_after_input()


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        # quit gratefully on termination
        print("\nThat was sudden. Goodbye!\n")
        sys.exit()
