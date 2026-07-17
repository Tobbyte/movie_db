"""Config Data for movies app."""

import datetime
from pathlib import Path

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
    "0.  Exit",
    "1.  List movies",
    "2.  List movies rating",
    "3.  List movies release",
    "4.  List movies by filter",
    "5.  Search movie",
    "6.  Random movie",
    "7.  Add movie",
    "8.  Update movie",
    "9.  Delete movie",
    "10.  Stats",
    "11. Create ratings histogram",
]
FIRST_MOVIE_RELEASE = 1878
CURRENT_YEAR = datetime.datetime.now().year  # noqa: DTZ005

DATA_DIR_PATH = Path("data_dir")
DATA_FILE_PATH = DATA_DIR_PATH / "data.json"
