from sdl2 import *
from sdl2.ext import *
import sdl2.sdlmixer as sdlmixer


text_color = Color(255, 255, 255)
text_over_color = Color(255, 0, 0)
text_win_color = Color(244, 164, 96)

font_manager_scor = FontManager(font_path="./Source/Font/better-vcr-5.4.ttf", size=15, color=text_color)
font_manager_over = FontManager(font_path="./Source/Font/better-vcr-5.4.ttf", size=50, color=text_over_color)
font_manager_win = FontManager(font_path="./Source/Font/better-vcr-5.4.ttf", size=50, color=text_win_color)

def draw_player(renderer, count, direction, player_x, player_y, player_images):
    """
    Рисовалка пакмана.
    0 - право, 1 - лево, 2 - вверх, 3 - вниз
    """
    if direction == 0:
        tx_1 = player_images[count // 5]
        renderer.blit(tx_1, dstrect=(player_x, player_y))
    elif direction == 1:
        tx_2 = player_images[count // 5]
        renderer.blit(tx_2, dstrect=(player_x, player_y), angle=180)
    elif direction == 2:
        tx_3 = player_images[count // 5]
        renderer.blit(tx_3, dstrect=(player_x, player_y), angle=270)
    elif direction == 3:
        tx_4 = player_images[count // 5]
        renderer.blit(tx_4, dstrect=(player_x, player_y), angle=90)

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

def check_target(level, WIDTH, HEIGHT, score, player_x, center_x, center_y, power, power_cnt, dead_ghosts, eat_sound):
    """"
    Пожирание точек и призраков.
    """
    num1 = (HEIGHT - 50) // 32
    num2 = WIDTH // 30
    if 0 < player_x < 870:
        if level[center_y//num1][center_x//num2] == 1:
            level[center_y//num1][center_x//num2] = 0
            score += 10
            sdlmixer.Mix_PlayChannel(2, eat_sound, 0)
        if level[center_y//num1][center_x//num2] == 2:
            level[center_y//num1][center_x//num2] = 0
            score += 50
            sdlmixer.Mix_PlayChannel(2, eat_sound, 0)
            power = True
            power_cnt = 0
            dead_ghosts = [False, False, False, False, False, False, False]
    return score, power, power_cnt, dead_ghosts

def draw_counter(renderer, scor, power, live, game_over, game_win, player_images, factory):
    """
    Отрисовка счетчика, надписи проигрыша/выигрыша.
    """
    tx_text = factory.from_text(f'Очки: {scor}', fontmanager=font_manager_scor)
    renderer.blit(tx_text, dstrect=(10, 920))
    if power:
        tx_power = factory.from_image(f'Source/Images/power.png')
        renderer.blit(tx_power, dstrect=(140, 915))
    tx_live = player_images[4]
    for i in range(live):
        renderer.blit(tx_live, dstrect=(650 + i * 40, 915))
    if game_over:
        tx_text_over = factory.from_text(f'Вы проиграли :(', fontmanager=font_manager_over)
        renderer.blit(tx_text_over, dstrect=(200, 425))
    if game_win:
        tx_text_win = factory.from_text(f'Вы выиграли!', fontmanager=font_manager_win)
        renderer.blit(tx_text_win, dstrect=(200, 425))

def get_targets_4(blink_x, blink_y, ink_x, ink_y, pink_x, pink_y, clyd_x, clyd_y,
                  player_x, player_y, powerup, dead_ghost, blinky, inky, pinky, clyde):
    """
    Изменение координат призраков в зависимости от: преследования ими пакмана, убегания от пакмана, перерождения.
    """
    if player_x < 450:
        runaway_x = 900
    else:
        runaway_x = 0
    if player_y < 450:
        runaway_y = 900
    else:
        runaway_y = 0
    return_target = (380, 400)
    if powerup:
        if not blinky.dead and not dead_ghost[0]:
            blink_target = (runaway_x, runaway_y)
        elif not blinky.dead and dead_ghost[0]:
            if 340 < blink_x < 560 and 340 < blink_y < 500:
                blink_target = (400, 100)
            else:
                blink_target = (player_x, player_y)
        else:
            blink_target = return_target
        if not inky.dead and not dead_ghost[1]:
            ink_target = (runaway_x, player_y)
        elif not inky.dead and dead_ghost[1]:
            if 340 < ink_x < 560 and 340 < ink_y < 500:
                ink_target = (400, 100)
            else:
                ink_target = (player_x, player_y)
        else:
            ink_target = return_target
        if not pinky.dead:
            pink_target = (player_x, runaway_y)
        elif not pinky.dead and dead_ghost[2]:
            if 340 < pink_x < 560 and 340 < pink_y < 500:
                pink_target = (400, 100)
            else:
                pink_target = (player_x, player_y)
        else:
            pink_target = return_target
        if not clyde.dead and not dead_ghost[3]:
            clyd_target = (450, 450)
        elif not clyde.dead and dead_ghost[3]:
            if 340 < clyd_x < 560 and 340 < clyd_y < 500:
                clyd_target = (400, 100)
            else:
                clyd_target = (player_x, player_y)
        else:
            clyd_target = return_target
    else:
        if not blinky.dead:
            if 340 < blink_x < 560 and 340 < blink_y < 500:
                blink_target = (400, 100)
            else:
                blink_target = (player_x, player_y)
        else:
            blink_target = return_target
        if not inky.dead:
            if 340 < ink_x < 560 and 340 < ink_y < 500:
                ink_target = (400, 100)
            else:
                ink_target = (player_x, player_y)
        else:
            ink_target = return_target
        if not pinky.dead:
            if 340 < pink_x < 560 and 340 < pink_y < 500:
                pink_target = (400, 100)
            else:
                pink_target = (player_x, player_y)
        else:
            pink_target = return_target
        if not clyde.dead:
            if 340 < clyd_x < 560 and 340 < clyd_y < 500:
                clyd_target = (400, 100)
            else:
                clyd_target = (player_x, player_y)
        else:
            clyd_target = return_target
    return [blink_target, ink_target, pink_target, clyd_target]

def get_targets_5(blink_x, blink_y, ink_x, ink_y, pink_x, pink_y, clyd_x, clyd_y,
                ghst1_x, ghst1_y, player_x, player_y, powerup, dead_ghost, blinky, inky, pinky, clyde, ghost1):
    """
    Изменение координат призраков в зависимости от: преследования ими пакмана, убегания от пакмана, перерождения.
    """
    if player_x < 450:
        runaway_x = 900
    else:
        runaway_x = 0
    if player_y < 450:
        runaway_y = 900
    else:
        runaway_y = 0
    return_target = (380, 400)
    if powerup:
        if not blinky.dead and not dead_ghost[0]:
            blink_target = (runaway_x, runaway_y)
        elif not blinky.dead and dead_ghost[0]:
            if 340 < blink_x < 560 and 340 < blink_y < 500:
                blink_target = (400, 100)
            else:
                blink_target = (player_x, player_y)
        else:
            blink_target = return_target
        if not inky.dead and not dead_ghost[1]:
            ink_target = (runaway_x, player_y)
        elif not inky.dead and dead_ghost[1]:
            if 340 < ink_x < 560 and 340 < ink_y < 500:
                ink_target = (400, 100)
            else:
                ink_target = (player_x, player_y)
        else:
            ink_target = return_target
        if not pinky.dead:
            pink_target = (player_x, runaway_y)
        elif not pinky.dead and dead_ghost[2]:
            if 340 < pink_x < 560 and 340 < pink_y < 500:
                pink_target = (400, 100)
            else:
                pink_target = (player_x, player_y)
        else:
            pink_target = return_target
        if not clyde.dead and not dead_ghost[3]:
            clyd_target = (450, 450)
        elif not clyde.dead and dead_ghost[3]:
            if 340 < clyd_x < 560 and 340 < clyd_y < 500:
                clyd_target = (400, 100)
            else:
                clyd_target = (player_x, player_y)
        else:
            clyd_target = return_target
        if not ghost1.dead and not dead_ghost[4]:
            ghst1_target = (450, 450)
        elif not ghost1.dead and dead_ghost[4]:
            if 340 < ghst1_x < 560 and 340 < ghst1_y < 500:
                ghst1_target = (400, 100)
            else:
                ghst1_target = (player_x, player_y)
        else:
            ghst1_target = return_target
    else:
        if not blinky.dead:
            if 340 < blink_x < 560 and 340 < blink_y < 500:
                blink_target = (400, 100)
            else:
                blink_target = (player_x, player_y)
        else:
            blink_target = return_target
        if not inky.dead:
            if 340 < ink_x < 560 and 340 < ink_y < 500:
                ink_target = (400, 100)
            else:
                ink_target = (player_x, player_y)
        else:
            ink_target = return_target
        if not pinky.dead:
            if 340 < pink_x < 560 and 340 < pink_y < 500:
                pink_target = (400, 100)
            else:
                pink_target = (player_x, player_y)
        else:
            pink_target = return_target
        if not clyde.dead:
            if 340 < clyd_x < 560 and 340 < clyd_y < 500:
                clyd_target = (400, 100)
            else:
                clyd_target = (player_x, player_y)
        else:
            clyd_target = return_target
        if not ghost1.dead:
            if 340 < ghst1_x < 560 and 340 < ghst1_y < 500:
                ghst1_target = (400, 100)
            else:
                ghst1_target = (player_x, player_y)
        else:
            ghst1_target = return_target
    return [blink_target, ink_target, pink_target, clyd_target, ghst1_target]

def get_targets_6(blink_x, blink_y, ink_x, ink_y, pink_x, pink_y, clyd_x, clyd_y,
                ghst1_x, ghst1_y, ghst2_x, ghst2_y,
                  player_x, player_y, powerup, dead_ghost, blinky, inky, pinky, clyde, ghost1, ghost2):
    """
    Изменение координат призраков в зависимости от: преследования ими пакмана, убегания от пакмана, перерождения.
    """
    if player_x < 450:
        runaway_x = 900
    else:
        runaway_x = 0
    if player_y < 450:
        runaway_y = 900
    else:
        runaway_y = 0
    return_target = (380, 400)
    if powerup:
        if not blinky.dead and not dead_ghost[0]:
            blink_target = (runaway_x, runaway_y)
        elif not blinky.dead and dead_ghost[0]:
            if 340 < blink_x < 560 and 340 < blink_y < 500:
                blink_target = (400, 100)
            else:
                blink_target = (player_x, player_y)
        else:
            blink_target = return_target
        if not inky.dead and not dead_ghost[1]:
            ink_target = (runaway_x, player_y)
        elif not inky.dead and dead_ghost[1]:
            if 340 < ink_x < 560 and 340 < ink_y < 500:
                ink_target = (400, 100)
            else:
                ink_target = (player_x, player_y)
        else:
            ink_target = return_target
        if not pinky.dead:
            pink_target = (player_x, runaway_y)
        elif not pinky.dead and dead_ghost[2]:
            if 340 < pink_x < 560 and 340 < pink_y < 500:
                pink_target = (400, 100)
            else:
                pink_target = (player_x, player_y)
        else:
            pink_target = return_target
        if not clyde.dead and not dead_ghost[3]:
            clyd_target = (450, 450)
        elif not clyde.dead and dead_ghost[3]:
            if 340 < clyd_x < 560 and 340 < clyd_y < 500:
                clyd_target = (400, 100)
            else:
                clyd_target = (player_x, player_y)
        else:
            clyd_target = return_target
        if not ghost1.dead and not dead_ghost[4]:
            ghst1_target = (450, 450)
        elif not ghost1.dead and dead_ghost[4]:
            if 340 < ghst1_x < 560 and 340 < ghst1_y < 500:
                ghst1_target = (400, 100)
            else:
                ghst1_target = (player_x, player_y)
        else:
            ghst1_target = return_target
        if not ghost2.dead and not dead_ghost[5]:
            ghst2_target = (450, 450)
        elif not ghost2.dead and dead_ghost[5]:
            if 340 < ghst2_x < 560 and 340 < ghst2_y < 500:
                ghst2_target = (400, 100)
            else:
                ghst2_target = (player_x, player_y)
        else:
            ghst2_target = return_target        
    else:
        if not blinky.dead:
            if 340 < blink_x < 560 and 340 < blink_y < 500:
                blink_target = (400, 100)
            else:
                blink_target = (player_x, player_y)
        else:
            blink_target = return_target
        if not inky.dead:
            if 340 < ink_x < 560 and 340 < ink_y < 500:
                ink_target = (400, 100)
            else:
                ink_target = (player_x, player_y)
        else:
            ink_target = return_target
        if not pinky.dead:
            if 340 < pink_x < 560 and 340 < pink_y < 500:
                pink_target = (400, 100)
            else:
                pink_target = (player_x, player_y)
        else:
            pink_target = return_target
        if not clyde.dead:
            if 340 < clyd_x < 560 and 340 < clyd_y < 500:
                clyd_target = (400, 100)
            else:
                clyd_target = (player_x, player_y)
        else:
            clyd_target = return_target
        if not ghost1.dead:
            if 340 < ghst1_x < 560 and 340 < ghst1_y < 500:
                ghst1_target = (400, 100)
            else:
                ghst1_target = (player_x, player_y)
        else:
            ghst1_target = return_target
        if not ghost2.dead:
            if 340 < ghst2_x < 560 and 340 < ghst2_y < 500:
                ghst2_target = (400, 100)
            else:
                ghst2_target = (player_x, player_y)
        else:
            ghst2_target = return_target
    return [blink_target, ink_target, pink_target, clyd_target, ghst1_target, ghst2_target]

def get_targets_7(blink_x, blink_y, ink_x, ink_y, pink_x, pink_y, clyd_x, clyd_y,
                ghst1_x, ghst1_y, ghst2_x, ghst2_y, ghst3_x, ghst3_y,
                  player_x, player_y, powerup, dead_ghost, blinky, inky, pinky, clyde, ghost1, ghost2, ghost3):
    """
    Изменение координат призраков в зависимости от: преследования ими пакмана, убегания от пакмана, перерождения.
    """
    if player_x < 450:
        runaway_x = 900
    else:
        runaway_x = 0
    if player_y < 450:
        runaway_y = 900
    else:
        runaway_y = 0
    return_target = (380, 400)
    if powerup:
        if not blinky.dead and not dead_ghost[0]:
            blink_target = (runaway_x, runaway_y)
        elif not blinky.dead and dead_ghost[0]:
            if 340 < blink_x < 560 and 340 < blink_y < 500:
                blink_target = (400, 100)
            else:
                blink_target = (player_x, player_y)
        else:
            blink_target = return_target
        if not inky.dead and not dead_ghost[1]:
            ink_target = (runaway_x, player_y)
        elif not inky.dead and dead_ghost[1]:
            if 340 < ink_x < 560 and 340 < ink_y < 500:
                ink_target = (400, 100)
            else:
                ink_target = (player_x, player_y)
        else:
            ink_target = return_target
        if not pinky.dead:
            pink_target = (player_x, runaway_y)
        elif not pinky.dead and dead_ghost[2]:
            if 340 < pink_x < 560 and 340 < pink_y < 500:
                pink_target = (400, 100)
            else:
                pink_target = (player_x, player_y)
        else:
            pink_target = return_target
        if not clyde.dead and not dead_ghost[3]:
            clyd_target = (450, 450)
        elif not clyde.dead and dead_ghost[3]:
            if 340 < clyd_x < 560 and 340 < clyd_y < 500:
                clyd_target = (400, 100)
            else:
                clyd_target = (player_x, player_y)
        else:
            clyd_target = return_target
        if not ghost1.dead and not dead_ghost[4]:
            ghst1_target = (450, 450)
        elif not ghost1.dead and dead_ghost[4]:
            if 340 < ghst1_x < 560 and 340 < ghst1_y < 500:
                ghst1_target = (400, 100)
            else:
                ghst1_target = (player_x, player_y)
        else:
            ghst1_target = return_target
        if not ghost2.dead and not dead_ghost[5]:
            ghst2_target = (450, 450)
        elif not ghost2.dead and dead_ghost[5]:
            if 340 < ghst2_x < 560 and 340 < ghst2_y < 500:
                ghst2_target = (400, 100)
            else:
                ghst2_target = (player_x, player_y)
        else:
            ghst2_target = return_target
        if not ghost3.dead and not dead_ghost[6]:
            ghst3_target = (450, 450)
        elif not ghost3.dead and dead_ghost[6]:
            if 340 < ghst3_x < 560 and 340 < ghst3_y < 500:
                ghst3_target = (400, 100)
            else:
                ghst3_target = (player_x, player_y)
        else:
            ghst3_target = return_target
        
    else:
        if not blinky.dead:
            if 340 < blink_x < 560 and 340 < blink_y < 500:
                blink_target = (400, 100)
            else:
                blink_target = (player_x, player_y)
        else:
            blink_target = return_target
        if not inky.dead:
            if 340 < ink_x < 560 and 340 < ink_y < 500:
                ink_target = (400, 100)
            else:
                ink_target = (player_x, player_y)
        else:
            ink_target = return_target
        if not pinky.dead:
            if 340 < pink_x < 560 and 340 < pink_y < 500:
                pink_target = (400, 100)
            else:
                pink_target = (player_x, player_y)
        else:
            pink_target = return_target
        if not clyde.dead:
            if 340 < clyd_x < 560 and 340 < clyd_y < 500:
                clyd_target = (400, 100)
            else:
                clyd_target = (player_x, player_y)
        else:
            clyd_target = return_target
        if not ghost1.dead:
            if 340 < ghst1_x < 560 and 340 < ghst1_y < 500:
                ghst1_target = (400, 100)
            else:
                ghst1_target = (player_x, player_y)
        else:
            ghst1_target = return_target
        if not ghost2.dead:
            if 340 < ghst2_x < 560 and 340 < ghst2_y < 500:
                ghst2_target = (400, 100)
            else:
                ghst2_target = (player_x, player_y)
        else:
            ghst2_target = return_target
        if not ghost3.dead:
            if 340 < ghst3_x < 560 and 340 < ghst3_y < 500:
                ghst3_target = (400, 100)
            else:
                ghst3_target = (player_x, player_y)
        else:
            ghst3_target = return_target
    return [blink_target, ink_target, pink_target, clyd_target, ghst1_target, ghst2_target, ghst3_target]