# ruff: noqa: FIX002, TD002, TD003, S311, TD005

"""A simple interface to interact with an dummy movie "db"."""

import datetime
import sys
from random import randint

import matplotlib.pyplot as plt
from my_fuzzy_search import get_similar

"""


TODO: (but out of scope of this exercise):
  - unify user input and validation across all features
  - add movie: check if already exists, present option to update
  - update movie: check if not existing, present option to add
  - update / delete movie: fuzzy search
  - delete movie: present list and let choose by inputting number
  - fix fail on empty db
  - add real clear terminal
  - implement fname from matplotlib instead naive str as filename
  - cache sorted db

Version 1.1.0 <- submitted
"""

"""
 ~ Made with ❤️ and without ai or code completion (except intelliSense) ~
"""


def main() -> None:
    """Run app and load movie db."""
    # Dictionary to store the movies and the rating
    movies = {
        "The Shawshank Redemption": {"rating": 9.5, "release": 1990},
        "Pulp Fiction": {"rating": 8.8, "release": 1990},
        "The Room": {"rating": 3.6, "release": 1990},
        "The Godfather": {"rating": 9.2, "release": 1990},
        "The Godfather: Part II": {"rating": 9.0, "release": 1990},
        "The Dark Knight": {"rating": 9.0, "release": 1990},
        "12 Angry Men": {"rating": 8.9, "release": 1990},
        "Everything Everywhere All At Once": {"rating": 8.9, "release": 1990},
        "Forrest Gump": {"rating": 8.8, "release": 1990},
        "Star Wars: Episode V": {"rating": 8.7, "release": 1990},
    }

    run(movies)


# dict used to shorthand color codes
OUTPUT_COLORS = {
    "red": "\033[91m",
    "blue": "\033[94m",
    "yellow": "\033[93m",
    "end": "\033[00m",
}

MOVIE_MIN_RATING = 0
MOVIE_MAX_RATING = 10
MENU_ITEMS = [
    "Menu:",
    "0. Exit",
    "1. List movies",
    "2. Add movie",
    "3. Delete movie",
    "4. Update movie",
    "5. Stats",
    "6. Random movie",
    "7. Search movie",
    "8. Movies sorted by rating",
    "9. Create ratings histogram",
]
FIRST_MOVIE_RELEASE = 1878
CURRENT_YEAR = datetime.datetime.now().year  # noqa: DTZ005


