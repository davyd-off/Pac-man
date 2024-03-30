import sys
import copy
from sdl2 import *
from sdl2.ext import *
import sdl2.sdlmixer as sdlmixer
from button import ImageButton
import player
import level as lvl
from board_1 import boards
from ghost import Ghost

# Создание аудиоканала
sdlmixer.Mix_OpenAudio(44100, sdlmixer.MIX_DEFAULT_FORMAT, 2, 1024)

WIDTH = 900
HEIGHT = 950

music_theme = sdlmixer.Mix_LoadWAV(b"Source/Sound/start.wav")
eat_sound = sdlmixer.Mix_LoadWAV(b"Source/Sound/eat dot.wav")
eat_ghost = sdlmixer.Mix_LoadWAV(b"Source/Sound/eat ghost.wav")
eye_sound = sdlmixer.Mix_LoadWAV(b"Source/Sound/ghost go home.wav")

def main():
    init()
    
    window = Window("Pac-man", (WIDTH, HEIGHT), flags=SDL_WINDOW_RESIZABLE)
    window.show()
    
    if "-hardware" in sys.argv:
        print(1)
        render_flags = (SDL_RENDERER_ACCELERATED | SDL_RENDERER_PRESENTVSYNC | SDL_RENDERER_TARGETTEXTURE)
    else:
        print(0)
        render_flags = (SDL_RENDERER_SOFTWARE | SDL_RENDERER_PRESENTVSYNC)
    renderer = Renderer(window, backend=-1, flags=render_flags)
    set_texture_scale_quality(method="best")

    flicker = False   # для моргания жирных точек
    # Переменные для работы с функциями пакмана #
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
    dead_ghost = [False, False, False, False]
    moving = False
    start_count = 0
    lives = 3
    #############################################

    # Переменные для работы с функциями призраков #
    blinky_tx = Texture(renderer, load_image(b"Source/Images/blinky.png"))
    inky_tx = Texture(renderer, load_image(b"Source/Images/inky.png"))
    pinky_tx = Texture(renderer, load_image(b"Source/Images/pinky.png"))
    clyde_tx = Texture(renderer, load_image(b"Source/Images/clyde.png"))
    death_ghost_tx = Texture(renderer, load_image(b"Source/Images/death_ghost.png"))
    eye_tx = Texture(renderer, load_image(b"Source/Images/eye.png"))
    blinky_x = 56
    blinky_y = 58
    blinky_direction = 0
    inky_x = 440
    inky_y = 388
    inky_direction = 2
    pinky_x = 440
    pinky_y = 438
    pinky_direction = 2
    clyde_x = 440
    clyde_y = 438
    clyde_direction = 2
    targets = [(player_x, player_y), (player_x, player_y), (player_x, player_y), (player_x, player_y)]
    blinky_dead = False
    inky_dead = False
    pinky_dead = False
    clyde_dead = False
    blinky_box = False
    inky_box = False
    pinky_box = False
    clyde_box = False
    ghost_speeds = [2, 2, 2, 2]
    ###############################################

    # Экземпляры класса кнопок (button)
    work_button = ImageButton(window, renderer, WIDTH, HEIGHT)

    main_menu = True
    game_over = False
    game_win = False
    sound_check = True

    running = True
    while running:
        if main_menu:
            work_button.render_button()
        else:
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
                dead_ghost = [False, False, False, False]
            if start_count < 56 and not game_over and not game_win:
                moving = False
                start_count += 1
            else:
                moving = True

            lvl.draw_board(renderer, WIDTH, HEIGHT, flicker)
            center_x = player_x + 23
            center_y = player_y + 24

            if powerup:
                ghost_speeds = [1, 1, 1, 1]
            else:
                ghost_speeds = [2, 2, 2, 2]
            if dead_ghost[0]:
                ghost_speeds[0] = 2
            if dead_ghost[1]:
                ghost_speeds[1] = 2
            if dead_ghost[2]:
                ghost_speeds[2] = 2
            if dead_ghost[3]:
                ghost_speeds[3] = 2
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

            game_win = True
            for i in range(len(lvl.level)):
                if 1 in lvl.level[i] or 2 in lvl.level[i]:
                    game_win = False

            # хитбокс пакмана
            player_rect = SDL_Rect(center_x , center_y, 25, 25)
            player.draw_player(renderer, count, direction, player_x, player_y)

            blinky = Ghost(WIDTH, HEIGHT, blinky_x, blinky_y, targets[0], ghost_speeds[0], blinky_tx, blinky_direction,
                           blinky_dead, blinky_box, 0, renderer, lvl.level, powerup, dead_ghost, death_ghost_tx, eye_tx)
            inky = Ghost(WIDTH, HEIGHT, inky_x, inky_y, targets[1], ghost_speeds[1], inky_tx, inky_direction,
                         inky_dead, inky_box, 1, renderer, lvl.level, powerup, dead_ghost, death_ghost_tx, eye_tx)
            pinky = Ghost(WIDTH, HEIGHT, pinky_x, pinky_y, targets[2], ghost_speeds[2], pinky_tx, pinky_direction,
                          pinky_dead, pinky_box, 2, renderer, lvl.level, powerup, dead_ghost, death_ghost_tx, eye_tx)
            clyde = Ghost(WIDTH, HEIGHT, clyde_x, clyde_y, targets[3], ghost_speeds[3], clyde_tx, clyde_direction,
                          clyde_dead, clyde_box, 3, renderer, lvl.level, powerup, dead_ghost, death_ghost_tx, eye_tx)

            player.draw_counter(renderer, score, powerup, lives, game_over, game_win)

            targets = player.get_targets(blinky_x, blinky_y, inky_x, inky_y, pinky_x, pinky_y, clyde_x, clyde_y,
                                         player_x, player_y, powerup, dead_ghost, blinky, inky, pinky, clyde)
            
            turns_allowed = player.check_position(center_x, center_y, direction, WIDTH, HEIGHT, lvl.level)
            
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

            score, powerup, power_count, dead_ghost = player.check_target(lvl.level, WIDTH, HEIGHT, score, player_x, center_x, center_y,
                                                                          powerup, power_count, dead_ghost, eat_sound)

            if not powerup:
                if SDL_HasIntersection(player_rect, blinky.rect) and not blinky.dead or SDL_HasIntersection(player_rect, inky.rect) and not inky.dead or \
                        SDL_HasIntersection(player_rect, pinky.rect) and not pinky.dead or SDL_HasIntersection(player_rect, clyde.rect) and not clyde.dead:
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
                        pinky_x = 440
                        pinky_y = 438
                        pinky_direction = 2
                        clyde_x = 440
                        clyde_y = 438
                        clyde_direction = 2
                        dead_ghost = [False, False, False, False]
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
                    pinky_x = 440
                    pinky_y = 438
                    pinky_direction = 2
                    clyde_x = 440
                    clyde_y = 438
                    clyde_direction = 2
                    dead_ghost = [False, False, False, False]
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
                    pinky_x = 440
                    pinky_y = 438
                    pinky_direction = 2
                    clyde_x = 440
                    clyde_y = 438
                    clyde_direction = 2
                    dead_ghost = [False, False, False, False]
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
                    pinky_x = 440
                    pinky_y = 438
                    pinky_direction = 2
                    clyde_x = 440
                    clyde_y = 438
                    clyde_direction = 2
                    dead_ghost = [False, False, False, False]
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
                    pinky_x = 440
                    pinky_y = 438
                    pinky_direction = 2
                    clyde_x = 440
                    clyde_y = 438
                    clyde_direction = 2
                    dead_ghost = [False, False, False, False]
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

        events = get_events()
            # обработка событий
        for event in events:
            # сюда пишутся все if
            if event.type == SDL_QUIT:
                running = False
                break
            
            if event.type == SDL_MOUSEBUTTONDOWN:   # нажатие кнопок меню
                x, y = event.button.x, event.button.y
                if WIDTH // 4 <= x <= 618 and (HEIGHT // 4) + 96 <= y <= (HEIGHT // 4) + 144:
                    main_menu = False
                    work_button.play_sound()
                    work_button.render_clean()
                    print("Start Game button pressed")
                if WIDTH // 4 <= x <= 762 and (HEIGHT // 2) - 48 <= y <= (HEIGHT // 2):
                    work_button.play_sound()
                    print("Help button pressed")
                if WIDTH // 4 <= x <= 438 and (HEIGHT // 2) + 48 <= y <= (HEIGHT // 2) + 96:
                    work_button.play_sound()
                    running = False
                    break
 
            if main_menu == False:
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
                    pinky_x = 440
                    pinky_y = 438
                    pinky_direction = 2
                    clyde_x = 440
                    clyde_y = 438
                    clyde_direction = 2
                    dead_ghost = [False, False, False, False]
                    blinky_dead = False
                    inky_dead = False
                    clyde_dead = False
                    pinky_dead = False
                    score = 0
                    lives = 3
                    lvl.level = copy.deepcopy(boards)
                    game_over = False
                    game_win = False
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

        if player_x > 900:
            player_x = -47
        elif player_x < -50:
            player_x = 897
        
         
        renderer.present()
        renderer.clear()
    renderer.destroy()
    window.close()
    quit()


if __name__ == "__main__":
    main()