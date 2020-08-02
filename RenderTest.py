import itertools
import pygame as pg
import time

example = [['♖', 1, 1], ['♘', 1, 2], ['♗', 1, 3], ['♕', 1, 4], ['♔', 1, 5], ['♗', 1, 6], ['♘', 1, 7], ['♖', 1, 8], ['♙', 2, 1], ['♙', 2, 2], ['♙', 2, 3], ['♙', 2, 4], ['♙', 2, 5], ['♙', 2, 6], ['♙', 2, 7], ['♙', 2, 8]]

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
    return_list = []
    for i in range(1, 9):
        if i - 0.99 <= (mouse_pos[0] - 100) / tile_size <= i:
            return_list.append(i)

        if i - 0.99 <= (mouse_pos[1] - 100) / tile_size <= i:
            return_list.append(i)
    return return_list

game_exit = False
while not game_exit:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            game_exit = True

    screen.fill((60, 70, 90))
    screen.blit(background, (100, 100))

    if pg.mouse.get_pressed()[0]:
        print(get_mouse_box(pg.mouse.get_pos()))
        time.sleep(1)

    for i in example:
        for j in chrs:
            if chrs[j] == i[0]:
                screen.blit(image_chrs[j], (98 + ((i[2] - 1) * tile_size), 98 + ((i[1] - 1) * tile_size)))

    pg.display.flip()
    clock.tick(30)
    game_exit = False

pg.quit()
