import pygame as pg

from .component import Component

class Player(Component):

    x_acc = 2
    y_acc = 0.5
    vel_limit = 15

    def __init__(self, x, y, width, height, color):
        self.x_vel = 0
        self.y_vel = 0
        super().__init__(x, y, width, height, color)

    def experience_gravity(self):
        self.y_vel += Player.y_acc
        self.y += self.y_vel

    def experience_horizontal_slow_down(self):
        self.x_vel *= 0.8

    def move_horizontal(self, left_impulse, right_impulse):
        left_impulse = -left_impulse
        self.x_vel += Player.x_acc * (left_impulse + right_impulse)
        if abs(self.x_vel) > Player.vel_limit:
            self.x_vel = self.x_vel * Player.vel_limit / abs(self.x_vel)
        self.x += self.x_vel

    def jump(self):
        self.y_vel = -13

