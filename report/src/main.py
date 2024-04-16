import sys
from sdl2 import *
from sdl2.ext import *
import sdl2.sdlmixer as sdlmixer
from button import ImageButton
import player
import level as lvl
from ghost import Ghost


def main():
    init()

    # Создание аудиоканала
    sdlmixer.Mix_OpenAudio(44100, sdlmixer.MIX_DEFAULT_FORMAT, 2, 1024)
    music_theme = sdlmixer.Mix_LoadWAV(b"Source/Sound/start.wav")
    eat_sound = sdlmixer.Mix_LoadWAV(b"Source/Sound/eat dot.wav")
    eat_ghost = sdlmixer.Mix_LoadWAV(b"Source/Sound/eat ghost.wav")
    eye_sound = sdlmixer.Mix_LoadWAV(b"Source/Sound/ghost go home.wav")

	# Создание окна
    WIDTH = 900
    HEIGHT = 950
    window = Window("Pac-man", (WIDTH, HEIGHT), flags=SDL_WINDOW_SHOWN)
    window.show()
    
    # Проверка на запуск с аппаратным или программным ускорением
    if "-hardware" in sys.argv:
        print(1)
        render_flags = (SDL_RENDERER_ACCELERATED | SDL_RENDERER_PRESENTVSYNC | SDL_RENDERER_TARGETTEXTURE)
    else:
        print(0)
        render_flags = (SDL_RENDERER_SOFTWARE | SDL_RENDERER_PRESENTVSYNC)
    
    # Создание рендера
    renderer = Renderer(window, backend=-1, flags=render_flags)
    set_texture_scale_quality(method="best")

    # Объявление фабричного класса для создания спрайтов (текстур)
    factory = SpriteFactory(TEXTURE, renderer=renderer)

    # текстуры кнопок
    tx_1 = factory.from_image(f'Source/Images/dot.png')
    tx_2 = factory.from_image(f'Source/Images/power dot.png')

    flicker = False   # для моргания жирных точек
    
    # Переменные для работы с функциями пакмана #
    player_images = []
    for i in range(1, 5):
        player_images.append(factory.from_image(f'Source/Images/pacman_{i}.png'))
    player_images.append(factory.from_image(f'Source/Images/pacman_live.png'))
    count = 0
    direction = 0
    turns_allowed = [False, False, False, False]
    player_speed = 2
    direction_command = 0
    player_x = 450
    player_y = 663
    score = 0
    powerup = False
    power_count = 0
    dead_ghost = [False, False, False, False, False, False, False]
    moving = False
    start_count = 0
    lives = 3

    # Переменные для работы с функциями призраков #
    blinky_tx = factory.from_image(f'Source/Images/blinky.png')
    inky_tx = factory.from_image(f'Source/Images/inky.png')
    pinky_tx = factory.from_image(f'Source/Images/pinky.png')
    clyde_tx = factory.from_image(f'Source/Images/clyde.png')
    ghost1_tx = factory.from_image(f'Source/Images/ghost_1.png')
    ghost2_tx = factory.from_image(f'Source/Images/ghost_2.png')
    ghost3_tx = factory.from_image(f'Source/Images/ghost_3.png')
    death_ghost_tx = factory.from_image(f'Source/Images/death_ghost.png')
    eye_tx = factory.from_image(f'Source/Images/eye.png')
    blinky_x = 56
    blinky_y = 58
    blinky_direction = 0
    inky_x = 440
    inky_y = 388
    inky_direction = 2
    pinky_x = 430
    pinky_y = 438
    pinky_direction = 2
    clyde_x = 440
    clyde_y = 438
    clyde_direction = 2
    ghost1_x = 65
    ghost1_y = 58
    ghost1_direction = 0
    ghost2_x = 450
    ghost2_y = 438
    ghost2_direction = 2
    ghost3_x = 700
    ghost3_y = 58
    ghost3_direction = 2
    targets_4 = [(player_x, player_y), (player_x, player_y), (player_x, player_y), (player_x, player_y)]
    targets_5 = [(player_x, player_y), (player_x, player_y), (player_x, player_y), (player_x, player_y),
               (player_x, player_y)]
    targets_6 = [(player_x, player_y), (player_x, player_y), (player_x, player_y), (player_x, player_y),
               (player_x, player_y), (player_x, player_y)]
    targets_7 = [(player_x, player_y), (player_x, player_y), (player_x, player_y), (player_x, player_y),
               (player_x, player_y), (player_x, player_y), (player_x, player_y)]
    blinky_dead = False
    inky_dead = False
    pinky_dead = False
    clyde_dead = False
    ghost1_dead = False
    ghost2_dead = False
    ghost3_dead = False
    blinky_box = False
    inky_box = False
    pinky_box = False
    clyde_box = False
    ghost1_box = False
    ghost2_box = False
    ghost3_box = False
    ghost_speeds = [2, 2, 2, 2, 2, 2, 2]

    # Экземпляр класса кнопок (button)
    work_button = ImageButton(window, renderer, WIDTH, HEIGHT)

	# Булевы переменные для работы с меню и игрой
    main_menu = True
    game_over = False
    game_win = False
    sound_check = True
    help_screen = False
    select_screen = False
    select_level = [False, False, False]
    select_ghost = [False, False, False, False]
    flag = True
    running = True
    
    while running:
        if main_menu:
            work_button.show_menu()
            if help_screen:
                work_button.render_clean()
                work_button.show_help()
            if select_screen:
                work_button.render_clean()
                work_button.show_select()
        if (select_ghost[0] or select_ghost[1] or select_ghost[2] or select_ghost[3]) and \
              (select_level[0] or select_level[1] or select_level[2]):
            work_button.render_clean()
            main_menu = False
            if flag:
                flag = False
                map = lvl.selected_level(select_level)

            if count < 19:
                count += 1
                if count > 3:
                    flicker = False
            else:
                count = 0
                flicker = True
            if powerup and power_count < 600:
                power_count += 1
            elif powerup and power_count >= 600:
                power_count = 0
                powerup = False
                dead_ghost = [False, False, False, False, False, False, False]
            if start_count < 56 and not game_over and not game_win:
                moving = False
                start_count += 1
            elif game_over or game_win:
                moving = False
            else:
                moving = True

            lvl.draw_board(renderer, WIDTH, HEIGHT, flicker, map, tx_1, tx_2)
            center_x = player_x + 23
            center_y = player_y + 24

            if powerup:
                ghost_speeds = [1, 1, 1, 1, 1, 1, 1]
            else:
                ghost_speeds = [2, 2, 2, 2, 2, 2, 2]
            if dead_ghost[0]:
                ghost_speeds[0] = 2
            if dead_ghost[1]:
                ghost_speeds[1] = 2
            if dead_ghost[2]:
                ghost_speeds[2] = 2
            if dead_ghost[3]:
                ghost_speeds[3] = 2
            if dead_ghost[4]:
                ghost_speeds[4] = 2
            if dead_ghost[5]:
                ghost_speeds[5] = 2
            if dead_ghost[6]:
                ghost_speeds[6] = 2
            if blinky_dead:
                ghost_speeds[0] = 4
                sdlmixer.Mix_PlayChannel(4, eye_sound, 0)
            if inky_dead:
                ghost_speeds[1] = 4
                sdlmixer.Mix_PlayChannel(4, eye_sound, 0)
            if pinky_dead:
                ghost_speeds[2] = 4
                sdlmixer.Mix_PlayChannel(4, eye_sound, 0)
            if clyde_dead:
                ghost_speeds[3] = 4
                sdlmixer.Mix_PlayChannel(4, eye_sound, 0)
            if ghost1_dead:
                ghost_speeds[4] = 4
                sdlmixer.Mix_PlayChannel(4, eye_sound, 0)
            if ghost2_dead:
                ghost_speeds[5] = 4
                sdlmixer.Mix_PlayChannel(4, eye_sound, 0)
            if ghost3_dead:
                ghost_speeds[6] = 4
                sdlmixer.Mix_PlayChannel(4, eye_sound, 0)

            game_win = True # проверка, есть ли точки на поле? Нет - победа!
            for i in range(len(map)):
                if 1 in map[i] or 2 in map[i]:
                    game_win = False

            # хитбокс пакмана
            player_rect = SDL_Rect(player_x + 17, player_y + 17, 18, 18)
            player.draw_player(renderer, count, direction, player_x, player_y, player_images)

            # добавление призраков в зависимости от выбора игрока
            if select_ghost[0]:
                blinky = Ghost(WIDTH, HEIGHT, blinky_x, blinky_y, targets_4[0], ghost_speeds[0], blinky_tx, blinky_direction,
                            blinky_dead, blinky_box, 0, renderer, map, powerup, dead_ghost, death_ghost_tx, eye_tx)
                inky = Ghost(WIDTH, HEIGHT, inky_x, inky_y, targets_4[1], ghost_speeds[1], inky_tx, inky_direction,
                            inky_dead, inky_box, 1, renderer, map, powerup, dead_ghost, death_ghost_tx, eye_tx)
                pinky = Ghost(WIDTH, HEIGHT, pinky_x, pinky_y, targets_4[2], ghost_speeds[2], pinky_tx, pinky_direction,
                            pinky_dead, pinky_box, 2, renderer, map, powerup, dead_ghost, death_ghost_tx, eye_tx)
                clyde = Ghost(WIDTH, HEIGHT, clyde_x, clyde_y, targets_4[3], ghost_speeds[3], clyde_tx, clyde_direction,
                            clyde_dead, clyde_box, 3, renderer, map, powerup, dead_ghost, death_ghost_tx, eye_tx)
                

                player.draw_counter(renderer, score, powerup, lives, game_over, game_win, player_images, factory)

                targets_4 = player.get_targets_4(blinky_x, blinky_y, inky_x, inky_y, pinky_x, pinky_y, clyde_x, clyde_y,
                                         player_x, player_y, powerup, dead_ghost, blinky, inky, pinky, clyde)
            
                turns_allowed = player.check_position(center_x, center_y, direction, WIDTH, HEIGHT, map)
            
                if moving:
                    player_x, player_y = player.move(player_x, player_y, direction, turns_allowed, player_speed)
                    if not blinky_dead and not blinky.in_box:
                        blinky_x, blinky_y, blinky_direction = blinky.move_blinky()
                    else:
                        blinky_x, blinky_y, blinky_direction = blinky.move_clyde()
                    if not pinky_dead and not pinky.in_box:
                        pinky_x, pinky_y, pinky_direction = pinky.move_pinky()
                    else:
                        pinky_x, pinky_y, pinky_direction = pinky.move_clyde()
                    if not inky_dead and not inky.in_box:
                        inky_x, inky_y, inky_direction = inky.move_inky()
                    else:
                        inky_x, inky_y, inky_direction = inky.move_clyde()
                    clyde_x, clyde_y, clyde_direction = clyde.move_clyde()

                score, powerup, power_count, dead_ghost = player.check_target(map, WIDTH, HEIGHT, score, player_x, center_x, center_y,
                                                                            powerup, power_count, dead_ghost, eat_sound)

                if not powerup:
                    if SDL_HasIntersection(player_rect, blinky.rect) and not blinky.dead or SDL_HasIntersection(player_rect, inky.rect) and not inky.dead or \
                            SDL_HasIntersection(player_rect, pinky.rect) and not pinky.dead or \
                                SDL_HasIntersection(player_rect, clyde.rect) and not clyde.dead:
                        if lives > 0:
                            lives -= 1
                            start_count = 0
                            powerup = False
                            power_count = 0
                            player_x = 450
                            player_y = 663
                            direction = 0
                            direction_command = 0
                            blinky_x = 56
                            blinky_y = 58
                            blinky_direction = 0
                            inky_x = 440
                            inky_y = 388
                            inky_direction = 2
                            pinky_x = 430
                            pinky_y = 438
                            pinky_direction = 2
                            clyde_x = 440
                            clyde_y = 438
                            clyde_direction = 2
                            dead_ghost = [False, False, False, False, False, False, False]
                            blinky_dead = False
                            inky_dead = False
                            pinky_dead = False
                            clyde_dead = False
                        else:
                            game_over = True
                            moving = False
                            start_count = 0
                if powerup and SDL_HasIntersection(player_rect, blinky.rect) and dead_ghost[0] and not blinky.dead:
                    if lives > 0:
                        powerup = False
                        power_count = 0
                        lives -= 1
                        start_count = 0
                        player_x = 450
                        player_y = 663
                        direction = 0
                        direction_command = 0
                        blinky_x = 56
                        blinky_y = 58
                        blinky_direction = 0
                        inky_x = 440
                        inky_y = 388
                        inky_direction = 2
                        pinky_x = 430
                        pinky_y = 438
                        pinky_direction = 2
                        clyde_x = 440
                        clyde_y = 438
                        clyde_direction = 2
                        dead_ghost = [False, False, False, False, False, False, False]
                        blinky_dead = False
                        inky_dead = False
                        pinky_dead = False
                        clyde_dead = False
                    else:
                        game_over = True
                        moving = False
                        start_count = 0
                if powerup and SDL_HasIntersection(player_rect, inky.rect) and dead_ghost[1] and not inky.dead:
                    if lives > 0:
                        powerup = False
                        power_count = 0
                        lives -= 1
                        start_count = 0
                        player_x = 450
                        player_y = 663
                        direction = 0
                        direction_command = 0
                        blinky_x = 56
                        blinky_y = 58
                        blinky_direction = 0
                        inky_x = 440
                        inky_y = 388
                        inky_direction = 2
                        pinky_x = 430
                        pinky_y = 438
                        pinky_direction = 2
                        clyde_x = 440
                        clyde_y = 438
                        clyde_direction = 2
                        dead_ghost = [False, False, False, False, False, False, False]
                        blinky_dead = False
                        inky_dead = False
                        pinky_dead = False
                        clyde_dead = False
                    else:
                        game_over = True
                        moving = False
                        start_count = 0
                if powerup and SDL_HasIntersection(player_rect, pinky.rect) and dead_ghost[2] and not pinky.dead:
                    if lives > 0:
                        powerup = False
                        power_count = 0
                        lives -= 1
                        start_count = 0
                        player_x = 450
                        player_y = 663
                        direction = 0
                        direction_command = 0
                        blinky_x = 56
                        blinky_y = 58
                        blinky_direction = 0
                        inky_x = 440
                        inky_y = 388
                        inky_direction = 2
                        pinky_x = 430
                        pinky_y = 438
                        pinky_direction = 2
                        clyde_x = 440
                        clyde_y = 438
                        clyde_direction = 2
                        dead_ghost = [False, False, False, False, False, False, False]
                        blinky_dead = False
                        inky_dead = False
                        pinky_dead = False
                        clyde_dead = False
                    else:
                        game_over = True
                        moving = False
                        start_count = 0 
                if powerup and SDL_HasIntersection(player_rect, clyde.rect) and dead_ghost[3] and not clyde.dead:
                    if lives > 0:
                        powerup = False
                        power_count = 0
                        lives -= 1
                        start_count = 0
                        player_x = 450
                        player_y = 663
                        direction = 0
                        direction_command = 0
                        blinky_x = 56
                        blinky_y = 58
                        blinky_direction = 0
                        inky_x = 440
                        inky_y = 388
                        inky_direction = 2
                        pinky_x = 430
                        pinky_y = 438
                        pinky_direction = 2
                        clyde_x = 440
                        clyde_y = 438
                        clyde_direction = 2
                        dead_ghost = [False, False, False, False, False, False, False]
                        blinky_dead = False
                        inky_dead = False
                        pinky_dead = False
                        clyde_dead = False
                    else:
                        game_over = True
                        moving = False
                        start_count = 0
                if powerup and SDL_HasIntersection(player_rect, blinky.rect) and not blinky.dead and not dead_ghost[0]:
                    blinky_dead = True
                    dead_ghost[0] = True
                    score += (2 ** dead_ghost.count(True)) * 100
                    sdlmixer.Mix_PlayChannel(3, eat_ghost, 0)
                if powerup and SDL_HasIntersection(player_rect, inky.rect) and not inky.dead and not dead_ghost[1]:
                    inky_dead = True
                    dead_ghost[1] = True
                    score += (2 ** dead_ghost.count(True)) * 100
                    sdlmixer.Mix_PlayChannel(3, eat_ghost, 0)
                if powerup and SDL_HasIntersection(player_rect, pinky.rect) and not pinky.dead and not dead_ghost[2]:
                    pinky_dead = True
                    dead_ghost[2] = True
                    score += (2 ** dead_ghost.count(True)) * 100
                    sdlmixer.Mix_PlayChannel(3, eat_ghost, 0)
                if powerup and SDL_HasIntersection(player_rect, clyde.rect) and not clyde.dead and not dead_ghost[3]:
                    clyde_dead = True
                    dead_ghost[3] = True
                    score += (2 ** dead_ghost.count(True)) * 100
                    sdlmixer.Mix_PlayChannel(3, eat_ghost, 0)
        
                if blinky.in_box and blinky_dead:
                    blinky_dead = False
                if inky.in_box and inky_dead:
                    inky_dead = False
                if pinky.in_box and pinky_dead:
                    pinky_dead = False
                if clyde.in_box and clyde_dead:
                    clyde_dead = False
            
            if select_ghost[1]:
                blinky = Ghost(WIDTH, HEIGHT, blinky_x, blinky_y, targets_5[0], ghost_speeds[0], blinky_tx, blinky_direction,
                            blinky_dead, blinky_box, 0, renderer, map, powerup, dead_ghost, death_ghost_tx, eye_tx)
                inky = Ghost(WIDTH, HEIGHT, inky_x, inky_y, targets_5[1], ghost_speeds[1], inky_tx, inky_direction,
                            inky_dead, inky_box, 1, renderer, map, powerup, dead_ghost, death_ghost_tx, eye_tx)
                pinky = Ghost(WIDTH, HEIGHT, pinky_x, pinky_y, targets_5[2], ghost_speeds[2], pinky_tx, pinky_direction,
                            pinky_dead, pinky_box, 2, renderer, map, powerup, dead_ghost, death_ghost_tx, eye_tx)
                clyde = Ghost(WIDTH, HEIGHT, clyde_x, clyde_y, targets_5[3], ghost_speeds[3], clyde_tx, clyde_direction,
                            clyde_dead, clyde_box, 3, renderer, map, powerup, dead_ghost, death_ghost_tx, eye_tx)
                ghost1 = Ghost(WIDTH, HEIGHT, ghost1_x, ghost1_y, targets_5[4], ghost_speeds[4], ghost1_tx, ghost1_direction,
                            ghost1_dead, ghost1_box, 4, renderer, map, powerup, dead_ghost, death_ghost_tx, eye_tx)
                

                player.draw_counter(renderer, score, powerup, lives, game_over, game_win, player_images, factory)

                targets_5 = player.get_targets_5(blinky_x, blinky_y, inky_x, inky_y, pinky_x, pinky_y, clyde_x, clyde_y,
                                                ghost1_x, ghost1_y, player_x, player_y, powerup, dead_ghost, blinky, inky, pinky, clyde, ghost1)
            
                turns_allowed = player.check_position(center_x, center_y, direction, WIDTH, HEIGHT, map)

                if moving:
                    player_x, player_y = player.move(player_x, player_y, direction, turns_allowed, player_speed)
                    if not blinky_dead and not blinky.in_box:
                        blinky_x, blinky_y, blinky_direction = blinky.move_blinky()
                    else:
                        blinky_x, blinky_y, blinky_direction = blinky.move_clyde()
                    if not pinky_dead and not pinky.in_box:
                        pinky_x, pinky_y, pinky_direction = pinky.move_pinky()
                    else:
                        pinky_x, pinky_y, pinky_direction = pinky.move_clyde()
                    if not inky_dead and not inky.in_box:
                        inky_x, inky_y, inky_direction = inky.move_inky()
                    else:
                        inky_x, inky_y, inky_direction = inky.move_clyde()
                    if not ghost1_dead and not ghost1.in_box:
                        ghost1_x, ghost1_y, ghost1_direction = ghost1.move_inky()
                    else:
                        ghost1_x, ghost1_y, ghost1_direction = ghost1.move_clyde()
                    clyde_x, clyde_y, clyde_direction = clyde.move_clyde()

                score, powerup, power_count, dead_ghost = player.check_target(map, WIDTH, HEIGHT, score, player_x, center_x, center_y,
                                                                            powerup, power_count, dead_ghost, eat_sound)
                
                if not powerup:
                    if SDL_HasIntersection(player_rect, blinky.rect) and not blinky.dead or SDL_HasIntersection(player_rect, inky.rect) and not inky.dead or \
                            SDL_HasIntersection(player_rect, pinky.rect) and not pinky.dead or \
                                SDL_HasIntersection(player_rect, clyde.rect) and not clyde.dead or \
                                    SDL_HasIntersection(player_rect, ghost1.rect) and not ghost1.dead:
                        if lives > 0:
                            lives -= 1
                            start_count = 0
                            powerup = False
                            power_count = 0
                            player_x = 450
                            player_y = 663
                            direction = 0
                            direction_command = 0
                            blinky_x = 56
                            blinky_y = 58
                            blinky_direction = 0
                            inky_x = 440
                            inky_y = 388
                            inky_direction = 2
                            pinky_x = 430
                            pinky_y = 438
                            pinky_direction = 2
                            clyde_x = 440
                            clyde_y = 438
                            clyde_direction = 2
                            ghost1_x = 65
                            ghost1_y = 58
                            ghost1_direction = 0
                            dead_ghost = [False, False, False, False, False, False, False]
                            blinky_dead = False
                            inky_dead = False
                            pinky_dead = False
                            clyde_dead = False
                            ghost1_dead = False
                        else:
                            game_over = True
                            moving = False
                            start_count = 0
                if powerup and SDL_HasIntersection(player_rect, blinky.rect) and dead_ghost[0] and not blinky.dead:
                    if lives > 0:
                        powerup = False
                        power_count = 0
                        lives -= 1
                        start_count = 0
                        player_x = 450
                        player_y = 663
                        direction = 0
                        direction_command = 0
                        blinky_x = 56
                        blinky_y = 58
                        blinky_direction = 0
                        inky_x = 440
                        inky_y = 388
                        inky_direction = 2
                        pinky_x = 430
                        pinky_y = 438
                        pinky_direction = 2
                        clyde_x = 440
                        clyde_y = 438
                        clyde_direction = 2
                        ghost1_x = 65
                        ghost1_y = 58
                        ghost1_direction = 0
                        dead_ghost = [False, False, False, False, False, False, False]
                        blinky_dead = False
                        inky_dead = False
                        pinky_dead = False
                        clyde_dead = False
                        ghost1_dead = False
                    else:
                        game_over = True
                        moving = False
                        start_count = 0
                if powerup and SDL_HasIntersection(player_rect, inky.rect) and dead_ghost[1] and not inky.dead:
                    if lives > 0:
                        powerup = False
                        power_count = 0
                        lives -= 1
                        start_count = 0
                        player_x = 450
                        player_y = 663
                        direction = 0
                        direction_command = 0
                        blinky_x = 56
                        blinky_y = 58
                        blinky_direction = 0
                        inky_x = 440
                        inky_y = 388
                        inky_direction = 2
                        pinky_x = 430
                        pinky_y = 438
                        pinky_direction = 2
                        clyde_x = 440
                        clyde_y = 438
                        clyde_direction = 2
                        ghost1_x = 65
                        ghost1_y = 58
                        ghost1_direction = 0
                        dead_ghost = [False, False, False, False, False, False, False]
                        blinky_dead = False
                        inky_dead = False
                        pinky_dead = False
                        clyde_dead = False
                        ghost1_dead = False
                    else:
                        game_over = True
                        moving = False
                        start_count = 0
                if powerup and SDL_HasIntersection(player_rect, pinky.rect) and dead_ghost[2] and not pinky.dead:
                    if lives > 0:
                        powerup = False
                        power_count = 0
                        lives -= 1
                        start_count = 0
                        player_x = 450
                        player_y = 663
                        direction = 0
                        direction_command = 0
                        blinky_x = 56
                        blinky_y = 58
                        blinky_direction = 0
                        inky_x = 440
                        inky_y = 388
                        inky_direction = 2
                        pinky_x = 430
                        pinky_y = 438
                        pinky_direction = 2
                        clyde_x = 440
                        clyde_y = 438
                        clyde_direction = 2
                        ghost1_x = 65
                        ghost1_y = 58
                        ghost1_direction = 0
                        dead_ghost = [False, False, False, False, False, False, False]
                        blinky_dead = False
                        inky_dead = False
                        pinky_dead = False
                        clyde_dead = False
                        ghost1_dead = False
                    else:
                        game_over = True
                        moving = False
                        start_count = 0 
                if powerup and SDL_HasIntersection(player_rect, clyde.rect) and dead_ghost[3] and not clyde.dead:
                    if lives > 0:
                        powerup = False
                        power_count = 0
                        lives -= 1
                        start_count = 0
                        player_x = 450
                        player_y = 663
                        direction = 0
                        direction_command = 0
                        blinky_x = 56
                        blinky_y = 58
                        blinky_direction = 0
                        inky_x = 440
                        inky_y = 388
                        inky_direction = 2
                        pinky_x = 430
                        pinky_y = 438
                        pinky_direction = 2
                        clyde_x = 440
                        clyde_y = 438
                        clyde_direction = 2
                        ghost1_x = 65
                        ghost1_y = 58
                        ghost1_direction = 0
                        dead_ghost = [False, False, False, False, False, False, False]
                        blinky_dead = False
                        inky_dead = False
                        pinky_dead = False
                        clyde_dead = False
                        ghost1_dead = False
                    else:
                        game_over = True
                        moving = False
                        start_count = 0
                if powerup and SDL_HasIntersection(player_rect, ghost1.rect) and dead_ghost[4] and not ghost1.dead:
                    if lives > 0:
                        powerup = False
                        power_count = 0
                        lives -= 1
                        start_count = 0
                        player_x = 450
                        player_y = 663
                        direction = 0
                        direction_command = 0
                        blinky_x = 56
                        blinky_y = 58
                        blinky_direction = 0
                        inky_x = 440
                        inky_y = 388
                        inky_direction = 2
                        pinky_x = 430
                        pinky_y = 438
                        pinky_direction = 2
                        clyde_x = 440
                        clyde_y = 438
                        clyde_direction = 2
                        ghost1_x = 65
                        ghost1_y = 58
                        ghost1_direction = 0
                        dead_ghost = [False, False, False, False, False, False, False]
                        blinky_dead = False
                        inky_dead = False
                        pinky_dead = False
                        clyde_dead = False
                        ghost1_dead = False
                    else:
                        game_over = True
                        moving = False
                        start_count = 0
                if powerup and SDL_HasIntersection(player_rect, blinky.rect) and not blinky.dead and not dead_ghost[0]:
                    blinky_dead = True
                    dead_ghost[0] = True
                    score += (2 ** dead_ghost.count(True)) * 100
                    sdlmixer.Mix_PlayChannel(3, eat_ghost, 0)
                if powerup and SDL_HasIntersection(player_rect, inky.rect) and not inky.dead and not dead_ghost[1]:
                    inky_dead = True
                    dead_ghost[1] = True
                    score += (2 ** dead_ghost.count(True)) * 100
                    sdlmixer.Mix_PlayChannel(3, eat_ghost, 0)
                if powerup and SDL_HasIntersection(player_rect, pinky.rect) and not pinky.dead and not dead_ghost[2]:
                    pinky_dead = True
                    dead_ghost[2] = True
                    score += (2 ** dead_ghost.count(True)) * 100
                    sdlmixer.Mix_PlayChannel(3, eat_ghost, 0)
                if powerup and SDL_HasIntersection(player_rect, clyde.rect) and not clyde.dead and not dead_ghost[3]:
                    clyde_dead = True
                    dead_ghost[3] = True
                    score += (2 ** dead_ghost.count(True)) * 100
                    sdlmixer.Mix_PlayChannel(3, eat_ghost, 0)
                if powerup and SDL_HasIntersection(player_rect, ghost1.rect) and not ghost1.dead and not dead_ghost[4]:
                    ghost1_dead = True
                    dead_ghost[4] = True
                    score += (2 ** dead_ghost.count(True)) * 100
                    sdlmixer.Mix_PlayChannel(3, eat_ghost, 0)

                if blinky.in_box and blinky_dead:
                    blinky_dead = False
                if inky.in_box and inky_dead:
                    inky_dead = False
                if pinky.in_box and pinky_dead:
                    pinky_dead = False
                if clyde.in_box and clyde_dead:
                    clyde_dead = False
                if ghost1.in_box and ghost1_dead:
                    ghost1_dead = False

            if select_ghost[2]:
                blinky = Ghost(WIDTH, HEIGHT, blinky_x, blinky_y, targets_6[0], ghost_speeds[0], blinky_tx, blinky_direction,
                            blinky_dead, blinky_box, 0, renderer, map, powerup, dead_ghost, death_ghost_tx, eye_tx)
                inky = Ghost(WIDTH, HEIGHT, inky_x, inky_y, targets_6[1], ghost_speeds[1], inky_tx, inky_direction,
                            inky_dead, inky_box, 1, renderer, map, powerup, dead_ghost, death_ghost_tx, eye_tx)
                pinky = Ghost(WIDTH, HEIGHT, pinky_x, pinky_y, targets_6[2], ghost_speeds[2], pinky_tx, pinky_direction,
                            pinky_dead, pinky_box, 2, renderer, map, powerup, dead_ghost, death_ghost_tx, eye_tx)
                clyde = Ghost(WIDTH, HEIGHT, clyde_x, clyde_y, targets_6[3], ghost_speeds[3], clyde_tx, clyde_direction,
                            clyde_dead, clyde_box, 3, renderer, map, powerup, dead_ghost, death_ghost_tx, eye_tx)
                ghost1 = Ghost(WIDTH, HEIGHT, ghost1_x, ghost1_y, targets_6[4], ghost_speeds[4], ghost1_tx, ghost1_direction,
                            ghost1_dead, ghost1_box, 4, renderer, map, powerup, dead_ghost, death_ghost_tx, eye_tx)
                ghost2 = Ghost(WIDTH, HEIGHT, ghost2_x, ghost2_y, targets_6[5], ghost_speeds[5], ghost2_tx, ghost2_direction,
                            ghost2_dead, ghost2_box, 5, renderer, map, powerup, dead_ghost, death_ghost_tx, eye_tx)
                

                player.draw_counter(renderer, score, powerup, lives, game_over, game_win, player_images, factory)

                targets_6 = player.get_targets_6(blinky_x, blinky_y, inky_x, inky_y, pinky_x, pinky_y, clyde_x, clyde_y,
                                                ghost1_x, ghost1_y, ghost2_x, ghost2_y,
                                                player_x, player_y, powerup, dead_ghost, blinky, inky, pinky, clyde, ghost1, ghost2)
            
                turns_allowed = player.check_position(center_x, center_y, direction, WIDTH, HEIGHT, map)

                if moving:
                    player_x, player_y = player.move(player_x, player_y, direction, turns_allowed, player_speed)
                    if not blinky_dead and not blinky.in_box:
                        blinky_x, blinky_y, blinky_direction = blinky.move_blinky()
                    else:
                        blinky_x, blinky_y, blinky_direction = blinky.move_clyde()
                    if not pinky_dead and not pinky.in_box:
                        pinky_x, pinky_y, pinky_direction = pinky.move_pinky()
                    else:
                        pinky_x, pinky_y, pinky_direction = pinky.move_clyde()
                    if not inky_dead and not inky.in_box:
                        inky_x, inky_y, inky_direction = inky.move_inky()
                    else:
                        inky_x, inky_y, inky_direction = inky.move_clyde()
                    if not ghost1_dead and not ghost1.in_box:
                        ghost1_x, ghost1_y, ghost1_direction = ghost1.move_inky()
                    else:
                        ghost1_x, ghost1_y, ghost1_direction = ghost1.move_clyde()
                    if not ghost2_dead and not ghost2.in_box:
                        ghost2_x, ghost2_y, ghost2_direction = ghost2.move_pinky()
                    else:
                        ghost2_x, ghost2_y, ghost2_direction = ghost2.move_clyde()
                    clyde_x, clyde_y, clyde_direction = clyde.move_clyde()

                score, powerup, power_count, dead_ghost = player.check_target(map, WIDTH, HEIGHT, score, player_x, center_x, center_y,
                                                                            powerup, power_count, dead_ghost, eat_sound)
                
                if not powerup:
                    if SDL_HasIntersection(player_rect, blinky.rect) and not blinky.dead or SDL_HasIntersection(player_rect, inky.rect) and not inky.dead or \
                            SDL_HasIntersection(player_rect, pinky.rect) and not pinky.dead or \
                                SDL_HasIntersection(player_rect, clyde.rect) and not clyde.dead or \
                                    SDL_HasIntersection(player_rect, ghost1.rect) and not ghost1.dead or \
                                        SDL_HasIntersection(player_rect, ghost2.rect) and not ghost2.dead:
                        if lives > 0:
                            lives -= 1
                            start_count = 0
                            powerup = False
                            power_count = 0
                            player_x = 450
                            player_y = 663
                            direction = 0
                            direction_command = 0
                            blinky_x = 56
                            blinky_y = 58
                            blinky_direction = 0
                            inky_x = 440
                            inky_y = 388
                            inky_direction = 2
                            pinky_x = 430
                            pinky_y = 438
                            pinky_direction = 2
                            clyde_x = 440
                            clyde_y = 438
                            clyde_direction = 2
                            ghost1_x = 65
                            ghost1_y = 58
                            ghost1_direction = 0
                            ghost2_x = 450
                            ghost2_y = 438
                            ghost2_direction = 2
                            dead_ghost = [False, False, False, False, False, False, False]
                            blinky_dead = False
                            inky_dead = False
                            pinky_dead = False
                            clyde_dead = False
                            ghost1_dead = False
                            ghost2_dead = False
                        else:
                            game_over = True
                            moving = False
                            start_count = 0
                if powerup and SDL_HasIntersection(player_rect, blinky.rect) and dead_ghost[0] and not blinky.dead:
                    if lives > 0:
                        powerup = False
                        power_count = 0
                        lives -= 1
                        start_count = 0
                        player_x = 450
                        player_y = 663
                        direction = 0
                        direction_command = 0
                        blinky_x = 56
                        blinky_y = 58
                        blinky_direction = 0
                        inky_x = 440
                        inky_y = 388
                        inky_direction = 2
                        pinky_x = 430
                        pinky_y = 438
                        pinky_direction = 2
                        clyde_x = 440
                        clyde_y = 438
                        clyde_direction = 2
                        ghost1_x = 65
                        ghost1_y = 58
                        ghost1_direction = 0
                        ghost2_x = 450
                        ghost2_y = 438
                        ghost2_direction = 2
                        dead_ghost = [False, False, False, False, False, False, False]
                        blinky_dead = False
                        inky_dead = False
                        pinky_dead = False
                        clyde_dead = False
                        ghost1_dead = False
                        ghost2_dead = False
                    else:
                        game_over = True
                        moving = False
                        start_count = 0
                if powerup and SDL_HasIntersection(player_rect, inky.rect) and dead_ghost[1] and not inky.dead:
                    if lives > 0:
                        powerup = False
                        power_count = 0
                        lives -= 1
                        start_count = 0
                        player_x = 450
                        player_y = 663
                        direction = 0
                        direction_command = 0
                        blinky_x = 56
                        blinky_y = 58
                        blinky_direction = 0
                        inky_x = 440
                        inky_y = 388
                        inky_direction = 2
                        pinky_x = 430
                        pinky_y = 438
                        pinky_direction = 2
                        clyde_x = 440
                        clyde_y = 438
                        clyde_direction = 2
                        ghost1_x = 65
                        ghost1_y = 58
                        ghost1_direction = 0
                        ghost2_x = 450
                        ghost2_y = 438
                        ghost2_direction = 2
                        dead_ghost = [False, False, False, False, False, False, False]
                        blinky_dead = False
                        inky_dead = False
                        pinky_dead = False
                        clyde_dead = False
                        ghost1_dead = False
                        ghost2_dead = False
                    else:
                        game_over = True
                        moving = False
                        start_count = 0
                if powerup and SDL_HasIntersection(player_rect, pinky.rect) and dead_ghost[2] and not pinky.dead:
                    if lives > 0:
                        powerup = False
                        power_count = 0
                        lives -= 1
                        start_count = 0
                        player_x = 450
                        player_y = 663
                        direction = 0
                        direction_command = 0
                        blinky_x = 56
                        blinky_y = 58
                        blinky_direction = 0
                        inky_x = 440
                        inky_y = 388
                        inky_direction = 2
                        pinky_x = 430
                        pinky_y = 438
                        pinky_direction = 2
                        clyde_x = 440
                        clyde_y = 438
                        clyde_direction = 2
                        ghost1_x = 65
                        ghost1_y = 58
                        ghost1_direction = 0
                        ghost2_x = 450
                        ghost2_y = 438
                        ghost2_direction = 2
                        dead_ghost = [False, False, False, False, False, False, False]
                        blinky_dead = False
                        inky_dead = False
                        pinky_dead = False
                        clyde_dead = False
                        ghost1_dead = False
                        ghost2_dead = False
                    else:
                        game_over = True
                        moving = False
                        start_count = 0 
                if powerup and SDL_HasIntersection(player_rect, clyde.rect) and dead_ghost[3] and not clyde.dead:
                    if lives > 0:
                        powerup = False
                        power_count = 0
                        lives -= 1
                        start_count = 0
                        player_x = 450
                        player_y = 663
                        direction = 0
                        direction_command = 0
                        blinky_x = 56
                        blinky_y = 58
                        blinky_direction = 0
                        inky_x = 440
                        inky_y = 388
                        inky_direction = 2
                        pinky_x = 430
                        pinky_y = 438
                        pinky_direction = 2
                        clyde_x = 440
                        clyde_y = 438
                        clyde_direction = 2
                        ghost1_x = 65
                        ghost1_y = 58
                        ghost1_direction = 0
                        ghost2_x = 450
                        ghost2_y = 438
                        ghost2_direction = 2
                        dead_ghost = [False, False, False, False, False, False, False]
                        blinky_dead = False
                        inky_dead = False
                        pinky_dead = False
                        clyde_dead = False
                        ghost1_dead = False
                        ghost2_dead = False
                    else:
                        game_over = True
                        moving = False
                        start_count = 0
                if powerup and SDL_HasIntersection(player_rect, ghost1.rect) and dead_ghost[4] and not ghost1.dead:
                    if lives > 0:
                        powerup = False
                        power_count = 0
                        lives -= 1
                        start_count = 0
                        player_x = 450
                        player_y = 663
                        direction = 0
                        direction_command = 0
                        blinky_x = 56
                        blinky_y = 58
                        blinky_direction = 0
                        inky_x = 440
                        inky_y = 388
                        inky_direction = 2
                        pinky_x = 430
                        pinky_y = 438
                        pinky_direction = 2
                        clyde_x = 440
                        clyde_y = 438
                        clyde_direction = 2
                        ghost1_x = 65
                        ghost1_y = 58
                        ghost1_direction = 0
                        ghost2_x = 450
                        ghost2_y = 438
                        ghost2_direction = 2
                        dead_ghost = [False, False, False, False, False, False, False]
                        blinky_dead = False
                        inky_dead = False
                        pinky_dead = False
                        clyde_dead = False
                        ghost1_dead = False
                        ghost2_dead = False
                    else:
                        game_over = True
                        moving = False
                        start_count = 0
                if powerup and SDL_HasIntersection(player_rect, ghost2.rect) and dead_ghost[5] and not ghost2.dead:
                    if lives > 0:
                        powerup = False
                        power_count = 0
                        lives -= 1
                        start_count = 0
                        player_x = 450
                        player_y = 663
                        direction = 0
                        direction_command = 0
                        blinky_x = 56
                        blinky_y = 58
                        blinky_direction = 0
                        inky_x = 440
                        inky_y = 388
                        inky_direction = 2
                        pinky_x = 430
                        pinky_y = 438
                        pinky_direction = 2
                        clyde_x = 440
                        clyde_y = 438
                        clyde_direction = 2
                        ghost1_x = 65
                        ghost1_y = 58
                        ghost1_direction = 0
                        ghost2_x = 450
                        ghost2_y = 438
                        ghost2_direction = 2
                        dead_ghost = [False, False, False, False, False, False, False]
                        blinky_dead = False
                        inky_dead = False
                        pinky_dead = False
                        clyde_dead = False
                        ghost1_dead = False
                        ghost2_dead = False
                    else:
                        game_over = True
                        moving = False
                        start_count = 0
                if powerup and SDL_HasIntersection(player_rect, blinky.rect) and not blinky.dead and not dead_ghost[0]:
                    blinky_dead = True
                    dead_ghost[0] = True
                    score += (2 ** dead_ghost.count(True)) * 100
                    sdlmixer.Mix_PlayChannel(3, eat_ghost, 0)
                if powerup and SDL_HasIntersection(player_rect, inky.rect) and not inky.dead and not dead_ghost[1]:
                    inky_dead = True
                    dead_ghost[1] = True
                    score += (2 ** dead_ghost.count(True)) * 100
                    sdlmixer.Mix_PlayChannel(3, eat_ghost, 0)
                if powerup and SDL_HasIntersection(player_rect, pinky.rect) and not pinky.dead and not dead_ghost[2]:
                    pinky_dead = True
                    dead_ghost[2] = True
                    score += (2 ** dead_ghost.count(True)) * 100
                    sdlmixer.Mix_PlayChannel(3, eat_ghost, 0)
                if powerup and SDL_HasIntersection(player_rect, clyde.rect) and not clyde.dead and not dead_ghost[3]:
                    clyde_dead = True
                    dead_ghost[3] = True
                    score += (2 ** dead_ghost.count(True)) * 100
                    sdlmixer.Mix_PlayChannel(3, eat_ghost, 0)
                if powerup and SDL_HasIntersection(player_rect, ghost1.rect) and not ghost1.dead and not dead_ghost[4]:
                    ghost1_dead = True
                    dead_ghost[4] = True
                    score += (2 ** dead_ghost.count(True)) * 100
                    sdlmixer.Mix_PlayChannel(3, eat_ghost, 0)
                if powerup and SDL_HasIntersection(player_rect, ghost2.rect) and not ghost2.dead and not dead_ghost[5]:
                    ghost2_dead = True
                    dead_ghost[5] = True
                    score += (2 ** dead_ghost.count(True)) * 100
                    sdlmixer.Mix_PlayChannel(3, eat_ghost, 0)
                
                if blinky.in_box and blinky_dead:
                    blinky_dead = False
                if inky.in_box and inky_dead:
                    inky_dead = False
                if pinky.in_box and pinky_dead:
                    pinky_dead = False
                if clyde.in_box and clyde_dead:
                    clyde_dead = False
                if ghost1.in_box and ghost1_dead:
                    ghost1_dead = False
                if ghost2.in_box and ghost2_dead:
                    ghost2_dead = False

            if select_ghost[3]:
                blinky = Ghost(WIDTH, HEIGHT, blinky_x, blinky_y, targets_7[0], ghost_speeds[0], blinky_tx, blinky_direction,
                            blinky_dead, blinky_box, 0, renderer, map, powerup, dead_ghost, death_ghost_tx, eye_tx)
                inky = Ghost(WIDTH, HEIGHT, inky_x, inky_y, targets_7[1], ghost_speeds[1], inky_tx, inky_direction,
                            inky_dead, inky_box, 1, renderer, map, powerup, dead_ghost, death_ghost_tx, eye_tx)
                pinky = Ghost(WIDTH, HEIGHT, pinky_x, pinky_y, targets_7[2], ghost_speeds[2], pinky_tx, pinky_direction,
                            pinky_dead, pinky_box, 2, renderer, map, powerup, dead_ghost, death_ghost_tx, eye_tx)
                clyde = Ghost(WIDTH, HEIGHT, clyde_x, clyde_y, targets_7[3], ghost_speeds[3], clyde_tx, clyde_direction,
                            clyde_dead, clyde_box, 3, renderer, map, powerup, dead_ghost, death_ghost_tx, eye_tx)
                ghost1 = Ghost(WIDTH, HEIGHT, ghost1_x, ghost1_y, targets_7[4], ghost_speeds[4], ghost1_tx, ghost1_direction,
                            ghost1_dead, ghost1_box, 4, renderer, map, powerup, dead_ghost, death_ghost_tx, eye_tx)
                ghost2 = Ghost(WIDTH, HEIGHT, ghost2_x, ghost2_y, targets_7[5], ghost_speeds[5], ghost2_tx, ghost2_direction,
                            ghost2_dead, ghost2_box, 5, renderer, map, powerup, dead_ghost, death_ghost_tx, eye_tx)
                ghost3 = Ghost(WIDTH, HEIGHT, ghost3_x, ghost3_y, targets_7[6], ghost_speeds[6], ghost3_tx, ghost3_direction,
                            ghost3_dead, ghost3_box, 6, renderer, map, powerup, dead_ghost, death_ghost_tx, eye_tx)

                player.draw_counter(renderer, score, powerup, lives, game_over, game_win, player_images, factory)

                targets_7 = player.get_targets_7(blinky_x, blinky_y, inky_x, inky_y, pinky_x, pinky_y, clyde_x, clyde_y,
                                            ghost1_x, ghost1_y, ghost2_x, ghost2_y, ghost3_x, ghost3_y,
                                            player_x, player_y, powerup, dead_ghost, blinky, inky, pinky, clyde, ghost1, ghost2, ghost3)
                
                turns_allowed = player.check_position(center_x, center_y, direction, WIDTH, HEIGHT, map)
                
                if moving:
                    player_x, player_y = player.move(player_x, player_y, direction, turns_allowed, player_speed)
                    if not blinky_dead and not blinky.in_box:
                        blinky_x, blinky_y, blinky_direction = blinky.move_blinky()
                    else:
                        blinky_x, blinky_y, blinky_direction = blinky.move_clyde()
                    if not pinky_dead and not pinky.in_box:
                        pinky_x, pinky_y, pinky_direction = pinky.move_pinky()
                    else:
                        pinky_x, pinky_y, pinky_direction = pinky.move_clyde()
                    if not inky_dead and not inky.in_box:
                        inky_x, inky_y, inky_direction = inky.move_inky()
                    else:
                        inky_x, inky_y, inky_direction = inky.move_clyde()
                    if not ghost1_dead and not ghost1.in_box:
                        ghost1_x, ghost1_y, ghost1_direction = ghost1.move_inky()
                    else:
                        ghost1_x, ghost1_y, ghost1_direction = ghost1.move_clyde()
                    if not ghost2_dead and not ghost2.in_box:
                        ghost2_x, ghost2_y, ghost2_direction = ghost2.move_pinky()
                    else:
                        ghost2_x, ghost2_y, ghost2_direction = ghost2.move_clyde()
                    if not ghost3_dead and not ghost3.in_box:
                        ghost3_x, ghost3_y, ghost3_direction = ghost3.move_inky()
                    else:
                        ghost3_x, ghost3_y, ghost3_direction = ghost3.move_clyde()
                    clyde_x, clyde_y, clyde_direction = clyde.move_clyde()

                score, powerup, power_count, dead_ghost = player.check_target(map, WIDTH, HEIGHT, score, player_x, center_x, center_y,
                                                                            powerup, power_count, dead_ghost, eat_sound)

                if not powerup:
                    if SDL_HasIntersection(player_rect, blinky.rect) and not blinky.dead or SDL_HasIntersection(player_rect, inky.rect) and not inky.dead or \
                            SDL_HasIntersection(player_rect, pinky.rect) and not pinky.dead or \
                                SDL_HasIntersection(player_rect, clyde.rect) and not clyde.dead or \
                                    SDL_HasIntersection(player_rect, ghost1.rect) and not ghost1.dead or \
                                        SDL_HasIntersection(player_rect, ghost2.rect) and not ghost2.dead or \
                                            SDL_HasIntersection(player_rect, ghost3.rect) and not ghost3.dead:
                        if lives > 0:
                            lives -= 1
                            start_count = 0
                            powerup = False
                            power_count = 0
                            player_x = 450
                            player_y = 663
                            direction = 0
                            direction_command = 0
                            blinky_x = 56
                            blinky_y = 58
                            blinky_direction = 0
                            inky_x = 440
                            inky_y = 388
                            inky_direction = 2
                            pinky_x = 430
                            pinky_y = 438
                            pinky_direction = 2
                            clyde_x = 440
                            clyde_y = 438
                            clyde_direction = 2
                            ghost1_x = 65
                            ghost1_y = 58
                            ghost1_direction = 0
                            ghost2_x = 450
                            ghost2_y = 438
                            ghost2_direction = 2
                            ghost3_x = 700
                            ghost3_y = 58
                            ghost3_direction = 2
                            dead_ghost = [False, False, False, False, False, False, False]
                            blinky_dead = False
                            inky_dead = False
                            pinky_dead = False
                            clyde_dead = False
                            ghost1_dead = False
                            ghost2_dead = False
                            ghost3_dead = False
                        else:
                            game_over = True
                            moving = False
                            start_count = 0
                if powerup and SDL_HasIntersection(player_rect, blinky.rect) and dead_ghost[0] and not blinky.dead:
                    if lives > 0:
                        powerup = False
                        power_count = 0
                        lives -= 1
                        start_count = 0
                        player_x = 450
                        player_y = 663
                        direction = 0
                        direction_command = 0
                        blinky_x = 56
                        blinky_y = 58
                        blinky_direction = 0
                        inky_x = 440
                        inky_y = 388
                        inky_direction = 2
                        pinky_x = 430
                        pinky_y = 438
                        pinky_direction = 2
                        clyde_x = 440
                        clyde_y = 438
                        clyde_direction = 2
                        ghost1_x = 65
                        ghost1_y = 58
                        ghost1_direction = 0
                        ghost2_x = 450
                        ghost2_y = 438
                        ghost2_direction = 2
                        ghost3_x = 700
                        ghost3_y = 58
                        ghost3_direction = 2
                        dead_ghost = [False, False, False, False, False, False, False]
                        blinky_dead = False
                        inky_dead = False
                        pinky_dead = False
                        clyde_dead = False
                        ghost1_dead = False
                        ghost2_dead = False
                        ghost3_dead = False
                    else:
                        game_over = True
                        moving = False
                        start_count = 0
                if powerup and SDL_HasIntersection(player_rect, inky.rect) and dead_ghost[1] and not inky.dead:
                    if lives > 0:
                        powerup = False
                        power_count = 0
                        lives -= 1
                        start_count = 0
                        player_x = 450
                        player_y = 663
                        direction = 0
                        direction_command = 0
                        blinky_x = 56
                        blinky_y = 58
                        blinky_direction = 0
                        inky_x = 440
                        inky_y = 388
                        inky_direction = 2
                        pinky_x = 430
                        pinky_y = 438
                        pinky_direction = 2
                        clyde_x = 440
                        clyde_y = 438
                        clyde_direction = 2
                        ghost1_x = 65
                        ghost1_y = 58
                        ghost1_direction = 0
                        ghost2_x = 450
                        ghost2_y = 438
                        ghost2_direction = 2
                        ghost3_x = 700
                        ghost3_y = 58
                        ghost3_direction = 2
                        dead_ghost = [False, False, False, False, False, False, False]
                        blinky_dead = False
                        inky_dead = False
                        pinky_dead = False
                        clyde_dead = False
                        ghost1_dead = False
                        ghost2_dead = False
                        ghost3_dead = False
                    else:
                        game_over = True
                        moving = False
                        start_count = 0
                if powerup and SDL_HasIntersection(player_rect, pinky.rect) and dead_ghost[2] and not pinky.dead:
                    if lives > 0:
                        powerup = False
                        power_count = 0
                        lives -= 1
                        start_count = 0
                        player_x = 450
                        player_y = 663
                        direction = 0
                        direction_command = 0
                        blinky_x = 56
                        blinky_y = 58
                        blinky_direction = 0
                        inky_x = 440
                        inky_y = 388
                        inky_direction = 2
                        pinky_x = 430
                        pinky_y = 438
                        pinky_direction = 2
                        clyde_x = 440
                        clyde_y = 438
                        clyde_direction = 2
                        ghost1_x = 65
                        ghost1_y = 58
                        ghost1_direction = 0
                        ghost2_x = 450
                        ghost2_y = 438
                        ghost2_direction = 2
                        ghost3_x = 700
                        ghost3_y = 58
                        ghost3_direction = 2
                        dead_ghost = [False, False, False, False, False, False, False]
                        blinky_dead = False
                        inky_dead = False
                        pinky_dead = False
                        clyde_dead = False
                        ghost1_dead = False
                        ghost2_dead = False
                        ghost3_dead = False
                    else:
                        game_over = True
                        moving = False
                        start_count = 0 
                if powerup and SDL_HasIntersection(player_rect, clyde.rect) and dead_ghost[3] and not clyde.dead:
                    if lives > 0:
                        powerup = False
                        power_count = 0
                        lives -= 1
                        start_count = 0
                        player_x = 450
                        player_y = 663
                        direction = 0
                        direction_command = 0
                        blinky_x = 56
                        blinky_y = 58
                        blinky_direction = 0
                        inky_x = 440
                        inky_y = 388
                        inky_direction = 2
                        pinky_x = 430
                        pinky_y = 438
                        pinky_direction = 2
                        clyde_x = 440
                        clyde_y = 438
                        clyde_direction = 2
                        ghost1_x = 65
                        ghost1_y = 58
                        ghost1_direction = 0
                        ghost2_x = 450
                        ghost2_y = 438
                        ghost2_direction = 2
                        ghost3_x = 700
                        ghost3_y = 58
                        ghost3_direction = 2
                        dead_ghost = [False, False, False, False, False, False, False]
                        blinky_dead = False
                        inky_dead = False
                        pinky_dead = False
                        clyde_dead = False
                        ghost1_dead = False
                        ghost2_dead = False
                        ghost3_dead = False
                    else:
                        game_over = True
                        moving = False
                        start_count = 0
                if powerup and SDL_HasIntersection(player_rect, ghost1.rect) and dead_ghost[4] and not ghost1.dead:
                    if lives > 0:
                        powerup = False
                        power_count = 0
                        lives -= 1
                        start_count = 0
                        player_x = 450
                        player_y = 663
                        direction = 0
                        direction_command = 0
                        blinky_x = 56
                        blinky_y = 58
                        blinky_direction = 0
                        inky_x = 440
                        inky_y = 388
                        inky_direction = 2
                        pinky_x = 430
                        pinky_y = 438
                        pinky_direction = 2
                        clyde_x = 440
                        clyde_y = 438
                        clyde_direction = 2
                        ghost1_x = 65
                        ghost1_y = 58
                        ghost1_direction = 0
                        ghost2_x = 450
                        ghost2_y = 438
                        ghost2_direction = 2
                        ghost3_x = 700
                        ghost3_y = 58
                        ghost3_direction = 2
                        dead_ghost = [False, False, False, False, False, False, False]
                        blinky_dead = False
                        inky_dead = False
                        pinky_dead = False
                        clyde_dead = False
                        ghost1_dead = False
                        ghost2_dead = False
                        ghost3_dead = False
                    else:
                        game_over = True
                        moving = False
                        start_count = 0
                if powerup and SDL_HasIntersection(player_rect, ghost2.rect) and dead_ghost[5] and not ghost2.dead:
                    if lives > 0:
                        powerup = False
                        power_count = 0
                        lives -= 1
                        start_count = 0
                        player_x = 450
                        player_y = 663
                        direction = 0
                        direction_command = 0
                        blinky_x = 56
                        blinky_y = 58
                        blinky_direction = 0
                        inky_x = 440
                        inky_y = 388
                        inky_direction = 2
                        pinky_x = 430
                        pinky_y = 438
                        pinky_direction = 2
                        clyde_x = 440
                        clyde_y = 438
                        clyde_direction = 2
                        ghost1_x = 65
                        ghost1_y = 58
                        ghost1_direction = 0
                        ghost2_x = 450
                        ghost2_y = 438
                        ghost2_direction = 2
                        ghost3_x = 700
                        ghost3_y = 58
                        ghost3_direction = 2
                        dead_ghost = [False, False, False, False, False, False, False]
                        blinky_dead = False
                        inky_dead = False
                        pinky_dead = False
                        clyde_dead = False
                        ghost1_dead = False
                        ghost2_dead = False
                        ghost3_dead = False
                    else:
                        game_over = True
                        moving = False
                        start_count = 0
                if powerup and SDL_HasIntersection(player_rect, ghost3.rect) and dead_ghost[6] and not ghost3.dead:
                    if lives > 0:
                        powerup = False
                        power_count = 0
                        lives -= 1
                        start_count = 0
                        player_x = 450
                        player_y = 663
                        direction = 0
                        direction_command = 0
                        blinky_x = 56
                        blinky_y = 58
                        blinky_direction = 0
                        inky_x = 440
                        inky_y = 388
                        inky_direction = 2
                        pinky_x = 430
                        pinky_y = 438
                        pinky_direction = 2
                        clyde_x = 440
                        clyde_y = 438
                        clyde_direction = 2
                        ghost1_x = 65
                        ghost1_y = 58
                        ghost1_direction = 0
                        ghost2_x = 450
                        ghost2_y = 438
                        ghost2_direction = 2
                        ghost3_x = 700
                        ghost3_y = 58
                        ghost3_direction = 2
                        dead_ghost = [False, False, False, False, False, False, False]
                        blinky_dead = False
                        inky_dead = False
                        pinky_dead = False
                        clyde_dead = False
                        ghost1_dead = False
                        ghost2_dead = False
                        ghost3_dead = False
                    else:
                        game_over = True
                        moving = False
                        start_count = 0
                if powerup and SDL_HasIntersection(player_rect, blinky.rect) and not blinky.dead and not dead_ghost[0]:
                    blinky_dead = True
                    dead_ghost[0] = True
                    score += (2 ** dead_ghost.count(True)) * 100
                    sdlmixer.Mix_PlayChannel(3, eat_ghost, 0)
                if powerup and SDL_HasIntersection(player_rect, inky.rect) and not inky.dead and not dead_ghost[1]:
                    inky_dead = True
                    dead_ghost[1] = True
                    score += (2 ** dead_ghost.count(True)) * 100
                    sdlmixer.Mix_PlayChannel(3, eat_ghost, 0)
                if powerup and SDL_HasIntersection(player_rect, pinky.rect) and not pinky.dead and not dead_ghost[2]:
                    pinky_dead = True
                    dead_ghost[2] = True
                    score += (2 ** dead_ghost.count(True)) * 100
                    sdlmixer.Mix_PlayChannel(3, eat_ghost, 0)
                if powerup and SDL_HasIntersection(player_rect, clyde.rect) and not clyde.dead and not dead_ghost[3]:
                    clyde_dead = True
                    dead_ghost[3] = True
                    score += (2 ** dead_ghost.count(True)) * 100
                    sdlmixer.Mix_PlayChannel(3, eat_ghost, 0)
                if powerup and SDL_HasIntersection(player_rect, ghost1.rect) and not ghost1.dead and not dead_ghost[4]:
                    ghost1_dead = True
                    dead_ghost[4] = True
                    score += (2 ** dead_ghost.count(True)) * 100
                    sdlmixer.Mix_PlayChannel(3, eat_ghost, 0)
                if powerup and SDL_HasIntersection(player_rect, ghost2.rect) and not ghost2.dead and not dead_ghost[5]:
                    ghost2_dead = True
                    dead_ghost[5] = True
                    score += (2 ** dead_ghost.count(True)) * 100
                    sdlmixer.Mix_PlayChannel(3, eat_ghost, 0)
                if powerup and SDL_HasIntersection(player_rect, ghost3.rect) and not ghost3.dead and not dead_ghost[6]:
                    ghost3_dead = True
                    dead_ghost[6] = True
                    score += (2 ** dead_ghost.count(True)) * 100
                    sdlmixer.Mix_PlayChannel(3, eat_ghost, 0)
            
                if blinky.in_box and blinky_dead:
                    blinky_dead = False
                if inky.in_box and inky_dead:
                    inky_dead = False
                if pinky.in_box and pinky_dead:
                    pinky_dead = False
                if clyde.in_box and clyde_dead:
                    clyde_dead = False
                if ghost1.in_box and ghost1_dead:
                    ghost1_dead = False
                if ghost2.in_box and ghost2_dead:
                    ghost2_dead = False
                if ghost3.in_box and ghost3_dead:
                    ghost3_dead = False

        events = get_events()
            # обработка событий
        for event in events:
            # сюда пишутся все if
            if event.type == SDL_QUIT:
                running = False
                break
            
            if event.type == SDL_MOUSEBUTTONDOWN:   # нажатие кнопок меню
                x, y = event.button.x, event.button.y
                if WIDTH // 4 <= x <= 618 and (HEIGHT // 4) + 96 <= y <= (HEIGHT // 4) + 144: # Начать игру
                    select_screen = True
                    work_button.play_sound()
                    work_button.render_clean()
                if WIDTH // 4 <= x <= 762 and (HEIGHT // 2) - 48 <= y <= (HEIGHT // 2): # Помощь
                    help_screen = True
                    work_button.play_sound()
                if 350 <= x <= 542 and HEIGHT - 96 <= y <= HEIGHT - 48: # Назад
                    work_button.play_sound()
                    work_button.render_clean()
                    main_menu = True
                    game_over = False
                    game_win = False
                    running = True
                    help_screen = False
                    select_screen = False
                    select_level = [False, False, False]
                    select_ghost = [False, False, False, False]
                
                if 60 <= x <= 160 and 272 <= y <= 392: # Кнопки выбора кол-ва призраков
                    select_ghost[0] = True
                    work_button.play_sound()
                if 60 <= x <= 160 and 440 <= y <= 560:
                    select_ghost[1] = True
                    work_button.play_sound()
                if 60 <= x <= 160 and 607 <= y <= 727:
                    select_ghost[2] = True
                    work_button.play_sound()
                if 60 <= x <= 160 and 773 <= y <= 893:
                    select_ghost[3] = True
                    work_button.play_sound()

                if 800 <= x <= 840 and 272 <= y <= 320: # Кнопки выбора карты
                    select_level[0] = True
                    work_button.play_sound()
                if 800 <= x <= 840 and 440 <= y <= 480:
                    select_level[1] = True
                    work_button.play_sound()
                if 800 <= x <= 840 and 607 <= y <= 647:
                    select_level[2] = True
                    work_button.play_sound()               

                if WIDTH // 4 <= x <= 438 and (HEIGHT // 2) + 48 <= y <= (HEIGHT // 2) + 96: # Выход
                    work_button.play_sound()
                    running = False
                    break
 
            if main_menu == False: # Музыка в начале
                if sound_check:
                    sdlmixer.Mix_PlayChannel(1, music_theme, 0)
                    sound_check = False
                
            if event.type == SDL_KEYDOWN:   # нажатие на стрелочки
                if event.key.keysym.sym == SDLK_RIGHT:
                    direction_command = 0
                if event.key.keysym.sym == SDLK_LEFT:
                    direction_command = 1
                if event.key.keysym.sym == SDLK_UP:
                    direction_command = 2
                if event.key.keysym.sym == SDLK_DOWN:
                    direction_command = 3
                if event.key.keysym.sym == SDLK_SPACE and (game_over or game_win):
                    powerup = False
                    power_count = 0
                    lives -= 1
                    start_count = 0
                    player_x = 450
                    player_y = 663
                    direction = 0
                    direction_command = 0
                    blinky_x = 56
                    blinky_y = 58
                    blinky_direction = 0
                    inky_x = 440
                    inky_y = 388
                    inky_direction = 2
                    pinky_x = 430
                    pinky_y = 438   
                    pinky_direction = 2
                    clyde_x = 440
                    clyde_y = 438
                    clyde_direction = 2
                    ghost1_x = 65
                    ghost1_y = 58
                    ghost1_direction = 0
                    ghost2_x = 450
                    ghost2_y = 438
                    ghost2_direction = 2
                    ghost3_x = 700
                    ghost3_y = 58
                    ghost3_direction = 2
                    dead_ghost = [False, False, False, False, False, False, False]
                    blinky_dead = False
                    inky_dead = False
                    clyde_dead = False
                    pinky_dead = False
                    ghost1_dead = False
                    ghost2_dead = False
                    ghost3_dead = False
                    score = 0
                    lives = 3
                    map = lvl.selected_level(select_level)
                    game_over = False
                    game_win = False
                    sound_check = True
            if event.type == SDL_KEYUP:
                if event.key.keysym.sym == SDLK_RIGHT and direction_command == 0:
                    direction_command = direction
                if event.key.keysym.sym == SDLK_LEFT and direction_command == 1:
                    direction_command = direction
                if event.key.keysym.sym == SDLK_UP and direction_command == 2:
                    direction_command = direction
                if event.key.keysym.sym == SDLK_DOWN and direction_command == 3:
                    direction_command = direction
        if direction_command == 0 and turns_allowed[0]:
            direction = 0
        if direction_command == 1 and turns_allowed[1]:
            direction = 1
        if direction_command == 2 and turns_allowed[2]:
            direction = 2
        if direction_command == 3 and turns_allowed[3]:
            direction = 3

        # появление пакмана с другого края карты
        if player_x > 900:
            player_x = -47
        elif player_x < -50:
            player_x = 897
         
        renderer.present()
        renderer.clear()
        window.refresh()
    renderer.destroy()
    window.close()
    quit()

if __name__ == "__main__":
    main()
