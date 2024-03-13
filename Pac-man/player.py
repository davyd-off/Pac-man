from sdl2 import *
from sdl2.ext import *

player_images = []
for i in range(1, 5):
    player_images.append(load_image(f'Source/Images/pacman_{i}.png'))
player_images.append(load_image(f'Source/Images/pacman_live.png'))

def draw_player(renderer, count, direction, player_x, player_y):
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

def check_target(level, WIDTH, HEIGHT, score, player_x, center_x, center_y, power, power_cnt, dead_ghosts):
    """"
    Пожирание точек.
    """
    num1 = (HEIGHT - 50) // 32
    num2 = WIDTH // 30
    if 0 < player_x < 870:
        if level[center_y//num1][center_x//num2] == 1:
            level[center_y//num1][center_x//num2] = 0
            score += 10
        if level[center_y//num1][center_x//num2] == 2:
            level[center_y//num1][center_x//num2] = 0
            score += 50
            power = True
            power_cnt = 0
            dead_ghosts = [False, False, False, False]
    return score, power, power_cnt, dead_ghosts

def draw_counter(renderer, scor, power, live):
    """
    Отрисовка счетчика.
    """
    text_color = Color(255, 255, 255)
    font = FontTTF("./Source/Font/better-vcr-5.4.ttf", "15px", text_color)

    txt = f'Score: {scor}'
    txt_rendered = font.render_text(txt)
    tx_text = Texture(renderer, txt_rendered)
    renderer.copy(tx_text, dstrect=(10, 920))
    if power:
        tx_power = Texture(renderer, load_image(b"Source/Images/power.png"))
        renderer.copy(tx_power, dstrect=(140, 915))
    tx_live = Texture(renderer, player_images[4])
    for i in range(live):
        renderer.copy(tx_live, dstrect=(650 + i * 40, 915))
