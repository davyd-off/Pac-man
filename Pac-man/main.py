from sdl2 import *
from sdl2.ext import *
import sdl2.sdlmixer as sdlmixer
from board_1 import boards
from button import ImageButton


sdlmixer.Mix_OpenAudio(44100, sdlmixer.MIX_DEFAULT_FORMAT, 2, 1024)

WIDTH = 900
HEIGHT = 950

RESOURCES_IMG = Resources(__file__, "./Source/Images")

level = boards


def draw_board(renderer):
    """
    Рисование карты.
    tx[k] - текстура картинки.
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
            if level[i][j] == 2:
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





def main():
    init()

    window = Window("Pac-man", (WIDTH, HEIGHT), flags=SDL_WINDOW_RESIZABLE)
    window.show()

    render_flags = (SDL_RENDERER_ACCELERATED | SDL_RENDERER_PRESENTVSYNC)
    renderer = Renderer(window, -1, flags=render_flags)
    set_texture_scale_quality(method="best")

    # Экземпляры класса кнопок (button)
    work_button = ImageButton(window, renderer, WIDTH, HEIGHT)
    work_button.render_button()

    game_pause = True
    running = True
    while running:
        events = get_events()
            # обработка событий
        for event in events:
            # сюда пишутся все if
            if event.type == SDL_QUIT:
                running = False
                break
            
            if event.type == SDL_MOUSEBUTTONDOWN:   # нажатие кнопок меню
                x, y = event.button.x, event.button.y
                if game_pause == True and WIDTH // 4 <= x <= 618 and (HEIGHT // 4) + 96 <= y <= (HEIGHT // 4) + 144:
                    game_pause = False
                    work_button.play_sound()
                    work_button.render_clean()
                    print("Start Game button pressed")
                if game_pause == True and WIDTH // 4 <= x <= 762 and (HEIGHT // 2) - 48 <= y <= (HEIGHT // 2):
                    work_button.play_sound()
                    print("Leaderboard button pressed")
                if game_pause == True and WIDTH // 4 <= x <= 438 and (HEIGHT // 2) + 48 <= y <= (HEIGHT // 2) + 96:
                    work_button.play_sound()
                    print("Help button pressed")
                if game_pause == True and WIDTH // 4 <= x <= 402 and (HEIGHT // 2) + 144 <= y <= (HEIGHT // 2) + 192:
                    work_button.play_sound()
                    running = False
                    break
            if game_pause == False:      
                music = sdlmixer.Mix_LoadMUS(b"Source/Sound/A Touch Of Class - Around the World.mp3")               
                draw_board(renderer)
                sdlmixer.Mix_PlayMusic(music, 1)
                

                

        renderer.present()           
    quit()


if __name__ == "__main__":
    main()