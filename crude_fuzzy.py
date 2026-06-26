


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


def init_table(str1:str, str2:str):

    data_matrix: list = []

    for i in range(0, len(str2)+1):
        row = []
        for j in range(0,len(str1)+1):  # len word + extra 0 
            if i == 0:
                # top row
                row.append(j)
            else: 
                if j == 0:
                    # left column
                    row.append(i)
                else:
                    row.append("?")
        data_matrix.append(row)

    print_fuzzy_table(data_matrix, str1, str2)


init_table(str1, str2)