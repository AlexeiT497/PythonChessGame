import sys
import pygame as pg
import math
import time
import itertools

sys.setrecursionlimit(100000)
chrs = {
    'b_checker': u'\u25FB',
    'w_pawn': u'\u265F',
    'w_rook': u'\u265C',
    'w_knight': u'\u265E',
    'w_bishop': u'\u265D',
    'w_king': u'\u265A',
    'w_queen': u'\u265B',
    'w_checker': u'\u25FC',
    'b_pawn': u'\u2659',
    'b_rook': u'\u2656',
    'b_knight': u'\u2658',
    'b_bishop': u'\u2657',
    'b_king': u'\u2654',
    'b_queen': u'\u2655'
}

image_chrs = {
    'w_pawn': pg.image.load("img\whitep.png"),
    'w_rook': pg.image.load("img\whiter.png"),
    'w_knight': pg.image.load("img\whiten.png"),
    'w_bishop':pg.image.load("img\whiteb.png"),
    'w_king': pg.image.load("img\whitek.png"),
    'w_queen': pg.image.load("img\whiteq.png"),
    'b_pawn': pg.image.load("img\\blackp.png"),
    'b_rook': pg.image.load("img\\blackr.png"),
    'b_knight': pg.image.load("img\\blackn.png"),
    'b_bishop': pg.image.load("img\\blackb.png"),
    'b_king': pg.image.load("img\\blackk.png"),
    'b_queen': pg.image.load("img\\blackq.png")
}


# created in the perspective of the computer winning
piece_value = {
    chrs['b_pawn']: -10,
    chrs['b_rook']: -50,
    chrs['b_knight']: -30,
    chrs['b_bishop']: -30,
    chrs['b_king']: -900,
    chrs['b_queen']: -90,
    chrs['w_pawn']: 10,
    chrs['w_rook']: 50,
    chrs['w_knight']: 30,
    chrs['w_bishop']: 30,
    chrs['w_king']: 900,
    chrs['w_queen']: 90
}

total_turns = 0

checkered_board = []
from_pos = []
to_pos = []

def place_checkers():
    global chrs
    global checkered_board
    checkered_board = []
    white = True
    temp_list = []
    for i in range(65):
        if i % 8 == 0 and i != 0:
            checkered_board.append(temp_list)
            temp_list = []
            white = not white
        if white:
            temp_list.append(chrs['w_checker'])
        else:
            temp_list.append(chrs['b_checker'])
        white = not white



place_checkers()

# position is like that of a matrix (y, x)
computer_pieces = [[chrs['b_rook'], 1, 1], [chrs['b_knight'], 1, 2], [chrs['b_bishop'], 1, 3],
                [chrs['b_queen'], 1, 4], [chrs['b_king'], 1, 5], [chrs['b_bishop'], 1, 6],
                [chrs['b_knight'], 1, 7], [chrs['b_rook'], 1, 8]]

human_pieces = [[chrs['w_rook'], 8, 1], [chrs['w_knight'], 8, 2], [chrs['w_bishop'], 8, 3],
                [chrs['w_queen'], 8, 4], [chrs['w_king'], 8, 5], [chrs['w_bishop'], 8, 6],
                [chrs['w_knight'], 8, 7], [chrs['w_rook'], 8, 8]]

for i in range(8):
    computer_pieces.append([chrs['b_pawn'], 2, i + 1])

for i in range(8):
    human_pieces.append([chrs['w_pawn'], 7, i + 1])

def display_board():
    global checkered_board
    global chrs
    place_checkers()
    copy_board = checkered_board.copy()
    string = ""
    counter = 0
    for i in human_pieces:
        copy_board[i[1] - 1][i[2] - 1] = i[0]

    for i in computer_pieces:

        copy_board[i[1] - 1][i[2] - 1] = i[0]

    for i in copy_board:
        print("    ". join(i))

def value(coordinates):
    global piece_value
    return_value = 0
    for i in human_pieces:
        if i[1] == coordinates[0] and i[2] == coordinates[1]:
            return_value = piece_value[i[0]]
            return return_value

    for i in computer_pieces:
        if i[1] == coordinates[0] and i[2] == coordinates[1]:
            return_value = piece_value[i[0]]
            return return_value

    return return_value

