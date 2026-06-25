


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
    print(rjust("x", len(str2)), end="")
    for i in range(len(table)-1):
        for j in range(len(table[i])-1):
            if i == 0:
                # top row
                if j == 0:
                    print(" "*(len(str1)-1) + str(table[i][j]), end=" "*len(str1))
                else:
                    print(str(table[i][j]), end=(" ")*(len(str1)-j+1))

            elif j == 0:
                # left column
                print(rjust(str(table[i][j]), len(str2)), end="")

            else:
                print(rjust(str(table[i][j]), len(str1)), end=" ")
        print("")   # space rows 
        print("")

    # print(table)


def init_table(str1:str, str2:str):
    str1 = "_" + str1
    str2 = "_" + str2

    table: list = [["_"]]
    
    for i in range(1, len(str1)+1):
        table[0].append(str1[1:i+1])

    table.append(["_"])

    for i in range(1,len(str2)+1):
        if i != 0:
            table.append([str2[1:i+1]])
        for j in range(1,len(str1)+2):

            if j == 0:
                table[i].append("?")
            elif i==1:
                table[i].append(j-1)
            elif j==1:
                table[i].append(i-1)
            else:
                table[i].append("?")

    draw_table(table)


init_table(str1, str2)