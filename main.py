import os

from components.fragment import Fragment

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame as pg

from utils.game_constants import *
from components.player import Player
from components.platform import Platform
from utils.camera import Camera
from utils.game_vars import GameVars
from utils.misc import generate_platforms, rand_x
import random

# init pygame
pg.init()

# Create the game window
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pg.time.Clock()
pg.display.set_caption("Test")

# init player and camera
player = Player(x=SCREEN_WIDTH // 2 - 30, y=SCREEN_HEIGHT // 2, width=60, height=60, color=Colors.RED)
camera = Camera(init_x=0, follow_rate=CAMERA_SMOOTHNESS)

# make some platforms
platforms = generate_platforms()
fragments = [Fragment(0, 0, 0, 0, 0)]

# Main game loop
while GameVars.run:
    for event in pg.event.get():
        if event.type == pg.QUIT: # handle quit event
            GameVars.run = False

    if GameVars.state in (1, 3): 
        if GameVars.state != 3:
            # get key pressed
            keys = pg.key.get_pressed()

            # calculate all positions
            if player.y - camera.y > SCREEN_HEIGHT:
                player.y_vel = player.x_vel = 0
                player.x = SCREEN_WIDTH // 2 - player.width // 2
                player.y = SCREEN_HEIGHT // 2
                platforms = generate_platforms()

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
                platform.additional_movement(player)

            camera.follow_player(player, disable_horizontal=True)

        # render game
        screen.fill(Colors.WHITE) # clear previous render

        for platform in platforms:
            platform.draw_self(surface=screen, camera=camera)

        GameVars.state != 3 and player.draw_self(surface=screen, camera=camera)
    elif GameVars.state == 2:
        fragments = [
            Fragment(
                x=player.x + i % 4,
                y=player.y + i // 4,
                width=player.width // 4,
                height=player.height // 4,
                color=Colors.GRAY
            ) for i in range(16)
        ]
        GameVars.state = 3
    if GameVars.state == 3:
        for fragment in fragments:
            fragment.experience_gravity()
            fragment.move_horizontal(0, 0)
            fragment.draw_self(surface=screen, camera=camera)


    pg.display.flip()

    clock.tick(60) # limit fps to 60

pg.quit()