def remove_piece(coordinates):
    global human_pieces
    global computer_pieces

    for counter, i in enumerate(human_pieces):
        if i[1] == coordinates[0] and i[2] == coordinates[1]:
            human_pieces.pop(counter)
            return

    for counter, i in enumerate(computer_pieces):
        if i[1] == coordinates[0] and i[2] == coordinates[1]:
            computer_pieces.pop(counter)
            return


def computer_updater(current, new):
    global computer_pieces
    for counter, values in enumerate(computer_pieces):
        if values[1] == current[0] and values[2] == current[1]:
            computer_pieces[counter][1] = new[0]
            computer_pieces[counter][2] = new[1]
            return


def human_updater(current, new):
    global human_pieces
    for counter, values in enumerate(human_pieces):
        if values[1] == current[0] and values[2] == current[1]:
            human_pieces[counter][1] = new[0]
            human_pieces[counter][2] = new[1]
            return

def user_input_updater(from_pos, to_pos):
    global human_pieces
    acceptable = False
    print(from_pos, to_pos)
    for j in human_pieces:
        if [to_pos[1], to_pos[0]] in return_possible_moves(j):
            acceptable = True
            break

    if acceptable:
        for counter, values in enumerate(human_pieces):

            if values[1] == from_pos[1] and values[2] == from_pos[0]:
                human_pieces[counter][1] = to_pos[1]
                human_pieces[counter][2] = to_pos[0]
                delete_piece(human_pieces[counter])
                break
    else:
        print("Nope, illegal move.")


def delete_piece(moving):
    global human_pieces
    global computer_pieces

    if moving in human_pieces:
        for counter, j in enumerate(computer_pieces):
            if moving[1] == j[1] and moving[2] == j[2]:
                computer_pieces.pop(counter)
                return

    elif moving in computer_pieces:
        for counter, j in enumerate(human_pieces):
            if moving[1] == j[1] and moving[2] == j[2]:
                human_pieces.pop(counter)
                return


