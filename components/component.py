import pygame as pg

class Component:

    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
    
    def get_rect(self, x_offset=0, y_offset=0):
        return pg.Rect(self.x + x_offset, self.y + y_offset, self.width, self.height)
    
    def draw_self(self, surface, camera):
        pg.draw.rect(surface, self.color, self.get_rect(x_offset=-camera.x, y_offset=-camera.y))

    def recycle_top(self, player, limit, offset, x):
        if (self.y - player.y) > limit:
            self.y -= offset
            self.x = x
