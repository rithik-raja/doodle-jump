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
            if self.platform_type == 1:
                y_diff = player.get_rect(y_offset=-player.y_vel).bottom - self.get_rect().top # move one y_vel frame back and check if colliding from the top
                if y_diff <= 0:
                    y_intersection = player.get_rect().bottom - self.get_rect().top
                    player.y -= y_intersection
                    player.jump()
                    GameVars.sound = "jump"
            elif self.platform_type == 2:
                GameVars.state = 2
                GameVars.sound = "game_over"

    def draw_self(self, surface, camera):
        if self.platform_type == 1:  # normal platform
            platform_image = pg.image.load('assets/images/platform.png').convert_alpha()
            platform_rect = pg.Rect(self.x + camera.x, self.y - camera.y, self.width, self.height)
            surface.blit(platform_image, platform_rect.topleft)
            
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

        elif self.platform_type == 3: #platform below spikes
            return super().draw_self(surface, camera)

    def recycle_top(self, player, limit, offset, x):
        if self.platform_type == 1: # unique behavior for spikes
            return super().recycle_top(player, limit, offset, x)
        
    def additional_movement(self, player):
        if self.platform_type in (2, 3): # unique behavior for spikes and the block below them
            target = player.y + SCREEN_HEIGHT // 2 + (40 if self.platform_type == 3 else 0)
            if target < self.y - 2:
                self.y += (target - self.y) / 10
            else:
                self.y -= 1.5
        
