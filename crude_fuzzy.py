


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
    draw_table = [table]
    print(rjust("x", len(str2)), end="") # top left filler


    for i in range(len(table)):

        if i == 1:
            print(rjust("_", len(str2)))

        for j in range(len(table[i])):
            # top row
            if i == 0:
                if j == 0:
                    print(rjust("_", 6), end="")
                else:
                    print(rjust(str1[:j], 6), end="")

            # left column
            elif j == 0 and i <= len(str2):
                print(rjust(str2[:i], len(str2)), end="")

            # elif i > 0 and j > 0:
            #     print(rjust(str(table[i][j]), len(str1)), end=" ")

        print("")   # space rows 

# def draw_table(table:list[list[int | str]]):
#     print(rjust("x", len(str2)), end="")
#     for i in range(len(table)-1):
#         for j in range(len(table[i])-1):
#             if i == 0:
#                 # top row
#                 if j == 0:
#                     print(" "*(len(str1)-1) + str(table[i][j]), end=" "*len(str1))
#                 else:
#                     print(str(table[i][j]), end=(" ")*(len(str1)-j+1))

#             elif j == 0:
#                 # left column
#                 print(rjust(str(table[i][j]), len(str2)), end="")

#             else:
#                 print(rjust(str(table[i][j]), len(str1)), end=" ")
#         print("")   # space rows 
#         print("")

#     # print(table)


def init_table(str1:str, str2:str):

    data_matrix: list = []

    for i in range(0, len(str2)+2): # len word + extra 0 + range end not incl.
        row = []
        for j in range(0,len(str1)+1):  # len word + extra 0 
            if i == 0:
                # top row
                row.append(j)
            else: 
                if j == 0:
                    # left column
                    row.append(i-1)
                else:
                    row.append("?")
        data_matrix.append(row)


    draw_table(data_matrix)


init_table(str1, str2)