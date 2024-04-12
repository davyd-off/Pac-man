from sdl2 import *
from sdl2.ext import *
import sdl2.sdlmixer as sdlmixer

class ImageButton:
    def __init__(self, window, renderer, w, h):
        self.window = window
        self.renderer = renderer
        self.w = w
        self.h = h

        sdlmixer.Mix_OpenAudio(44100, sdlmixer.MIX_DEFAULT_FORMAT, 2, 1024)
        self.music = sdlmixer.Mix_LoadMUS(b"Source/Sound/click.mp3")

        self.text_color = Color(127, 255, 212)
        self.bg_color1 = Color(0, 0, 128)
        self.bg_color2 = Color(0, 0, 0)
        self.factory = SpriteFactory(TEXTURE, renderer=renderer)
        self.font_manager = FontManager(font_path="./Source/Font/better-vcr-5.4.ttf", size=48, color=self.text_color, bg_color=self.bg_color1)
        
        # кнопки галвного меню
        self.buttons = {
            "Начать игру": self.factory.from_text("Начать игру", fontmanager=self.font_manager),
            "Помощь": self.factory.from_text("Помощь", fontmanager=self.font_manager),
            "Выход": self.factory.from_text("Выход", fontmanager=self.font_manager),
        }
        self.button_positions = {
            "Начать игру": (w // 4, (h // 4) + 96),
            "Помощь": (w // 4, (h // 2) - 48),
            "Выход": (w // 4, (h // 2) + 48),
        }

        # кнопка возврата
        self.button_back = {"Назад": self.factory.from_text("Назад", fontmanager=self.font_manager)}
        self.button_pos_back = {"Назад": (350, h - 96)}

        # кнопки выбора карты
        self.buttons_select_level = {
            "1": self.factory.from_text("1", fontmanager=self.font_manager),
            "2": self.factory.from_text("2", fontmanager=self.font_manager),
            "3": self.factory.from_text("3", fontmanager=self.font_manager),
        }
        self.button_pos_select_level = {
            "1": (800, 272),
            "2": (800, 440),
            "3": (800, 607),
        }       
                    
    def play_sound(self):
        sdlmixer.Mix_PlayMusic(self.music, 0)
    
    def show_menu(self):
        for button, texture in self.buttons.items():
            self.renderer.copy(texture, dstrect=self.button_positions[button])

    def show_help(self):
        self.background = load_image((f'Source/Images/help_screen.png'))
        self.tx_background = Texture(self.renderer, self.background)
        self.renderer.copy(self.tx_background, dstrect=(0, 0))
        for button, texture in self.button_back.items():
            self.renderer.copy(texture, dstrect=self.button_pos_back[button])

    def show_select(self):
        self.background = load_image((f'Source/Images/select_screen.png'))
        self.tx_background = Texture(self.renderer, self.background)
        self.renderer.copy(self.tx_background, dstrect=(0, 0))
        for button, texture in self.button_back.items():
            self.renderer.copy(texture, dstrect=self.button_pos_back[button])
        for button, texture in self.buttons_select_level.items():
            self.renderer.copy(texture, dstrect=self.button_pos_select_level[button])

    def render_clean(self):
        self.renderer.clear(self.bg_color2)
