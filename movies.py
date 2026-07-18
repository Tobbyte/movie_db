# ruff: noqa: RUF015
"""Main entry point with menu orchestration and handler dispatch."""

import sys

from app_config.app_config import MENU_ITEMS
from data_handling.data_provider import (
    get_movies_count,
)
from data_handling.movie_storage import assure_db_exists
from helpers.helpers import clear_screen, output
from movies_handlers import (
    add_movie,
    list_movies,
    list_movies_by_filter,
    list_movies_by_rating,
    list_movies_by_release,
    list_statistics,
    random_movie,
    ratings_histogram,
    remove_movie,
    search_movie,
    update_movie,
)
from user_input.user_input import (
    get_menu_selection,
    get_user_input_colored,
)

"""
TODO: (but out of scope of this exercise):
  - add movie: check if already exists, present option to update
  - update movie: check if not existing, present option to add
  - update / delete movie: fuzzy search
  - delete movie: present list and let choose by inputting number
  - fix fail on empty db
  - add real clear terminal
  - implement fname from matplotlib instead naive str as filename
  - pretty align movie outputs


Version 2.2. <- submitted
"""

"""
 ~ Made with ❤️ and without ai or code completion (except intelliSense) ~
"""


def run() -> None:
    """Print welcome and loop menu."""
    assure_db_exists()
    first_run = True
    clear_screen()
    output(
        "********** My Movies Database **********",
        color="blue",
    )

    menu_dispatch = {
        0: _quit_program,
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
    }

    while True:
        if not first_run:
            clear_screen()
        first_run = False

        selection = get_menu_selection()

        if not selection:
            _quit_program()

        else:
            i_of_add_movie = [
                key
                for key, value in menu_dispatch.items()
                if value == add_movie
            ][0]

            if get_movies_count() == 0 and selection != i_of_add_movie:
                output(
                    "No movies in db. "
                    f"You can only add one (press {i_of_add_movie}).",
                    color="red",
                )
            else:
                clear_screen()
                output(
                    f"~~~~~~~~~~\nSelected menu item: "
                    f"{MENU_ITEMS[selection]}\n"
                    "~~~~~~~~~~",
                    color="yellow",
                )

                menu_dispatch[selection]()

            _idle_after_input()


def _idle_after_input() -> None:
    """Idle with prompt to continue."""
    get_user_input_colored("\npress Enter to continue ")


def _quit_program() -> None:
    """Quit with farewell."""
    output("Bye!")
    sys.exit()


def main() -> None:
    """Run app."""
    run()


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        # quit gratefully on termination
        print("\nThat was sudden. Goodbye!\n")
        sys.exit()