def return_possible_moves(piece_list):
    global human_pieces
    global computer_pieces
    global total_turns
    global chrs
    return_list = []
    perm = True

    if piece_list[0] == chrs['w_pawn']:

        for counter, i in enumerate(human_pieces):
            if piece_list[1] - 1 == i[1] and piece_list[2] == i[2]:
                perm = False


        for counter, i in enumerate(computer_pieces):
            if piece_list[1] - 1 == i[1] and piece_list[2] == i[2]:
                perm = False
            elif counter == len(computer_pieces) - 1 and perm:
                return_list.append([piece_list[1] - 1, piece_list[2]])

        if piece_list[1] == 7 and perm:
            for counter, i in enumerate(human_pieces):
                if piece_list[1] - 2 == i[1] and piece_list[2] == i[2]:
                    perm = False
                elif counter == len(human_pieces) - 1 and perm:
                    return_list.append([piece_list[1] - 2, piece_list[2]])

        for counter, i in enumerate(computer_pieces):
            if piece_list[1] - 1 == i[1] and (i[2] == piece_list[2] - 1):
                return_list.append([piece_list[1] - 1, piece_list[2] - 1])
            if piece_list[1] - 1 == i[1] and i[2] == piece_list[2] + 1:
                return_list.append([piece_list[1] - 1, piece_list[2] + 1])

    elif piece_list[0] == chrs['b_pawn']:

        for counter, i in enumerate(computer_pieces):
            if piece_list[1] + 1 == i[1] and piece_list[2] == i[2]:
                perm = False

        for counter, i in enumerate(human_pieces):
            if piece_list[1] + 1 == i[1] and piece_list[2] == i[2]:
                perm = False

            elif counter == len(human_pieces) - 1 and perm:
                return_list.append([piece_list[1] + 1, piece_list[2]])

        if piece_list[1] == 2 and perm:
            for counter, i in enumerate(computer_pieces):
                if piece_list[1] + 2 == i[1] and piece_list[2] == i[2]:
                    perm = False
                elif counter == len(computer_pieces) - 1 and perm:
                    return_list.append([piece_list[1] + 2, piece_list[2]])

        for counter, i in enumerate(human_pieces):
            if piece_list[1] + 1 == i[1] and (i[2] == piece_list[2] - 1):
                return_list.append([piece_list[1] + 1, piece_list[2] - 1])
            if piece_list[1] + 1 == i[1] and i[2] == piece_list[2] + 1:
                return_list.append([piece_list[1] + 1, piece_list[2] + 1])

    elif piece_list[0] == chrs['w_bishop']:
        down_right = []
        down_left = []
        up_right = []
        up_left = []
        for i in range(1, 9):
            if piece_list[1] + i <= 8 and piece_list[2] + i <= 8:
                down_right.append([piece_list[1] + i, piece_list[2] + i])

            if piece_list[1] + i <= 8 and piece_list[2] - i >= 1:
                down_left.append([piece_list[1] + i, piece_list[2] - i])

            if piece_list[1] - i >= 1 and piece_list[2] + i <= 8:
                up_right.append([piece_list[1] - i, piece_list[2] + i])

            if piece_list[1] - i >= 1 and piece_list[2] - i >= 1:
                up_left.append([piece_list[1] - i, piece_list[2] - i])

        # reviews the lists from previous to avoid collision with own sort

        for counter, i in enumerate(human_pieces):
            for counter_pos, j in enumerate(down_right):
                if i[1] == j[0] and i[2] == j[1]:
                    down_right[counter_pos:len(down_right)] = []

            for counter_pos, j in enumerate(down_left):
                if i[1] == j[0] and i[2] == j[1]:
                    down_left[counter_pos:len(down_left)] = []

            for counter_pos, j in enumerate(up_right):
                if i[1] == j[0] and i[2] == j[1]:
                    up_right[counter_pos:len(up_right)] = []

            for counter_pos, j in enumerate(up_left):
                if i[1] == j[0] and i[2] == j[1]:
                    up_left[counter_pos:len(up_left)] = []

        # same as previous chunk but for the enemy's sort
        for counter, i in enumerate(computer_pieces):
            for counter_pos, j in enumerate(down_right):
                if i[1] == j[0] and i[2] == j[1]:
                    down_right[counter_pos + 1:len(down_right)] = []

            for counter_pos, j in enumerate(down_left):
                if i[1] == j[0] and i[2] == j[1]:
                    down_left[counter_pos + 1:len(down_left)] = []

            for counter_pos, j in enumerate(up_right):
                if i[1] == j[0] and i[2] == j[1]:
                    up_right[counter_pos + 1:len(up_right)] = []

            for counter_pos, j in enumerate(up_left):
                if i[1] == j[0] and i[2] == j[1]:
                    up_left[counter_pos + 1:len(up_left)] = []

        # adds to the return_list
        for i in up_left:
            return_list.append(i)
        for i in up_right:
            return_list.append(i)
        for i in down_left:
            return_list.append(i)
        for i in down_right:
            return_list.append(i)

    elif piece_list[0] == chrs['b_bishop']:
        down_right = []
        down_left = []
        up_right = []
        up_left = []
        for i in range(1, 9):
            if piece_list[1] + i <= 8 and piece_list[2] + i <= 8:
                down_right.append([piece_list[1] + i, piece_list[2] + i])

            if piece_list[1] + i <= 8 and piece_list[2] - i >= 1:
                down_left.append([piece_list[1] + i, piece_list[2] - i])

            if piece_list[1] - i >= 1 and piece_list[2] + i <= 8:
                up_right.append([piece_list[1] - i, piece_list[2] + i])

            if piece_list[1] - i >= 1 and piece_list[2] - i >= 1:
                up_left.append([piece_list[1] - i, piece_list[2] - i])

        # reviews the lists from previous to avoid collision with own sort

        for counter, i in enumerate(computer_pieces):
            for counter_pos, j in enumerate(down_right):
                if i[1] == j[0] and i[2] == j[1]:
                    down_right[counter_pos:len(down_right)] = []

            for counter_pos, j in enumerate(down_left):
                if i[1] == j[0] and i[2] == j[1]:
                    down_left[counter_pos:len(down_left)] = []

            for counter_pos, j in enumerate(up_right):
                if i[1] == j[0] and i[2] == j[1]:
                    up_right[counter_pos:len(up_right)] = []

            for counter_pos, j in enumerate(up_left):
                if i[1] == j[0] and i[2] == j[1]:
                    up_left[counter_pos:len(up_left)] = []

        # same as previous chunk but for the enemy's sort
        for counter, i in enumerate(human_pieces):
            for counter_pos, j in enumerate(down_right):
                if i[1] == j[0] and i[2] == j[1]:
                    down_right[counter_pos + 1:len(down_right)] = []

            for counter_pos, j in enumerate(down_left):
                if i[1] == j[0] and i[2] == j[1]:
                    down_left[counter_pos + 1:len(down_left)] = []

            for counter_pos, j in enumerate(up_right):
                if i[1] == j[0] and i[2] == j[1]:
                    up_right[counter_pos + 1:len(up_right)] = []

            for counter_pos, j in enumerate(up_left):
                if i[1] == j[0] and i[2] == j[1]:
                    up_left[counter_pos + 1:len(up_left)] = []

        # adds to the return_list
        for i in up_left:
            return_list.append(i)
        for i in up_right:
            return_list.append(i)
        for i in down_left:
            return_list.append(i)
        for i in down_right:
            return_list.append(i)

    elif piece_list[0] == chrs['w_rook']:
        up = []
        down = []
        left = []
        right = []
        for i in range(1, 9):
            if piece_list[1] + i <= 8:
                down.append([piece_list[1] + i, piece_list[2]])

            if piece_list[1] - i >= 1:
                up.append([piece_list[1] - i, piece_list[2]])

            if piece_list[2] + i <= 8:
                right.append([piece_list[1], piece_list[2] + i])

            if piece_list[2] - i >= 1:
                left.append([piece_list[1],  piece_list[2] - i])

        for counter, i in enumerate(human_pieces):
            for counter_pos, j in enumerate(down):
                if i[1] == j[0] and i[2] == j[1]:
                    down[counter_pos:len(down)] = []

            for counter_pos, j in enumerate(up):
                if i[1] == j[0] and i[2] == j[1]:
                    up[counter_pos:len(up)] = []

            for counter_pos, j in enumerate(left):
                if i[1] == j[0] and i[2] == j[1]:
                    left[counter_pos:len(left)] = []

            for counter_pos, j in enumerate(right):
                if i[1] == j[0] and i[2] == j[1]:
                    right[counter_pos:len(right)] = []

        for counter, i in enumerate(computer_pieces):
            for counter_pos, j in enumerate(down):
                if i[1] == j[0] and i[2] == j[1]:
                    down[counter_pos + 1:len(down)] = []

            for counter_pos, j in enumerate(up):
                if i[1] == j[0] and i[2] == j[1]:
                    up[counter_pos + 1:len(up)] = []

            for counter_pos, j in enumerate(left):
                if i[1] == j[0] and i[2] == j[1]:
                    left[counter_pos + 1:len(left)] = []

            for counter_pos, j in enumerate(right):
                if i[1] == j[0] and i[2] == j[1]:
                    right[counter_pos + 1:len(right)] = []

        for i in up:
            return_list.append(i)

        for i in down:
            return_list.append(i)

        for i in left:
            return_list.append(i)

        for i in right:
            return_list.append(i)

    elif piece_list[0] == chrs['b_rook']:
        up = []
        down = []
        left = []
        right = []
        for i in range(1, 9):
            if piece_list[1] + i <= 8:
                down.append([piece_list[1] + i, piece_list[2]])

            if piece_list[1] - i >= 1:
                up.append([piece_list[1] - i, piece_list[2]])

            if piece_list[2] + i <= 8:
                right.append([piece_list[1], piece_list[2] + i])

            if piece_list[2] - i >= 1:
                left.append([piece_list[1], piece_list[2] - i])

        for counter, i in enumerate(computer_pieces):
            for counter_pos, j in enumerate(down):
                if i[1] == j[0] and i[2] == j[1]:
                    down[counter_pos:len(down)] = []

            for counter_pos, j in enumerate(up):
                if i[1] == j[0] and i[2] == j[1]:
                    up[counter_pos:len(up)] = []

            for counter_pos, j in enumerate(left):
                if i[1] == j[0] and i[2] == j[1]:
                    left[counter_pos:len(left)] = []

            for counter_pos, j in enumerate(right):
                if i[1] == j[0] and i[2] == j[1]:
                    right[counter_pos:len(right)] = []

        for counter, i in enumerate(human_pieces):
            for counter_pos, j in enumerate(down):
                if i[1] == j[0] and i[2] == j[1]:
                    down[counter_pos + 1:len(down)] = []

            for counter_pos, j in enumerate(up):
                if i[1] == j[0] and i[2] == j[1]:
                    up[counter_pos + 1:len(up)] = []

            for counter_pos, j in enumerate(left):
                if i[1] == j[0] and i[2] == j[1]:
                    left[counter_pos + 1:len(left)] = []

            for counter_pos, j in enumerate(right):
                if i[1] == j[0] and i[2] == j[1]:
                    right[counter_pos + 1:len(right)] = []

        for i in up:
            return_list.append(i)

        for i in down:
            return_list.append(i)

        for i in left:
            return_list.append(i)

        for i in right:
            return_list.append(i)
    elif piece_list[0] == chrs['w_queen']:

        down_right = []
        down_left = []
        up_right = []
        up_left = []
        up = []
        down = []
        right = []
        left = []
        for i in range(1, 9):
            if piece_list[1] + i <= 8 and piece_list[2] + i <= 8:
                down_right.append([piece_list[1] + i, piece_list[2] + i])

            if piece_list[1] + i <= 8 and piece_list[2] - i >= 1:
                down_left.append([piece_list[1] + i, piece_list[2] - i])

            if piece_list[1] - i >= 1 and piece_list[2] + i <= 8:
                up_right.append([piece_list[1] - i, piece_list[2] + i])

            if piece_list[1] - i >= 1 and piece_list[2] - i >= 1:
                up_left.append([piece_list[1] - i, piece_list[2] - i])

            if piece_list[1] + i <= 8:
                down.append([piece_list[1] + i, piece_list[2]])

            if piece_list[1] - i >= 1:
                up.append([piece_list[1] - i, piece_list[2]])

            if piece_list[2] + i <= 8:
                right.append([piece_list[1], piece_list[2] + i])

            if piece_list[2] - i >= 1:
                left.append([piece_list[1], piece_list[2] - i])

        # reviews the lists from previous to avoid collision with own sort

        for counter, i in enumerate(human_pieces):
            for counter_pos, j in enumerate(down_right):
                if i[1] == j[0] and i[2] == j[1]:
                    down_right[counter_pos:len(down_right)] = []

            for counter_pos, j in enumerate(down_left):
                if i[1] == j[0] and i[2] == j[1]:
                    down_left[counter_pos:len(down_left)] = []

            for counter_pos, j in enumerate(up_right):
                if i[1] == j[0] and i[2] == j[1]:
                    up_right[counter_pos:len(up_right)] = []

            for counter_pos, j in enumerate(up_left):
                if i[1] == j[0] and i[2] == j[1]:
                    up_left[counter_pos:len(up_left)] = []

            for counter_pos, j in enumerate(down):
                if i[1] == j[0] and i[2] == j[1]:
                    down[counter_pos:len(down)] = []

            for counter_pos, j in enumerate(up):
                if i[1] == j[0] and i[2] == j[1]:
                    up[counter_pos:len(up)] = []

            for counter_pos, j in enumerate(left):
                if i[1] == j[0] and i[2] == j[1]:
                    left[counter_pos:len(left)] = []

            for counter_pos, j in enumerate(right):
                if i[1] == j[0] and i[2] == j[1]:
                    right[counter_pos:len(right)] = []

        # same as previous chunk but for the enemy's sort
        for counter, i in enumerate(computer_pieces):
            for counter_pos, j in enumerate(down_right):
                if i[1] == j[0] and i[2] == j[1]:
                    down_right[counter_pos + 1:len(down_right)] = []

            for counter_pos, j in enumerate(down_left):
                if i[1] == j[0] and i[2] == j[1]:
                    down_left[counter_pos + 1:len(down_left)] = []

            for counter_pos, j in enumerate(up_right):
                if i[1] == j[0] and i[2] == j[1]:
                    up_right[counter_pos + 1:len(up_right)] = []

            for counter_pos, j in enumerate(up_left):
                if i[1] == j[0] and i[2] == j[1]:
                    up_left[counter_pos + 1:len(up_left)] = []

            for counter_pos, j in enumerate(down):
                if i[1] == j[0] and i[2] == j[1]:
                    down[counter_pos + 1:len(down)] = []

            for counter_pos, j in enumerate(up):
                if i[1] == j[0] and i[2] == j[1]:
                    up[counter_pos + 1:len(up)] = []

            for counter_pos, j in enumerate(left):
                if i[1] == j[0] and i[2] == j[1]:
                    left[counter_pos + 1:len(left)] = []

            for counter_pos, j in enumerate(right):
                if i[1] == j[0] and i[2] == j[1]:
                    right[counter_pos + 1:len(right)] = []

        # adds to the return_list
        for i in up_left:
            return_list.append(i)
        for i in up_right:
            return_list.append(i)
        for i in down_left:
            return_list.append(i)
        for i in down_right:
            return_list.append(i)
        for i in up:
            return_list.append(i)

        for i in down:
            return_list.append(i)

        for i in left:
            return_list.append(i)

        for i in right:
            return_list.append(i)

    elif piece_list[0] == chrs['b_queen']:

        down_right = []
        down_left = []
        up_right = []
        up_left = []
        up = []
        down = []
        right = []
        left = []
        for i in range(1, 9):
            if piece_list[1] + i <= 8 and piece_list[2] + i <= 8:
                down_right.append([piece_list[1] + i, piece_list[2] + i])

            if piece_list[1] + i <= 8 and piece_list[2] - i >= 1:
                down_left.append([piece_list[1] + i, piece_list[2] - i])

            if piece_list[1] - i >= 1 and piece_list[2] + i <= 8:
                up_right.append([piece_list[1] - i, piece_list[2] + i])

            if piece_list[1] - i >= 1 and piece_list[2] - i >= 1:
                up_left.append([piece_list[1] - i, piece_list[2] - i])

            if piece_list[1] + i <= 8:
                down.append([piece_list[1] + i, piece_list[2]])

            if piece_list[1] - i >= 1:
                up.append([piece_list[1] - i, piece_list[2]])

            if piece_list[2] + i <= 8:
                right.append([piece_list[1], piece_list[2] + i])

            if piece_list[2] - i >= 1:
                left.append([piece_list[1], piece_list[2] - i])

        # reviews the lists from previous to avoid collision with own sort

        for counter, i in enumerate(computer_pieces):
            for counter_pos, j in enumerate(down_right):
                if i[1] == j[0] and i[2] == j[1]:
                    down_right[counter_pos:len(down_right)] = []

            for counter_pos, j in enumerate(down_left):
                if i[1] == j[0] and i[2] == j[1]:
                    down_left[counter_pos:len(down_left)] = []

            for counter_pos, j in enumerate(up_right):
                if i[1] == j[0] and i[2] == j[1]:
                    up_right[counter_pos:len(up_right)] = []

            for counter_pos, j in enumerate(up_left):
                if i[1] == j[0] and i[2] == j[1]:
                    up_left[counter_pos:len(up_left)] = []

            for counter_pos, j in enumerate(down):
                if i[1] == j[0] and i[2] == j[1]:
                    down[counter_pos:len(down)] = []

            for counter_pos, j in enumerate(up):
                if i[1] == j[0] and i[2] == j[1]:
                    up[counter_pos:len(up)] = []

            for counter_pos, j in enumerate(left):
                if i[1] == j[0] and i[2] == j[1]:
                    left[counter_pos:len(left)] = []

            for counter_pos, j in enumerate(right):
                if i[1] == j[0] and i[2] == j[1]:
                    right[counter_pos:len(right)] = []

        # same as previous chunk but for the enemy's sort
        for counter, i in enumerate(human_pieces):
            for counter_pos, j in enumerate(down_right):
                if i[1] == j[0] and i[2] == j[1]:
                    down_right[counter_pos + 1:len(down_right)] = []

            for counter_pos, j in enumerate(down_left):
                if i[1] == j[0] and i[2] == j[1]:
                    down_left[counter_pos + 1:len(down_left)] = []

            for counter_pos, j in enumerate(up_right):
                if i[1] == j[0] and i[2] == j[1]:
                    up_right[counter_pos + 1:len(up_right)] = []

            for counter_pos, j in enumerate(up_left):
                if i[1] == j[0] and i[2] == j[1]:
                    up_left[counter_pos + 1:len(up_left)] = []

            for counter_pos, j in enumerate(down):
                if i[1] == j[0] and i[2] == j[1]:
                    down[counter_pos + 1:len(down)] = []

            for counter_pos, j in enumerate(up):
                if i[1] == j[0] and i[2] == j[1]:
                    up[counter_pos + 1:len(up)] = []

            for counter_pos, j in enumerate(left):
                if i[1] == j[0] and i[2] == j[1]:
                    left[counter_pos + 1:len(left)] = []

            for counter_pos, j in enumerate(right):
                if i[1] == j[0] and i[2] == j[1]:
                    right[counter_pos + 1:len(right)] = []

        # adds to the return_list
        for i in up_left:
            return_list.append(i)
        for i in up_right:
            return_list.append(i)
        for i in down_left:
            return_list.append(i)
        for i in down_right:
            return_list.append(i)
        for i in up:
            return_list.append(i)

        for i in down:
            return_list.append(i)

        for i in left:
            return_list.append(i)

        for i in right:
            return_list.append(i)

    elif piece_list[0] == chrs["w_knight"]:
        position_list = [[piece_list[1] - 2, piece_list[2] + 1], [piece_list[1] + 2, piece_list[2] - 1],
                         [piece_list[1] - 2, piece_list[2] - 1], [piece_list[1] + 2, piece_list[2] + 1],
                         [piece_list[1] - 1, piece_list[2] - 2], [piece_list[1] - 1, piece_list[2] + 2],
                         [piece_list[1] + 1, piece_list[2] - 2], [piece_list[1] + 1, piece_list[2] + 2]]
        candidates = []
        refined_candidates = []

        for i in position_list:
            if 8 >= i[0] >= 1 and 8 >= i[1] >= 1:
                candidates.append(i)

        for j in candidates:
            approved = True
            for i in human_pieces:
                if i[1] == j[0] and i[2] == j[1]:
                    approved = False

            if approved:
                refined_candidates.append(j)

        return_list = refined_candidates

    elif piece_list[0] == chrs["b_knight"]:
        position_list = [[piece_list[1] - 2, piece_list[2] + 1], [piece_list[1] + 2, piece_list[2] - 1],
                         [piece_list[1] - 2, piece_list[2] - 1], [piece_list[1] + 2, piece_list[2] + 1],
                         [piece_list[1] - 1, piece_list[2] - 2], [piece_list[1] - 1, piece_list[2] + 2],
                         [piece_list[1] + 1, piece_list[2] - 2], [piece_list[1] + 1, piece_list[2] + 2]]
        candidates = []
        refined_candidates = []

        for i in position_list:
            if 8 >= i[0] >= 1 and 8 >= i[1] >= 1:
                candidates.append(i)

        for j in candidates:
            approved = True
            for i in computer_pieces:
                if i[1] == j[0] and i[2] == j[1]:
                    approved = False

            if approved:
                refined_candidates.append(j)

        return_list = refined_candidates

    elif piece_list[0] == chrs['w_king']:
        position_list = [[piece_list[1] - 1, piece_list[2]], [piece_list[1] - 1, piece_list[2] + 1],
                     [piece_list[1], piece_list[2] + 1], [piece_list[1] + 1, piece_list[2] + 1],
                     [piece_list[1] + 1, piece_list[2]], [piece_list[1] + 1, piece_list[2] - 1],
                     [piece_list[1], piece_list[2] - 1], [piece_list[1] - 1, piece_list[2] - 1]]
        candidates = []
        refined_candidates = []


        for i in position_list:
            if 8 >= i[0] >= 1 and 8 >= i[1] >= 1:
                candidates.append(i)

        for j in candidates:
            approved = True
            for i in human_pieces:
                if i[1] == j[0] and i[2] == j[1]:
                    approved = False

            if approved:
                refined_candidates.append(j)

        return_list = refined_candidates

    elif piece_list[0] == chrs['b_king']:
        position_list = [[piece_list[1] - 1, piece_list[2]], [piece_list[1] - 1, piece_list[2] + 1],
                     [piece_list[1], piece_list[2] + 1], [piece_list[1] + 1, piece_list[2] + 1],
                     [piece_list[1] + 1, piece_list[2]], [piece_list[1] + 1, piece_list[2] - 1],
                     [piece_list[1], piece_list[2] - 1], [piece_list[1] - 1, piece_list[2] - 1]]
        candidates = []
        refined_candidates = []


        for i in position_list:
            if 8 >= i[0] >= 1 and 8 >= i[1] >= 1:
                candidates.append(i)

        for j in candidates:
            approved = True
            for i in computer_pieces:
                if i[1] == j[0] and i[2] == j[1]:
                    approved = False

            if approved:
                refined_candidates.append(j)

        return_list = refined_candidates

    return return_list

