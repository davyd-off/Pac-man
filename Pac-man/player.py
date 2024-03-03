from sdl2 import *
from sdl2.ext import *

player_images = []
for i in range(1, 5):
    player_images.append(load_image(f'Source/Images/pacman_{i}.png'))

def draw(renderer, count, direction, player_x, player_y):
    """
    Рисовалка пакмана.
    0 - право, 1 - лево, 2 - вверх, 3 - вниз
    """
    if direction == 0:
        tx_1 = Texture(renderer, player_images[count // 5])
        renderer.copy(tx_1, dstrect=(player_x, player_y))
    elif direction == 1:
        tx_2 = Texture(renderer, player_images[count // 5])
        renderer.copy(tx_2, dstrect=(player_x, player_y), angle=180)
    elif direction == 2:
        tx_3 = Texture(renderer, player_images[count // 5])
        renderer.copy(tx_3, dstrect=(player_x, player_y), angle=270)
    elif direction == 3:
        tx_4 = Texture(renderer, player_images[count // 5])
        renderer.copy(tx_4, dstrect=(player_x, player_y), angle=90)

def check_position(centerx, centery, direction, WIDTH, HEIGHT, level):
    """
    Проверка на столкновение со стенкой. То есть не даёт сквозь псевдотекстуры проходить.
    """
    turns = [False, False, False, False]
    num1 = (HEIGHT - 50) // 32
    num2 = (WIDTH // 30)
    num3 = 15
    if centerx // 30 < 29:
        if direction == 0:
            if level[centery // num1][(centerx - num3) // num2] < 3:
                turns[1] = True
        if direction == 1:
            if level[centery // num1][(centerx + num3) // num2] < 3:
                turns[0] = True
        if direction == 2:
            if level[(centery + num3) // num1][centerx // num2] < 3:
                turns[3] = True
        if direction == 3:
            if level[(centery - num3) // num1][centerx // num2] < 3:
                turns[2] = True

        if direction == 2 or direction == 3:
            if 12 <= centerx % num2 <= 18:
                if level[(centery + num3) // num1][centerx // num2] < 3:
                    turns[3] = True
                if level[(centery - num3) // num1][centerx // num2] < 3:
                    turns[2] = True
            if 12 <= centery % num1 <= 18:
                if level[centery // num1][(centerx - num2) // num2] < 3:
                    turns[1] = True
                if level[centery // num1][(centerx + num2) // num2] < 3:
                    turns[0] = True
        if direction == 0 or direction == 1:
            if 12 <= centerx % num2 <= 18:
                if level[(centery + num1) // num1][centerx // num2] < 3:
                    turns[3] = True
                if level[(centery - num1) // num1][centerx // num2] < 3:
                    turns[2] = True
            if 12 <= centery % num1 <= 18:
                if level[centery // num1][(centerx - num3) // num2] < 3:
                    turns[1] = True
                if level[centery // num1][(centerx + num3) // num2] < 3:
                    turns[0] = True
    else:
        turns[0] = True
        turns[1] = True

    return turns

def move(play_x, play_y, direction, turns_allowed, player_speed):
    """
    Движение пакмана.
    """
    if direction == 0 and turns_allowed[0]:
        play_x += player_speed
    elif direction == 1 and turns_allowed[1]:
        play_x -= player_speed
    if direction == 2 and turns_allowed[2]:
        play_y -= player_speed
    elif direction == 3 and turns_allowed[3]:
        play_y += player_speed
    return play_x, play_y