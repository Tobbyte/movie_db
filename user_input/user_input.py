# ruff: noqa: FIX002, TD002, TD003
"""Module that handles all user inputs."""

from app_config.app_config import (
    CURRENT_YEAR,
    FIRST_MOVIE_RELEASE,
    MENU_ITEMS,
    OUTPUT_COLORS,
)
from helpers.helpers import (
    is_int,
    is_num,
    menu_selection_in_range,
    output,
    rating_in_range,
    strip_leading_zero,
)


def get_yes_no_choice(prompt: str) -> bool:
    """Ask user to choose between Yes or No.

    Returns True for Yes,
    returns False for No.
    """
    while True:
        name = get_user_input_colored(prompt).strip()
        if name not in ("Y", "Yes", "y", "N", "No", "n"):
            output("Choose (Y)es or (N)o: ", color="yellow")
        else:
            break

    return name in {"Y", "y"}


def get_user_input_colored(promt: str) -> str:
    """Ask for user input, now in technicolor."""
    try:
        return input(OUTPUT_COLORS["yellow"] + promt)
    finally:
        # reset input coloring, also at EOF
        print("" + OUTPUT_COLORS["end"], end="")


def get_movie_name(prompt: str) -> str:
    """Ask user to input a valid movies name."""
    # TODO: tbd: check for implausible names like *?
    while True:
        name = get_user_input_colored(prompt).strip()
        if name == "":
            output("Name required", color="red")
        else:
            break
    return name


def get_movie_release(prompt: str) -> int:
    """Ask user to input a valid movie release year."""
    while True:
        release = get_user_input_colored(prompt).strip()
        if release == "":
            output("Year required", color="red")
        else:
            release = _validate_release(release)
            if release is not None:
                return int(release)


def _validate_release(release: str) -> int | None:
    """Validate release input.

    Returns release as int or None
    """
    if not is_num(release):
        output("Year must be a number", color="red")
        return None
    if not is_int(release):
        output("Year must be valid int", color="red")
        return None
    if int(release) < FIRST_MOVIE_RELEASE:
        output(
            "Nice try. The first movie was released in "
            f"{FIRST_MOVIE_RELEASE}.",
            color="red",
        )
        return None
    if int(release) > CURRENT_YEAR:
        output(
            "Real futuristic movie - a rating from the future!",
            color="red",
        )
        return None
    return int(release)


def _get_movie_release_optional(prompt: str) -> int | None:
    """Ask user to input a valid movie release, or leave empty."""
    while True:
        release = get_user_input_colored(prompt).strip()
        if release == "":
            return None
        release = _validate_release(release)
        if release is not None:
            return release


def get_movie_rating(prompt: str) -> float:
    """Ask user to input a valid movies rating."""
    while True:
        rating = get_user_input_colored(prompt).strip()
        if rating == "":
            output("Rating required", color="red")
        rating = _validate_rating(rating)
        if rating is not None:
            return rating


def _validate_rating(rating: str) -> float | None:
    """Validate rating input.

    Returns rating as float or None
    """
    if not is_num(rating):
        output("Rating must be a number", color="red")
        return None
    if not rating_in_range(rating):
        output("Rating must be between 0 - 10", color="red")
        return None
    return float(rating)


def _get_movie_rating_optional(prompt: str) -> float | None:
    """Ask user to input a valid movie rating, or leave empty."""
    while True:
        rating = get_user_input_colored(prompt).strip()
        if rating == "":
            return None
        rating = _validate_rating(rating)
        if rating is not None:
            return rating


def get_movie_filters() -> tuple[float | None, int | None, int | None]:
    """Orchestrates getting user input on rating and release years."""
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
            output("Start hast do be before end", color="red")
        else:
            break
    return (filter_rating, filter_release_start, filter_release_end)


def get_file_name(prompt: str) -> str:
    """Ask user to input a valid movies rating."""
    while True:
        filename = get_user_input_colored(
            prompt,
        ).strip()
        if filename == "":
            output("Filename required", color="red")
        elif not filename.replace(".", "").isalnum():
            output("Filename must be alphanumeric", color="red")
        else:
            break
    return filename


def get_menu_selection() -> int | None:
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
        10: Stats
        11. Create ratings histogram
    """

    output("")

    for item in MENU_ITEMS:
        output(item, color="blue")

    insist_to_quit = False

    while True:
        selection = get_user_input_colored(
            "\nEnter choice (0-11): ",
        ).strip()

        if selection == "" and insist_to_quit:
            return None
        if (
            selection is not selection.isdecimal()
            and not menu_selection_in_range(selection)
        ):
            output(
                "Invalid input (Enter 0 - 11. Try again).\n"
                "Or press ENTER again to quit",
                color="red",
            )
            insist_to_quit = True
        else:
            break

    return int(selection)
