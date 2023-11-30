import pygame as pg
from math import pi

from utils.game_constants import SCREEN_WIDTH, Colors
from .component import Component

class Player(Component):

    x_acc = 2
    y_acc = 0.5
    vel_limit = 15

    def __init__(self, x, y, width, height, color):
        self.x_vel = 0
        self.y_vel = 0
        self.jump_height = 15
        super().__init__(x, y, width, height, color)

    def draw_self(self, surface, camera):
        super().draw_self(surface, camera)
        pg.draw.circle(surface, Colors.WHITE, (self.x + camera.x + self.width // 5, self.y - camera.y + self.height // 3), 5)
        pg.draw.circle(surface, Colors.WHITE, (self.x + camera.x + self.width * 4 // 5, self.y - camera.y + self.height // 3), 5)
        rect = pg.Rect(self.x + camera.x + self.width // 4, self.y - camera.y + 35, self.width // 2, 5)
        pg.draw.rect(surface, Colors.WHITE, rect)

    def experience_gravity(self):
        self.y_vel += self.__class__.y_acc
        self.y += self.y_vel

    def experience_horizontal_slow_down(self):
        self.x_vel *= 0.8

    def move_horizontal(self, left_impulse, right_impulse, wrap=True):
        left_impulse = -left_impulse
        self.x_vel += self.__class__.x_acc * (left_impulse + right_impulse)
        if abs(self.x_vel) > self.__class__.vel_limit:
            self.x_vel = self.x_vel * self.__class__.vel_limit / abs(self.x_vel)
        self.x += self.x_vel
        if wrap:
            if self.x > SCREEN_WIDTH:
                self.x -= SCREEN_WIDTH
            elif self.x + self.width < 0:
                self.x += SCREEN_WIDTH

    def jump(self):
        self.y_vel = -self.jump_height

