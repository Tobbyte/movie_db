"""Save a mathplotlob histogram to disk."""

import matplotlib.pyplot as plt
from app_config import DATA_DIR_PATH


def create_histogram(data: dict, filename: str) -> None:
    """Save a mathplotlob histogram to disk.

    Overrides if file already existing.
    """
    # TODO:
    #   - make data agnostic
    #   - check on other exceptions (f.e. no write perm)

    ratings_list = [info["rating"] for info in data.values()]
    plt.hist(ratings_list)

    try:
        plt.savefig(DATA_DIR_PATH / filename)

    except ValueError as e:
        # From mathplotlob
        error_msg = (
            "Format 'asd' is not supported (supported formats: "
            "avif, eps, gif, jpeg, jpg, pdf, pgf, png, ps, raw, rgba, svg, "
            "svgz, tif, tiff, webp)"
        )
        raise ValueError(error_msg) from e
