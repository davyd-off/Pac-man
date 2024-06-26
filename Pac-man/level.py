from sdl2 import *
from sdl2.ext import *
from board_1 import board1
from board_2 import board2
from board_3 import board3
import copy


def selected_level(select_level):
    """
    Загрузка карты.
    """
    if select_level[0]:
        map = copy.deepcopy(board1)
    elif select_level[1]:
        map = copy.deepcopy(board2)
    else:
        map = copy.deepcopy(board3)
    return map

def draw_board(renderer, WIDTH, HEIGHT, flick, level, tx_1, tx_2):
    """
    Рисование карты.
    """
    num1 = ((HEIGHT - 50) // 32)
    num2 = (WIDTH // 30)
    color_1 = Color(0, 255, 0)
    color_2 = Color(255, 255, 255)

    for i in range(len(level)):
        for j in range(len(level[i])):
            if level[i][j] == 1:
                renderer.blit(tx_1, dstrect=(j * num2 + (num2 // 2), i * num1 + (num1 // 2)), angle=0, flip=0)
            if level[i][j] == 2 and not flick:
                renderer.blit(tx_2, dstrect=(j * num2 + (num2 // 2), i * num1 + (num1 // 2)), angle=0, flip=0)                     
            if level[i][j] == 3:
                renderer.draw_line(((j * num2 + (num2 // 2)), (i * num1),
                                (j * num2 + (num2 // 2)), (i * num1 + num1)), color=color_1)
            if level[i][j] == 4:
                renderer.draw_line(((j * num2), (i * num1 + (num1 // 2)),
                                    (j * num2 + num2), (i * num1 + (num1 // 2))), color=color_1)
            if level[i][j] == 5:
                renderer.draw_line(((j * num2), (i * num1 + (num1 // 2)),
                                    (j * num2 + (num2 // 2)), (i * num1 + num1)), color=color_1)
            if level[i][j] == 6:
                renderer.draw_line(((j * num2 + num2), (i * num1 + (num1 // 2)),
                                 (j * num2 + (num2 // 2)), (i * num1 + num1)), color=color_1)
            if level[i][j] == 7:
                renderer.draw_line(((j * num2 + (num2 // 2)), (i * num1),
                                     (j * num2 + num2), (i * num1 + (num1 // 2))), color=color_1)
            if level[i][j] == 8:
                renderer.draw_line(((j * num2), (i * num1 + (num1 // 2)),
                                     (j * num2 + (num2 // 2)), (i * num1)), color=color_1)
            if level[i][j] == 9:
                renderer.draw_line(((j * num2), (i * num1 + (num1 // 2)),
                                 (j * num2 + num2), (i * num1 + (num1 // 2))), color=color_2)