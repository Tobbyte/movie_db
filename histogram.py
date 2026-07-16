"""Save a mathplotlob histogram to disk."""

from pathlib import Path

import matplotlib.pyplot as plt

FILE_PATH = Path("data_dir")


def create_histogram(data: dict, filename: str) -> str:
    """Save a mathplotlob histogram to disk.

    Overrides if file already existing.
    """
    # TODO:
    #   - make data agnostic
    #   - check on other exceptions (f.e. no write perm)

    ratings_list = [info["rating"] for info in data.values()]
    plt.hist(ratings_list)

    try:
        plt.savefig(FILE_PATH / filename)

    except ValueError:
        return (  # From mathplotlob
            "Format 'asd' is not supported (supported formats: "
            "avif, eps, gif, jpeg, jpg, pdf, pgf, png, ps, raw, rgba, "
            "svg, svgz, tif, tiff, webp)"
        )
    else:
        return f'File "{filename}" successfully saved to disk.'
