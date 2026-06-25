


from wcwidth import rjust

#        ""  m  a  r  e
#    ""  0   1  2  3  4
#    c   1   1  ?  ?  ?
#    a   2   ?  ?  ?  ?
#    r   3   ?  ?  ?  ?
#    s   4   ?  ?  ?  ?

# table = [
#     [0, 1, 2, 3, 4],      # Zeile 0 (das Gerüst oben)
#     [1, 1, ?, ?, ?],      # Zeile 1 (für 'c')
#     [2, ?, ?, ?, ?],      # Zeile 2 (für 'a')
#     [3, ?, ?, ?, ?],      # Zeile 3 (für 'r')
#     [4, ?, ?, ?, ?]       # Zeile 4 (für 's')
# ]

# x    _ M Ma Mar 
#    _ ? ? ? ? 
#    C ? ? ? ? 
#   Ca ? ? ? ? 
#  Car ? ? ? ? 
# Cars ? ? ? ?

str1 = "Mares"
str2 = "Cars"

def edit_distance():
    # schaut links: 
    pass

def draw_table(table:list[list[int | str]]):

    header = str1
    column = str2
    header_row: list[str | int] = ["_"]
    draw_table = list(table)
    first_column_width = len(column)
    column_width = len(header)

    """add header and first row to data"""
    # create header row with ascending length of str1
    for i in range(len(header)):
        header_row.append(str(header[:i+1]))

    draw_table.insert(0, header_row)

    # loop table, insert str2 in ascending as row 1
    for i in range(0,len(table)):
        if i == 0:
            draw_table[1].insert(0, "_")
        else:
            draw_table[i+1].insert(0, str(column[:i]))

    print("") # break line

    """print table"""
    for i in range(len(draw_table)):
        row = draw_table[i]
        if i == 0:
            # header row, needs special padding to account for rjust of 1 column
            # add icon in corner for fun
            for j in range(len(row)):
                if j == 0:
                    # pad for first column
                    print(" "*(first_column_width-1), end="")
                    print("▦",end="")
                    print(" "*(column_width), end="")
                
                # pad first row: dist between words gets smaller
                print(str(row[j]).ljust(column_width + 1), end="")

        else: 
            for j in range(len(row)):
                if j == 0:
                    print(str(row[j]).rjust(first_column_width), end=" ")
                else:
                    print(str(row[j]).rjust(column_width), end=" ")
        print("")
        print("")


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

    draw_table(data_matrix)


init_table(str1, str2)