def get_as_list_sorted_by_rating(
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


def list_movies(db: dict[str, dict]) -> None:
    """Return a list of all db items."""
    output(f"{len(db)} movies in total:\n", space_before=True)
    for name, info in db.items():
        rating = info["rating"]
        release = info["release"]
        output(f"{name} ({release}): {rating}")


def list_movies_by_rating(db: dict[str, dict]) -> None:
    """Return a list of all db items by rating."""
    output("Movies by rating:\n", space_before=True)

    for name, info in get_as_list_sorted_by_rating(db, descending=True):
        release = info["release"]
        rating = info["rating"]
        output(f"{name} ({release}): {rating}")


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


def get_user_input_colored(promt: str) -> str:
    """Ask for user input, now in technicolor."""
    inp = input(OUTPUT_COLORS["yellow"] + promt)
    print("" + OUTPUT_COLORS["end"], end="")  # reset input coloring
    return inp


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


def add_movie(db: dict[str, dict]) -> None:
    """Add an item to db."""
    # TODO: Check if already exists.

    name = None
    rating = None
    release = None

    while name is None or name == "":
        name = get_user_input_colored("\nEnter new movie name: ").strip()
        if name == "":
            output("Name required", color="red")

    while release is None or release == "":
        release = get_user_input_colored(
            "Enter new movies year of release: ",
        ).strip()
        if release == "":
            output("Year required", color="red")
        elif not is_num(release):
            release = None
            output("Year must be a number", color="red")
        elif not is_int(release):
            release = None
            output("Year must be valid int", color="red")

        if release and int(release) < FIRST_MOVIE_RELEASE:
            release = None
            output(
                "Nice try. The first movie was released in "
                f"{FIRST_MOVIE_RELEASE}.",
                color="red",
            )
        elif release and int(release) > CURRENT_YEAR:
            release = None
            output(
                "Real futuristic movie - a rating from the future!",
                color="red",
            )

    while rating is None or rating == "":
        rating = get_user_input_colored(
            "Enter new movies rating (0-10): ",
        ).strip()
        if rating == "":
            output("Rating required", color="red")
        elif not is_num(rating):
            rating = None
            output("Rating must be a number", color="red")
        elif (
            float(rating) > MOVIE_MAX_RATING
            or float(rating) < MOVIE_MIN_RATING
        ):
            rating = None
            output("Rating must be between 0 - 10", color="red")

    rating = float(strip_leading_zero(float(rating)))
    db[name] = {"rating": rating, "release": release}  # TODO: build factory

    output(
        f'Movie "{name}" ({release}) with rating {rating} successfully added',
        space_before=True,
    )


def remove_movie(db: dict[str, float]) -> None:
    """Remove an item from db."""
    tbdeleted = None

    while tbdeleted is None or tbdeleted == "":
        tbdeleted = get_user_input_colored(
            "\nEnter (exact) movie name to delete: ",
        ).strip()
        if tbdeleted == "":
            output("Name required", color="red")
        try:
            del db[tbdeleted]
            output(
                f'Movie "{tbdeleted}" successfully deleted',
                space_before=True,
            )

        except KeyError:
            output(
                f"Movie {tbdeleted} doesn't exist!",
                space_before=True,
                color="red",
            )
            break


def update_movie(db: dict[str, dict]) -> None:
    """Update movie rating."""
    tbupdated = None
    new_rating = None

    while tbupdated is None or tbupdated == "":
        tbupdated = get_user_input_colored(
            "\nEnter (exact) movie name to update: ",
        ).strip()
        if tbupdated == "":
            output("Name required", color="red")
        try:
            db[tbupdated]
        except KeyError:
            output(
                f"Movie {tbupdated} doesn't exist!",
                space_before=True,
                color="red",
            )

    while new_rating is None or new_rating == "":
        new_rating = get_user_input_colored(
            "Enter new movies rating (0-10): ",
        ).strip()
        if new_rating == "":
            output("Rating required", color="red")
        elif not is_num(new_rating):
            new_rating = None
            output("Rating must be a number", color="red")
        elif (
            float(new_rating) > MOVIE_MAX_RATING
            or float(new_rating) < MOVIE_MIN_RATING
        ):
            new_rating = None
            output("Rating must be between 0 - 10", color="red")

    new_rating = strip_leading_zero(float(new_rating))
    db[tbupdated]["rating"] = float(new_rating)

    output(
        f'Movie "{tbupdated}" successfully updated to rating: {new_rating}',
        space_before=True,
    )


def get_average(nums: list[float]) -> float:
    """Return average."""
    return sum(nums) / len(nums)


def get_median(nums: list[float]) -> float:
    """Return median."""
    # TODO:
    #    - use import statistics

    sorted_nums = sorted(nums)
    if len(sorted_nums) % 2 != 0:
        return sorted_nums[len(sorted_nums) // 2]
    centeri = len(sorted_nums) // 2
    return get_average(sorted_nums[centeri - 1 : centeri + 1])


def get_extremes(
    db: dict[str, dict],
    *,
    descending: bool = True,
) -> list[tuple[str, dict]]:
    """Get the extreme values:[num] of dict."""
    sorted_by_rating = get_as_list_sorted_by_rating(db, descending=descending)

    # take rating of first item of sorted movies
    _, info = sorted_by_rating[0]
    extr_rating = info["rating"]

    return [
        (name, info)
        for (name, info) in sorted_by_rating
        if info["rating"] == extr_rating
    ]


def get_statistics(db: dict[str, float]) -> None:
    """Get statistics.

    - average
    - median
    - top-ranked items
    - bottom-ranged items
    """
    val_list = list(db.values())

    avg = get_average(val_list)
    median = get_median(sorted(val_list))
    rated_best = get_extremes(db)
    rated_worst = get_extremes(db, descending=False)

    output(f"Average rating: {avg}", space_before=True)
    output(f"Median rating: {median}")
    output("Best rated movie(s):")
    for best_name, best_rat in rated_best:
        output(f'   "{best_name}", {best_rat}')
    output("Worst rated movie(s):")
    for worst_name, worst_rat in rated_worst:
        output(f'   "{worst_name}", {worst_rat}')


def get_random(db: dict[str, float]) -> None:
    """Return random movie."""
    name, rating = list(db.items())[randint(0, len(db) - 1)]
    output(
        f"Your movie for tonight: {name}, it's rated {rating}",
        space_before=True,
    )


def search_movie(db: dict[str, float]) -> None:
    """Search for items.

    Not case sensitive.
    """
    user_input = None
    while user_input is None or user_input == "":
        user_input = get_user_input_colored(
            "\nEnter part of movie name: ",
        ).strip()
        if user_input == "":
            output("Name required", color="red")

    user_input_lowered = user_input.lower()

    # create a dict of lowered_name:original_name for search comparison
    # TODO: cache

    db_lowered = {}
    for m in db:
        m_lo = m.lower()
        db_lowered[m_lo] = m

    if user_input in db:
        # Name is in db as put in
        output(f"{user_input}, {db[user_input]}", space_before=True)
    elif user_input_lowered in db_lowered:
        # Name is lowercase of db entry
        output(
            f"{db_lowered[user_input_lowered]}, "
            f"{db[db_lowered[user_input_lowered]]}",
            space_before=True,
        )

    else:
        # No direct finding, fuzzy
        search_results = fuzzy_search(db, user_input_lowered)

        found_titles = [
            (found, db.get(found)) for (found, _) in search_results
        ]

        if not found_titles:
            output(
                f'No Movie name similar to "{user_input}"'
                "(remember that at least the first letter has to match):\n",
                color="red",
            )
        else:
            output(
                f'No movie titled "{user_input}" found. Did you mean:\n',
                space_before=True,
            )

            for name, rate in found_titles:
                output(f"{name}, {rate}")


def fuzzy_search(db: dict[str, float], search_term: str) -> list[tuple]:
    """Fuzzy search on term, results sorted by distance."""
    similarity_threshold = 25  # pretty high. Workaround until optimized
    titles = list(db.keys())

    return get_similar(titles, search_term, similarity_threshold)


def ratings_histogram(db: list[float]) -> None:
    """Save a mathplotlob histogram to disk."""
    filename = None
    plt.hist(db)
    while filename is None or filename == "":
        filename = get_user_input_colored(
            "Enter filename (saved as png unless otherwise specified"
            "in your current working directory): ",
        ).strip()
        if filename == "":
            output("Filename required", color="red")
        elif not filename.replace(".", "").isalnum():
            output("Filename must be alphanumeric", color="red")
            filename = None
        else:
            try:
                plt.savefig(filename)
                output(
                    f'File "{filename}" successfully saved to disk.',
                    space_before=True,
                )
            except ValueError:
                # TODO:
                #   - check on other exceptions (f.e. no write perm)

                output(  # From mathplotlob
                    "Format 'asd' is not supported (supported formats: "
                    "avif, eps, gif, jpeg, jpg, pdf, pgf, png, ps, raw, rgba, "
                    "svg, svgz, tif, tiff, webp)",
                    color="red",
                )


def idle_after_input() -> None:
    """Idle with prompt to continue."""
    get_user_input_colored("\npress Enter to continue ")


def present_menu(menu_items: list[str]) -> int:
    """Print the menu to the user, asks for input."""
    """ Options:
        1. List movies, no input. Print. Return to menu.
        2. Add movie, single input:
            - str, int:[1-10] (not validated). Print new Entry.
            Return to menu.
        3. Delete movie, single input:
            - str. Print error or confirmation. Return to menu.
        4. Update movie, multi input:
            1.: str. Print error if not found. Return to menu.
            2.: int:[1-10] (not validated). Print new Entry.
            Return to menu.
        5. Stats, no input. Print. Return to menu.
        6. Random movie, no input. Print. Return to menu.
        7. Search movie, single input:
            - str. Print error or results. Return to menu.
        8. List movies sorted descending, no input. Print.
        Return to menu.
        9. Create ratings histogram
        0. Exit.
    """

    output("")

    for item in menu_items:
        output(item, color="blue")

    selection = None
    insist_to_quite = False
    while selection is None:
        selection = get_user_input_colored(
            "\nEnter choice (0-9): ",
        ).strip()

        if len(selection) > 1 or not selection.isdecimal():
            if not insist_to_quite:
                output(
                    "Invalid input (Enter 0 - 9. Try again).\n"
                    "Or press ENTER again to quit",
                    color="red",
                )
                selection = None
                insist_to_quite = True
            else:
                quit_program()

    return int(selection)


def quit_program() -> None:
    """Quit."""
    output("Bye!")
    sys.exit()


def clear_screen() -> None:
    """Clear console hack."""
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")


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


def run(db: dict[str, float]) -> None:
    """Print welcome and loop menu."""
    first_run = True
    clear_screen()
    output(
        "********** My Movies Database **********",
        color="blue",
    )

    menu_dispatch = {
        1: list_movies,
        2: add_movie,
        3: remove_movie,
        4: update_movie,
        5: get_statistics,
        6: get_random,
        7: search_movie,
        8: list_movies_by_rating,
        # 0: quit_program handled separately
    }

    while True:
        if not first_run:
            clear_screen()
        first_run = False

        selection = present_menu(MENU_ITEMS)

        if selection == 0:
            quit_program()
        else:
            clear_screen()
            output(
                f"~~~~~~~~~~\nSelected menu item:"
                f"{MENU_ITEMS[selection + 1]}\n"
                "~~~~~~~~~~",
                color="yellow",
            )

            menu_dispatch[selection](db)

            idle_after_input()


if __name__ == "__main__":
    main()