def minimax(depth, maximizing):
    global computer_pieces
    global initial_pos
    global move_pos
    global copy
    global chrs
    global best_score
    global best_pos
    global best_piece
    global score
    global counter
    global total_turns
    global worst_score
    global worster_score
    global human_copy
    global human_pieces
    global worst_initial_pos
    global worst_move_pos
    global worst_piece
    global worst_pos
    global counter
    global best_pos
    global alpha
    global beta
    global actual_best_pos

    counter = counter + 1

    if depth == 0:
        human_pieces = [x[:] for x in human_copy]
        computer_pieces = [x[:] for x in copy]


    if maximizing:
        for i in computer_pieces:
            for j in return_possible_moves(i):

                if depth == 3:
                    computer_pieces = [x[:] for x in copy]
                    initial_pos = i
                    move_pos = [j[0], j[1]]

                computer_updater([i[1], i[2]], [j[0], j[1]])

                score = -value([j[0], j[1]])

                #try:

                if (score + value(worst_pos)) * depth > best_score and move_pos in return_possible_moves(initial_pos):
                    best_score = (score + value(worst_pos))
                    best_piece = initial_pos
                    best_pos = move_pos
                    actual_best_pos = [j[0], j[1]]

                alpha = best_score

                if depth > 0:
                    minimax(depth - 1, False)
                else:
                    computer_pieces = [x[:] for x in copy]

                if beta >= alpha:
                    break

                #except Exception as e:
                    #pass

        depth = 3


    else:
        for i in human_pieces:
            for j in return_possible_moves(i):

                worst_initial_pos = i
                worst_move_pos = [j[0], j[1]]
                human_updater([i[1], i[2]], [j[0], j[1]])

                worst_score = -value([j[0], j[1]])

                if (worst_score + value(actual_best_pos)) * depth < worster_score:
                    worst_pos = worst_move_pos
                    worster_score = (worst_score + value(actual_best_pos))

                beta = worster_score

                minimax(depth - 1, True)

                if beta >= alpha:
                    break

        depth = 3


