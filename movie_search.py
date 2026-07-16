"""Search in data by query."""

from my_fuzzy_search import get_similar


def movie_search(data: dict[str, dict], query: str) -> list[tuple]:
    """Search for movies names that match query.

    Returns list of tuples with (name, info).
    Uses fuzzy search to return approximates.
    """
    query_lowered = query.lower()
    data_lowered = {}

    # create a dict of lowered_name:original_name for search comparison
    # TODO: cache / better let be provided by movie_storage
    for m in data:
        m_lo = m.lower()
        data_lowered[m_lo] = m

    if query in data:
        # Name is in data as put in
        return [(query, data[query])]
    if query_lowered in data_lowered:
        # Name is lowercase of movie title
        return [
            (data_lowered[query_lowered], data[data_lowered[query_lowered]]),
        ]

    # No direct finding, fuzzy
    search_results = _fuzzy_search(data, query_lowered)

    if not search_results:
        raise ValueError

    return [(title, data[title]) for title, _ in search_results]


def _fuzzy_search(db: dict[str, dict], search_term: str) -> list[tuple]:
    """Fuzzy search on term, results sorted by distance.

    Returns list of tuples (similar-to-term, distance)
    """
    similarity_threshold = 25  # pretty high. Workaround until optimized
    titles = list(db.keys())

    return get_similar(titles, search_term, similarity_threshold)
