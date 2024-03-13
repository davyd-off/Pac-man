import sys
from sdl2 import *
from sdl2.ext import *
import sdl2.sdlmixer as sdlmixer
from button import ImageButton
import player
import level as lvl

# Создание аудиоканала
sdlmixer.Mix_OpenAudio(44100, sdlmixer.MIX_DEFAULT_FORMAT, 2, 1024)

# Создание кадров в секунду (провально)
fps = 60
frameDelay = 1000 // fps
frameStart = None
frameTime = None

WIDTH = 900
HEIGHT = 950

music_theme = sdlmixer.Mix_LoadMUS(b"Source/Sound/start.mp3")

def main():
    flicker = False
    # Переменные для работы с функциями игрока #
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

    init()
    
    window = Window("Pac-man", (WIDTH, HEIGHT), flags=SDL_WINDOW_RESIZABLE)
    window.show()
    
    if "-hardware" in sys.argv:
        print(1)
        render_flags = (SDL_RENDERER_ACCELERATED | SDL_RENDERER_PRESENTVSYNC | SDL_RENDERER_TARGETTEXTURE)
    else:
        print(0)
        render_flags = (SDL_RENDERER_SOFTWARE | SDL_RENDERER_PRESENTVSYNC | SDL_RENDERER_TARGETTEXTURE)
    renderer = Renderer(window, backend=-1, flags=render_flags)
    set_texture_scale_quality(method="best")

    # Экземпляры класса кнопок (button)
    work_button = ImageButton(window, renderer, WIDTH, HEIGHT)

    main_menu = True
    game_pause = True
    sound_check = True
    running = True
    while running:
        frameStart = SDL_GetTicks()

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
            if start_count < 56:
                moving = False
                start_count += 1
            else:
                moving = True

            lvl.draw_board(renderer, WIDTH, HEIGHT, flicker)
            player.draw_player(renderer, count, direction, player_x, player_y)
            player.draw_counter(renderer, score, powerup, lives)
            center_x = player_x + 23
            center_y = player_y + 24
            turns_allowed = player.check_position(center_x, center_y, direction, WIDTH, HEIGHT, lvl.level)
            if moving:
                player_x, player_y = player.move(player_x, player_y, direction, turns_allowed, player_speed)
            score, powerup, power_count, dead_ghost = player.check_target(lvl.level, WIDTH, HEIGHT, score, player_x, center_x, center_y,
                                                                          powerup, power_count, dead_ghost)       

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
                    sdlmixer.Mix_PlayMusic(music_theme, 0)
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
       # SDL_Delay(16)
        
        frameTime = SDL_GetTicks() - frameStart
        #print(frameTime)  # вывод в терминал количества каров в окне
        #if frameDelay > frameTime:
        #    SDL_Delay(frameDelay - frameTime)
    renderer.destroy()
    window.close()
    quit()


if __name__ == "__main__":
    main()