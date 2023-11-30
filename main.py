import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame as pg

from utils.game_constants import *
from components.player import Player
from components.platform import Platform
from utils.camera import Camera
from utils.game_vars import GameVars
import random
import time

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

#This defines the path to the title logo (format from ChatGPT)
title_image_path = os.path.join(os.path.dirname(__file__), 'images/Jumps_Logo.png')  ##Derived from ChatGPT, the image was generated with AI
title_image = pg.image.load(title_image_path) 
title_rect = title_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

#Defines path to game over screen
game_over_image_path = os.path.join(os.path.dirname(__file__), 'images/Game_Over.jpg')  ##Derived from ChatGPT, the image was generated with AI
game_over_image = pg.image.load(game_over_image_path)
game_over_image = pg.transform.scale(game_over_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
game_over_rect = game_over_image.get_rect()

# Set the font for the menu options
menu_font = pg.font.Font(None, 36)

def show_title_screen():
    screen.blit(title_image, title_rect)
    pg.display.flip()
    time.sleep(2)  # Show the title for 2 seconds

    fade_out_duration = 1.0
    fade_out_frames = int(fade_out_duration * 60)
    alpha_step = 255 / fade_out_frames

    for frame in range(fade_out_frames):
        title_image.set_alpha(max(0, int(255 - frame * alpha_step)))
        screen.fill(Colors.BLACK)
        screen.blit(title_image, title_rect)
        pg.display.flip()
        pg.time.delay(int(1000 / 60))

# New function to show game over screen
def game_over_screen():
    screen.blit(game_over_image, game_over_rect)
    pg.display.flip()
    time.sleep(2)  # Show the game over screen for 3 seconds

    fade_out_duration = 1.5
    fade_out_frames = int(fade_out_duration * 60)
    alpha_step = 255 / fade_out_frames

    for frame in range(fade_out_frames):
        game_over_image.set_alpha(max(0, int(255 - frame * alpha_step)))
        screen.fill(Colors.BLACK)
        screen.blit(game_over_image, game_over_rect)
        pg.display.flip()
        pg.time.delay(int(1000 / 60))


#Menu screen definition
def show_menu_screen():
    menu_options = ["Start Game", "Highscores", "Quit"]
    selected_option = 0

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    selected_option = (selected_option - 1) % len(menu_options)
                elif event.key == pg.K_DOWN:
                    selected_option = (selected_option + 1) % len(menu_options)
                elif event.key == pg.K_RETURN:
                    if selected_option == 0:
                        return True  # Start game
                    elif selected_option == 1:
                        print("Highscores")  # Replace with highscore logic
                    elif selected_option == 2:
                        return False  # Quit program

        screen.fill(Colors.WHITE)

        for i, option in enumerate(menu_options):
            color = Colors.BLACK if i == selected_option else Colors.GRAY
            text = menu_font.render(option, True, color)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + i * 40))
            screen.blit(text, text_rect)

        pg.display.flip()
        clock.tick(60)

def new_game():
    #resets player position
    player.x = SCREEN_WIDTH // 2
    player.y = SCREEN_HEIGHT // 2
    player.y_vel = 0

    #Reset platforms
    global platforms
    platforms = [
        Platform(
            x=rand_x(),
            y=y,
            width=60,
            height=20,
            color=Colors.BLACK
        ) for y in range(0, SCREEN_HEIGHT + PLATFORM_OFFSCREEN_BUFFER, PLATFORM_SPACING)
    ]


    #guaranteed platform below player every new game
    start_platform = Platform(
        x=SCREEN_WIDTH // 2,  # Adjust the x-position as needed
        y=(SCREEN_WIDTH // 2) + 2,  # Ensure the platform is below the player
        width=60,
        height=20,
        color=Colors.BLACK
    )
    platforms.append(start_platform)
    
##game start
def game_loop():
    
    while GameVars.run:
        # get key pressed
        keys = pg.key.get_pressed()

        # calculate all positions

        if player.y - camera.y > SCREEN_HEIGHT:
            player.y = player.y_vel = player.x = player.x_vel = 0
            game_over_screen()   #Execute game over screen
            time.sleep(1)
            break
            
            
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

        for event in pg.event.get():
            if event.type == pg.QUIT:
                GameVars.run = False
        
        pg.display.flip()

        clock.tick(60) # limit fps to 60


show_title_screen()


# Main game loop

while GameVars.run:
    for event in pg.event.get():
        if event.type == pg.QUIT: # handle quit event
            GameVars.run = False

    if not show_menu_screen():
        break

    if GameVars.run:
        new_game()
        GameVars.run = True
        game_loop()

pg.quit()
