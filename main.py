import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame as pg

from utils.game_constants import *
from components.player import Player
from components.fragment import Fragment
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
pg.display.set_caption("Jason Jumps")

# init player and camera
player = Player(x=SCREEN_WIDTH // 2 - 30, y=SCREEN_HEIGHT // 2, width=60, height=60, color=Colors.GRAY)
camera = Camera(init_x=0, follow_rate=CAMERA_SMOOTHNESS)

# init fonts and sounds and background image
font_path = os.path.join(os.getcwd(), "assets", "fonts", "kongtext", "kongtext.ttf")
font = pg.font.Font(font_path, 30)
font2 = pg.font.Font(font_path, 20)
sounds = {
    "jump": pg.mixer.Sound(os.path.join(os.getcwd(), "assets", "sounds", "jump.wav")),
    "game_over": pg.mixer.Sound(os.path.join(os.getcwd(), "assets", "sounds", "game_over.wav"))
}
background_path = os.path.join(os.getcwd(), "assets", "images", "background.jpg")
background = pg.image.load(background_path).convert()


# make some platforms
platforms = generate_platforms()
fragments = []

# Main game loop
# Game states:
# 1 - main game
# 2 - process fragments for game over animation
# 3 - game over animation
# 4 - 
while GameVars.run:

    for event in pg.event.get():
        if event.type == pg.QUIT: # handle quit event
            GameVars.run = False

    if GameVars.sound:
        sounds[GameVars.sound].play()
        GameVars.sound = None

    if GameVars.state in (1, 3): 

        # ALL POSITION CALCULATIONS
        if GameVars.state == 1:
            # get key pressed
            keys = pg.key.get_pressed()

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
        else:
            for fragment in fragments:
                fragment.experience_gravity()
                fragment.move_horizontal(0, 0, wrap=False)
            GameVars.wait += 1
            if GameVars.wait > 120: # after 2 seconds, reset
                player.y_vel = player.x_vel = 0
                player.x = SCREEN_WIDTH // 2 - player.width // 2
                player.y = SCREEN_HEIGHT // 2
                platforms = generate_platforms()
                camera.follow_player(player, disable_horizontal=True, immediate=True)
                GameVars.state = 1
                GameVars.highscore = max(GameVars.highscore, GameVars.score)
                GameVars.score = 0

        # ALL RENDERING
        screen.blit(background, (0,0)) # clear previous render
        for platform in platforms:
            platform.draw_self(surface=screen, camera=camera)
        if GameVars.state == 3:
            for fragment in fragments:
                fragment.draw_self(surface=screen, camera=camera)
        else:
            player.draw_self(surface=screen, camera=camera)

        GameVars.score = max(GameVars.score, int(-player.y + SCREEN_HEIGHT // 2))
        score_surf = font.render(f"Score-{GameVars.score}", False, Colors.WHITE)
        score_rect = score_surf.get_rect()
        score_rect.topleft = (10, 10)
        highscorescore_surf = font2.render(f"Highscore-{GameVars.highscore}", False, Colors.GREEN)
        highscore_rect = highscorescore_surf.get_rect()
        highscore_rect.topleft = (13, 40)
        screen.blit(score_surf, score_rect)
        screen.blit(highscorescore_surf, highscore_rect)

    elif GameVars.state == 2:
        fragments = [
            Fragment(
                x=player.x + i % 4,
                y=player.y + i // 4,
                width=player.width // 4,
                height=player.height // 4,
                color=Colors.ORANGE
            ) for i in range(16)
        ]
        GameVars.state = 3
        GameVars.wait = 0


    pg.display.flip()

    clock.tick(60) # limit fps to 60

pg.quit()
