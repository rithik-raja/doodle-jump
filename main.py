import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame as pg

from utils.game_constants import *
from components.player import Player
from components.platform import Platform
from utils.camera import Camera
from utils.game_vars import GameVars
import random

# init pygame
pg.init()

# Create the game window
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pg.time.Clock()
pg.display.set_caption("Test")

# init player and camera
player = Player(x=SCREEN_WIDTH // 2, y=SCREEN_HEIGHT // 2, width=60, height=60, color=Colors.RED)
camera = Camera(init_x=0, follow_rate=CAMERA_SMOOTHNESS)

rand_x = lambda: random.randint(0, SCREEN_WIDTH)

# make some platforms
platforms = [
    Platform(
        x=rand_x(),
        y=y,
        width=60,
        height=20,
        color=Colors.BLACK
    ) for y in range(0, SCREEN_HEIGHT + PLATFORM_OFFSCREEN_BUFFER, PLATFORM_SPACING)
]

# Main game loop

while GameVars.run:
    for event in pg.event.get():
        if event.type == pg.QUIT: # handle quit event
            GameVars.run = False

    # get key pressed
    keys = pg.key.get_pressed()

    # calculate all positions

    if player.y - camera.y > SCREEN_HEIGHT:
        player.y = player.y_vel = player.x = player.x_vel = 0

    player.experience_gravity()
    player.experience_horizontal_slow_down()
    player.move_horizontal(keys[pg.K_LEFT], keys[pg.K_RIGHT])

    for platform in platforms:
        platform.collide(player)
        platform.recycle_top(
            player=player,
            limit=SCREEN_HEIGHT // 2 + PLATFORM_OFFSCREEN_BUFFER,
            offset=SCREEN_HEIGHT + PLATFORM_OFFSCREEN_BUFFER,
            x=rand_x()
        )

    camera.follow_player(player, disable_horizontal=True)

    # render game

    screen.fill(Colors.WHITE) # clear previous render

    for platform in platforms:
        platform.draw_self(surface=screen, camera=camera)

    player.draw_self(surface=screen, camera=camera)

    pg.display.flip()

    clock.tick(60) # limit fps to 60

pg.quit()
