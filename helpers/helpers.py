from app_config import (
    MENU_ITEMS,
    MOVIE_MAX_RATING,
    MOVIE_MIN_RATING,
    OUTPUT_COLORS,
)


def is_num(inp: str) -> bool:
    """Validate if a sting input is a valid number."""
    if inp == "":
        return False
    try:
        float(inp)
    except ValueError:
        return False
    return True


def is_int(inp: str) -> bool:
    """Validate if a sting input is a valid int."""
    if inp == "" or "." in inp:
        return False
    try:
        int(inp)
    except ValueError:
        return False
    return True


def rating_in_range(inp: str) -> bool:
    """Validate if a rating is in allowed range."""
    return MOVIE_MIN_RATING <= float(inp) <= MOVIE_MAX_RATING


def strip_leading_zero(num: str | float) -> str | int | float:
    """Strip leading "0"s in input, returns same format."""
    res = str(num)
    while res[0] == "0" and len(res) > 1:
        res = res[1:]

    if isinstance(num, int):
        return int(res)
    if isinstance(num, float):
        return float(res)
    return res


def construct_filter_output(
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


def output(
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


def menu_selection_in_range(
    selection: str,
) -> bool:
    max_range = len(MENU_ITEMS)
    min_range = 0
    try:
        int(selection)
    except ValueError:
        return False
    else:
        return min_range <= int(selection) <= max_range + 1


def clear_screen() -> None:
    """Clear console hack."""
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
