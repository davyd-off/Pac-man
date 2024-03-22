from sdl2 import *
from sdl2.ext import *


class Ghost:
    def __init__(self, x_coord, y_coord, target, speed, img, direct, dead, box, id, renderer, powerup, dead_ghost, death_ghost_tx, eye_tx):
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
        self.renderer = renderer
        self.powerup = powerup
        self.dead_ghost = dead_ghost
        self.death_ghost_tx = death_ghost_tx
        self.eye_tx = eye_tx
        self.turns, self.in_box = self.check_collisions()
        self.rect = self.draw_ghost()   

    def draw_ghost(self):
        if (not self.powerup and not self.dead) or (self.dead_ghost[self.id] and self.powerup and not self.dead):
            self.renderer.copy(self.img, dstrect=(self.x_pos, self.y_pos))
        elif self.powerup and not self.dead and not self.dead_ghost[self.id]:
            self.renderer.copy(self.death_ghost_tx, dstrect=(self.x_pos, self.y_pos))
        else:
            self.renderer.copy(self.eye_tx, dstrect=(self.x_pos, self.y_pos))
        
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