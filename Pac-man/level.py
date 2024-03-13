from sdl2 import *
from sdl2.ext import *
from board_1 import boards

level = boards

def draw_board(renderer, WIDTH, HEIGHT, flick):
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
                tx_1 = Texture(renderer, load_image(b"Source/Images/dot.png"))
                renderer.copy(tx_1, dstrect=(j * num2 + (num2 // 2), i * num1 + (num1 // 2)), angle=0, flip=0)
            if level[i][j] == 2 and not flick:
                tx_2 = Texture(renderer, load_image(b"Source/Images/power dot.png"))
                renderer.copy(tx_2, dstrect=(j * num2 + (num2 // 2), i * num1 + (num1 // 2)), angle=0, flip=0)                     
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