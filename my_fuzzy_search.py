import copy


"""
 ~~ Made with  and without ai or code completion (except intelliSense) ~~
"""


def print_fuzzy_table(table: list, str1: str, str2: str):
    """pretty print the table"""
    header = str1
    column = str2

    first_col_w = len(column)
    cell_w = len(header)

    # header Row
    header_row: list[str] = ["_"]
    for i in range(len(header)):
        header_row.append(header[: i + 1])

    # body rows
    display_rows: list[list[str | int]] = []
    original_row: list[int | str] = []

    for i, original_row in enumerate(table):
        row_copy = list(original_row)
        row_prefix = "_" if i == 0 else column[:i]
        row_copy.insert(0, row_prefix)
        display_rows.append(row_copy)

    print("")

    # Print header Row
    print("▦".rjust(first_col_w), end="")
    # Align to first data column
    print(" " * (first_col_w + 1), end="")

    for cell in header_row:
        print(str(cell).ljust(cell_w + 1), end="")

    print("\n")

    # print data rows
    for row in display_rows:
        # first cell (row labels)
        print(str(row[0]).rjust(first_col_w), end=" ")

        for cell in row[1:]:
            print(str(cell).rjust(cell_w), end=" ")
        print("\n")


def calc_distance(search_term: str, compar_term: str, print_table=False):

    data_matrix = init_table(search_term, compar_term)

    data_copy = copy.deepcopy(data_matrix)

    for row in range(1, len(data_copy)):
        for column in range(1, len(data_copy[row])):
            left_cell = data_copy[row][column - 1] + 1
            top_cell = data_copy[row - 1][column] + 1
            diag_top_char = (
                "" if column - 1 > len(search_term) - 1 else search_term[column - 1]
            )
            diag_left_char = (
                "" if column - 1 > len(compar_term) - 1 else compar_term[column - 1]
            )
            diag_is_diff = 0

            if diag_top_char != diag_left_char:
                diag_is_diff = 1
            diag = data_copy[row - 1][column - 1] + diag_is_diff
            data_copy[row][column] = min(left_cell, top_cell, diag)

    if print_table:
        print("\n\n\n\n\n\n")
        print_fuzzy_table(data_copy, search_term, compar_term)
        print(f"distance: {data_copy[-1][-1]}")

    return data_copy[-1][-1]


def init_table(str1: str, str2: str):

    data_matrix: list = []

    for i in range(0, len(str2) + 1):
        row = []
        for j in range(0, len(str1) + 1):  # len word + extra 0
            if i == 0:
                # top row
                row.append(j)
            else:
                if j == 0:
                    # left column
                    row.append(i)
                else:
                    row.append(-1)
        data_matrix.append(row)

    return data_matrix


excluded_terms = ["the "]


def strip_excluded_terms(term: str):
    stripped = term
    for exc in excluded_terms:
        stripped = stripped.replace(exc, "")
    return stripped


def any_first_char_matching(term1:str, term2:str):
    lterm1 = term1.split()
    lterm2 = term2.split()
    for w1 in lterm1:
        for w2 in lterm2:
            if w1[0] == w2[0]:
                return True 


def get_similar(db: list[str], search_term, threshold, print_table=False):

    search_term_wo_excluded = strip_excluded_terms(search_term).lower()

    similar_results:list[tuple] = []
    for item in db:
        item_wo_excluded = strip_excluded_terms(item.lower()).lower()
        print(search_term_wo_excluded, item_wo_excluded)
        dist = calc_distance(search_term_wo_excluded, item_wo_excluded, print_table=print_table)
        
        # naively demand first char matching
        if dist <= threshold and any_first_char_matching(search_term_wo_excluded,item_wo_excluded):
            similar_results.append((item, dist))

    similar_results = sorted(similar_results, key=lambda dist: dist[1])
    return similar_results



if __name__ == "__main__":
    pass