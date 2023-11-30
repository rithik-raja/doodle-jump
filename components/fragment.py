import random
import pygame as pg

from components.player import Player

class Fragment(Player):

    x_acc = 2
    y_acc = 0.5
    vel_limit = float("inf")

    def __init__(self, x, y, width, height, color):
        super().__init__(x, y, width, height, color)
        self.x_vel = random.randint(-20, 20)
        self.y_vel = random.randint(-20, 5)

    def draw_self(self, surface, camera):
        return super(Player, self).draw_self(surface, camera)

