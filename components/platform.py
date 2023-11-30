import pygame as pg

from utils.game_constants import SCREEN_HEIGHT
from utils.game_vars import GameVars

from .component import Component

class Platform(Component):

    def __init__(self, x, y, width, height, color, platform_type=1):
        self.platform_type = platform_type
        super().__init__(x, y, width, height, color)

    def collide(self, player):
        if self.get_rect().colliderect(player.get_rect()): # is colliding?
            if self.platform_type != 2:
                y_diff = player.get_rect(y_offset=-player.y_vel).bottom - self.get_rect().top # move one y_vel frame back and check if colliding from the top
                if y_diff <= 0:
                    y_intersection = player.get_rect().bottom - self.get_rect().top
                    player.y -= y_intersection
                    player.jump()
            else:
                GameVars.state = 2

    def draw_self(self, surface, camera):
        if self.platform_type == 1: # normal platform
            return super().draw_self(surface, camera)
        elif self.platform_type == 2: # spike
            x = self.x + camera.x
            y = self.y - camera.y
            pg.draw.polygon(
                surface,
                self.color,
                [
                    (x + self.width // 2, y),
                    (x, y + self.height),
                    (x + self.width, y + self.height)
                ]
            )

    def recycle_top(self, player, limit, offset, x):
        if self.platform_type != 2: # unique behavior for spikes
            return super().recycle_top(player, limit, offset, x)
        
    def additional_movement(self, player):
        if self.platform_type == 2: # unique behavior for spikes
            self.y = min(player.y + SCREEN_HEIGHT // 2, self.y - 2)
        