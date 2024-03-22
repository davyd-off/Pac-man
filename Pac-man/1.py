import sys
from sdl2 import *
from sdl2.ext import *
import sdl2.sdlmixer as sdlmixer
from button import ImageButton
import player
import level as lvl
from ghost import Ghost

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
blinky_tx = load_image(f'Source/Images/blinky.png')
pinky_tx = load_image(f'Source/Images/pinky.png')
inky_tx = load_image(f'Source/Images/inky.png')
clyde_tx = load_image(f'Source/Images/clyde.png')

flicker = False
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
ghost_speed = 2
###############################################

death_ghost_tx = load_image(f'Source/Images/death_ghost.png')
eye_tx = load_image(f'Source/Images/eye.png')

class Ghost:
    def __init__(self, x_coord, y_coord, target, speed, img, direct, dead, box, id, renderer):
        self.x_pos = x_coord
        self.y_pos = y_coord
        self.center_x = self.x_pos + 22
        self.center_y = self.y_pos + 22
        self.target = target
        self.speed = speed
        self.img = img
        self.direction = direct
        self.dead = dead
        self.in_box = box
        self.id = id
        self.turns, self.in_box = self.check_collisions()
        self.rect = self.draw_ghost()

    def draw_ghost(self):
        if (not powerup and not self.dead) or (dead_ghost[self.id] and powerup and not self.dead):
            self.renderer.copy(self.img, dstrect=(self.x_pos, self.y_pos))
        elif powerup and not self.dead and not dead_ghost[self.id]:
            self.renderer.copy(death_ghost_tx, dstrect=(self.x_pos, self.y_pos))
        else:
            self.renderer.copy(eye_tx, dstrect=(self.x_pos, self.y_pos))
        
        ghost_rect = SDL_Rect
        ghost_rect.x = self.center_x - 18
        ghost_rect.y = self.center_y - 18
        ghost_rect.w = 36
        ghost_rect.h = 36
        return ghost_rect
    
    def check_collisions(self):
        self.turns = [False, False, False, False]
        self.in_box = True

        return self.turns, self.in_box

def main():
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

            blinky = Ghost(blinky_x, blinky_y, targets[0], ghost_speed, blinky_tx, blinky_direction, blinky_dead, blinky_box, 0)
            inky = Ghost(inky_x, inky_y, targets[1], ghost_speed, inky_tx, inky_direction, inky_dead, inky_box, 1)
            pinky = Ghost(pinky_x, pinky_y, targets[2], ghost_speed, pinky_tx, pinky_direction, pinky_dead, pinky_box, 2)
            clyde = Ghost(clyde_x, clyde_y, targets[3], ghost_speed, clyde_tx, clyde_direction, clyde_dead, clyde_box, 3)

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