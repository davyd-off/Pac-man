import sdl2.ext
import sdl2.sdlmixer as sdlmixer

class ImageButton:
    def __init__(self, window, renderer, w, h):
        self.window = window
        self.renderer = renderer
        self.w = w
        self.h = h

        sdlmixer.Mix_OpenAudio(44100, sdlmixer.MIX_DEFAULT_FORMAT, 2, 1024)
        self.music = sdlmixer.Mix_LoadMUS(b"Source/Sound/click.mp3")

        self.text_color = sdl2.ext.Color(127, 255, 212)
        self.bg_color1 = sdl2.ext.Color(0, 0, 128)
        self.bg_color2 = sdl2.ext.Color(0, 0, 0)
        self.factory = sdl2.ext.SpriteFactory(sdl2.ext.TEXTURE, renderer=renderer)
        self.font_manager = sdl2.ext.FontManager(font_path="./Source/Font/better-vcr-5.4.ttf", size=48, color=self.text_color, bg_color=self.bg_color1)
        
        self.buttons = {
            "Начать игру": self.factory.from_text("Начать игру", fontmanager=self.font_manager),
            "Таблица лидеров": self.factory.from_text("Таблица лидеров", fontmanager=self.font_manager),
            "Помощь": self.factory.from_text("Помощь", fontmanager=self.font_manager),
            "Выход": self.factory.from_text("Выход", fontmanager=self.font_manager)
        }

      #  self.buttons_pause = {
       #     "Продолжить": self.factory.from_text("Продолжить", fontmanager=self.font_manager),
       #     "Выход": self.factory.from_text("Выход", fontmanager=self.font_manager)
      #  }
        
        self.button_positions = {
            "Начать игру": (w // 4, (h // 4) + 96),
            "Таблица лидеров": (w // 4, (h // 2) - 48),
            "Помощь": (w // 4, (h // 2) + 48),
            "Выход": (w // 4, (h // 2) + 144)
        }

       # self.button_pause_positions = {
       #     "Продолжить": (w // 4, (h // 2) - 48),
       #     "Выход": (w // 4, (h // 2) + 48),
       # }

    def play_sound(self):
        sdlmixer.Mix_PlayMusic(self.music, 0)
    
    def render_button(self):
        for button, texture in self.buttons.items():
            self.renderer.copy(texture, dstrect=self.button_positions[button])
        self.renderer.present()

   # def render_button_pause(self):
   #     for button_pause, texture_pause in self.buttons_pause.items():
   #         self.renderer.copy(texture_pause, dstrect=self.button_pause_positions[button_pause])
   #     self.renderer.present()

    def render_clean(self):
        self.renderer.clear(self.bg_color2)
