# ruff: noqa: FIX002, TD002, TD003, TD005
"""Save a mathplotlob histogram to disk."""
import matplotlib.pyplot as plt

from app_config.app_config import DATA_DIR_PATH


def create_histogram(data: dict, filename: str) -> tuple[str, str] | None:
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
        return _full_file_name(filename)

    except ValueError as e:
        split_filename = filename.split(".")
        invalid_extension = split_filename[-1]
        # From mathplotlob
        error_msg = (
            f'File extension "{invalid_extension}" is not supported '
            "(supported formats: avif, eps, gif, jpeg, jpg, "
            "pdf, pgf, png, ps, raw, rgba, svg, svgz, tif, tiff, webp)"
        )
        raise ValueError(error_msg) from e
    finally:
        plt.close()

def _full_file_name(filename: str) -> tuple[str, str]:
    """Return the filename with extension of not present.

    If the user has not put in an extension, return filename with
    default extension (png)
    """
    while filename[-1] == ".":
        filename = filename[:-1]
    if "." in filename:
        split_filename = filename.split(".")

        extension = "." + split_filename[-1]
        name = ".".join(split_filename[:-1])
        return name, extension
    return filename, ".png"
