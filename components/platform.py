import pygame as pg

from .component import Component

class Platform(Component):

    def __init__(self, x, y, width, height, color, platform_type=1):
        self.platform_type = platform_type
        super().__init__(x, y, width, height, color)

    def collide(self, player):
        if self.get_rect().colliderect(player.get_rect()): # is colliding?
            y_diff = player.get_rect(y_offset=-player.y_vel).bottom - self.get_rect().top # move one y_vel frame back and check if colliding from the top
            if y_diff <= 0:
                y_intersection = player.get_rect().bottom - self.get_rect().top
                player.y -= y_intersection
                player.jump()
