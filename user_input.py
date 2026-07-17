from app_config import (
    CURRENT_YEAR,
    FIRST_MOVIE_RELEASE,
    OUTPUT_COLORS,
)
from helpers.helpers import (
    _is_int,
    _is_num,
    _output,
    _rating_in_range,
    _strip_leading_zero,
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


def _get_user_input_colored(promt: str) -> str:
    """Ask for user input, now in technicolor."""
    try:
        return input(OUTPUT_COLORS["yellow"] + promt)
    finally:
        # reset input coloring, also at EOF
        print("" + OUTPUT_COLORS["end"], end="")


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
