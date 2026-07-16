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

DATA_DIR_PATH = Path("data_dir")
DATA_FILE_PATH = DATA_DIR_PATH / "data.json"
