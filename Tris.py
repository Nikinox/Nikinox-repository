x=10
o=11
spreadsheet=[1, 2, 3, 4, 5, 6, 7, 8, 9]
turn="x"
x_move = 0
o_move = 0
while True:
    if turn=="x":
        print("X turn: put a cross in a free slot")
        x_move=int(input())
        while (x_move<1 or x_move>9):
            print("error")
            x_move=int(input())
        spreadsheet[x_move-1] = x
        turn="o"
    if turn =="o":
        print("O turn: put a cross in a free slot")
        x_move=int(input())
        while (o_move<1 or o_move>9):
            print("error")
            o_move=int(input())
        spreadsheet[o_move-1] = o
        turn="x"
    if spreadsheet==[10, 10, 10, 4, 5, 6, 7, 8, 9] or spreadsheet==[1, 2, 3, 10, 10, 10, 7, 8, 9] or spreadsheet==[1, 2, 3, 4, 5, 6, 10, 10, 10] or spreadsheet==[10, 2, 3, 10, 5, 6, 10, 8, 9] or spreadsheet==[1, 10, 3, 4, 10, 6, 7, 10, 9] or spreadsheet==[1, 2, 10, 4, 5, 10, 7, 8, 10] or spreadsheet==[10, 2, 3, 4, 10, 6, 7, 8, 10] or spreadsheet==[1, 2, 10, 4, 10, 6, 10, 8, 9]:
        print("X win")
        break

    if spreadsheet==[11, 11, 11, 4, 5, 6, 7, 8, 9] or spreadsheet==[1, 2, 3, 11, 11, 11, 7, 8, 9] or spreadsheet==[1, 2, 3, 4, 5, 6, 11, 11, 11 or spreadsheet==[11, 2, 3, 11, 5, 6, 11, 8, 9] or spreadsheet==[1, 11, 3, 4, 11, 6, 7, 11, 9] or spreadsheet==[1, 2, 11, 4, 5, 11, 7, 8, 11] or spreadsheet==[11, 2, 3, 4, 11, 6, 7, 8, 11] or spreadsheet==[1, 2, 11, 4, 11, 6, 11, 8, 9]:
                                                                                                                   
        
        print("O win")
        break