pg.init()

BLUE = pg.Color('blue')
WHITE = pg.Color('white')

screen = pg.display.set_mode((800, 600))
clock = pg.time.Clock()

colors = itertools.cycle((WHITE, BLUE))
tile_size = 60
width, height = 8*tile_size, 8*tile_size
background = pg.Surface((width, height))

for y in range(0, height, tile_size):
    for x in range(0, width, tile_size):
        rect = (x, y, tile_size, tile_size)
        pg.draw.rect(background, next(colors), rect)
    next(colors)

def get_mouse_box(mouse_pos):
    return [math.ceil((mouse_pos[0] - 100) / tile_size), math.ceil((mouse_pos[1] - 100) / tile_size)]

game_exit = False
while not game_exit:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            game_exit = True

    screen.fill((60, 70, 90))
    screen.blit(background, (100, 100))

    for i in human_pieces:
        for j in chrs:
            if chrs[j] == i[0]:
                screen.blit(image_chrs[j], (98 + ((i[2] - 1) * tile_size), 98 + ((i[1] - 1) * tile_size)))

    for i in computer_pieces:
        for j in chrs:
            if chrs[j] == i[0]:
                screen.blit(image_chrs[j], (98 + ((i[2] - 1) * tile_size), 98 + ((i[1] - 1) * tile_size)))

    if pg.mouse.get_pressed()[0]:
        if len(from_pos) < 2:
            from_pos = get_mouse_box(pg.mouse.get_pos())
        else:
            to_pos = get_mouse_box(pg.mouse.get_pos())
        time.sleep(1)
    print(from_pos, to_pos)
    if len(from_pos) > 1 and len(to_pos) > 1:
        user_input_updater(from_pos, to_pos)
        copy = [x[:] for x in computer_pieces]
        human_copy = [x[:] for x in human_pieces]
        best_pos = [0, 0]
        worst_score = 2000
        best_piece = []
        score = -2000
        best_score = -2000
        alpha = -2000
        beta = 2000
        worster_score = 2000
        counter = 0
        initial_pos = []
        worst_initial_pos = []
        move_pos = []
        worst_pos = [0, 0]
        worst_piece = []
        actual_best_pos = [0, 0]
        counter = 0
        from_pos = []
        to_pos = []
        minimax(3, True)

        print(best_piece[1], best_piece[2], best_pos)
        print(best_score, worster_score)
        time.sleep(2)
        computer_pieces = [x[:] for x in copy]
        human_pieces = [x[:] for x in human_copy]
        computer_updater([best_piece[1], best_piece[2]], best_pos)
        delete_piece([best_piece[0], best_pos[0], best_pos[1]])
    pg.display.flip()
    clock.tick(30)
    game_exit = False

pg.quit()




