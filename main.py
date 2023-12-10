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
import time
import numpy as np

# init pygame
pg.init()

# Create the game window
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pg.time.Clock()
pg.display.set_caption("Jason Jumps")

# initialize player and camera
player = Player(x=SCREEN_WIDTH // 2 - 30, y=SCREEN_HEIGHT // 2, width=60, height=60, color=Colors.GRAY)
camera = Camera(init_x=0, follow_rate=CAMERA_SMOOTHNESS)

# initialize fonts and sounds and background image
menu_font = pg.font.Font(None, 50)
font_path = os.path.join(os.getcwd(), "assets", "fonts", "kongtext", "kongtext.ttf")
font = pg.font.Font(font_path, 30)
font2 = pg.font.Font(font_path, 20)
sounds = {
    "jump": pg.mixer.Sound(os.path.join(os.getcwd(), "assets", "sounds", "jump.wav")),
    "game_over": pg.mixer.Sound(os.path.join(os.getcwd(), "assets", "sounds", "game_over.wav"))
}

# initialize background image
background_path = os.path.join(os.getcwd(), "assets", "images", "background.jpg")
background = pg.image.load(background_path).convert()

# initialize title screen image and variables
title_flash_duration = 60  # number of frames for the title screen flash
menu_duration = 180  # number of frames for the menu screen
current_frame = 0  # current frame count
title_image = pg.image.load(os.path.join(os.getcwd(), "assets", "images", "Jumps_Logo.png")).convert_alpha()
title_rect = title_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)) # this centers the image rectangle

# initialize menu screen image and path
menu_background_path = os.path.join(os.getcwd(), "assets", "images", "menu_image.jpg")
menu_background = pg.image.load(menu_background_path).convert()

# initialize menu title image and path
menu_title_path = os.path.join(os.getcwd(), "assets", "images", "menu_title.png")
menu_title = pg.image.load(menu_title_path).convert()

# initialize game over screen image and path
game_over_image = pg.image.load(os.path.join(os.getcwd(), "assets", "images", "Game_Over.jpg")).convert_alpha()
game_over_image = pg.transform.scale(game_over_image, (SCREEN_WIDTH, SCREEN_HEIGHT)) # this scales the image to the size of the game window
game_over_rect = game_over_image.get_rect()

# initialize the path to the csv containing the scoreboard 
scoreboard_path = os.path.join(os.getcwd(), "assets", "highscores", "scoreboard.csv")

# make some platforms
platforms = generate_platforms()
fragments = []

# this defines a function which writes the scores obtained to a csv file in order to save it across game instances
def save_highscore(score):
    try:
        highscores = np.loadtxt(scoreboard_path, delimiter=',')
    except FileNotFoundError:
        highscores = np.array([]) # if the csv file does not exist, the array is initialized with 0 elements

    highscores = np.append(highscores, score) # the current score is appended to the highscores array
    np.savetxt(scoreboard_path, highscores, fmt='%d', delimiter=',') # this saves the data from the array to the csv file

#Set the state to 0 to start with the loading screen
GameVars.state = 0

# Main game loop
# Game states:
# 0 - loading screen
# 1 - main game
# 2 - process fragments for game over animation
# 3 - game over animation
# 4 - main menu state
# 5 - game over animation
# 6 - scoreboard display

while GameVars.run:

    for event in pg.event.get():
        if event.type == pg.QUIT: # handles the quit event
            GameVars.run = False # this stops the game loop

    if GameVars.sound: # handles the soudns in the game
        sounds[GameVars.sound].play()
        GameVars.sound = None

    # State 0 is the loading screen
    if GameVars.state == 0:
        screen.blit(title_image, title_rect)
        pg.display.flip()
        time.sleep(2)  # Show the title for 2 seconds

        fade_out_duration = 1.0
        fade_out_frames = int(fade_out_duration * 60)
        alpha_step = 255 / fade_out_frames

        for frame in range(fade_out_frames): # fade out effect from title screen to menu screen
            title_image.set_alpha(max(0, int(255 - frame * alpha_step)))
            screen.fill(Colors.BLACK)
            screen.blit(title_image, title_rect)
            pg.display.flip()
            pg.time.delay(int(1000 / 60))

        GameVars.state = 4  # Transition to the menu state

    # State 4 is the menu screen
    elif GameVars.state == 4:
        menu_options = ["Start Game", "Highscores", "Quit"] # These are the three options in the menu
        selected_option = 0
        show_menu = True

        while show_menu:
            for event in pg.event.get():
                if event.type == pg.QUIT: # handles if the game is exited
                    GameVars.run = False
                    show_menu = False
                elif event.type == pg.KEYDOWN: # this handles the moving up and down through the menu options
                    if event.key == pg.K_UP:
                        selected_option = (selected_option - 1) % len(menu_options)
                    elif event.key == pg.K_DOWN:
                        selected_option = (selected_option + 1) % len(menu_options)
                    elif event.key == pg.K_RETURN:
                        if selected_option == 0: # Option 0 starts the main game loop
                            GameVars.state = 1
                            show_menu = False
                        elif selected_option == 1: # Option 1 goes to the scoreboard menu
                            GameVars.state = 6  
                            show_menu = False 
                        elif selected_option == 2: # Option 2 quits the game
                            GameVars.run = False
                            show_menu = False
                        
            screen.blit(menu_background, (0, 0))   # renders the menu_bakcground image
            screen.blit(menu_title, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 3 - 50)) # renders the menu_title image

            for i, option in enumerate(menu_options):   # this goes through the elements in menu_options and renders the text on the screen in order
                color = Colors.BLACK if i == selected_option else Colors.WHITE
                text = menu_font.render(option, True, color)
                text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + i * 45))
                screen.blit(text, text_rect)

            pg.display.flip()
            clock.tick(60)

    # State 5 is the game over animation
    elif GameVars.state == 5:
        for GameVars.wait in (0,360): # this renders the game over image
            screen.fill(Colors.BLACK)
            screen.blit(game_over_image, game_over_rect)
            GameVars.wait += 1

        # these variables fascilitate the fade out of the image
        fade_out_duration = 1.5
        fade_out_frames = int(fade_out_duration * 60)
        alpha_step = 255 / fade_out_frames

        for frame in range(fade_out_frames): # this loop renders the fade out as it transitions to the next game state
            game_over_image.set_alpha(max(0, int(255 - frame * alpha_step)))
            screen.fill(Colors.BLACK)
            screen.blit(game_over_image, game_over_rect)
            pg.display.flip()
            pg.time.delay(int(1000 / 60))

        GameVars.state = 4 # transitions back to the main menu screen
        GameVars.highscore = max(GameVars.highscore, GameVars.score) # if the current score is highesr than the current best, it overrides the current best score with the new best score
        GameVars.score = 0 # resets the current score value back to 0
        screen.fill(Colors.BLACK)

    # State 6 is the highscore screen
    elif GameVars.state == 6:
        try:
            highscores = np.loadtxt(scoreboard_path, delimiter=',')
        except FileNotFoundError:
            highscores = np.array([]) # this try except initializes the highscores array with no elements if the csv file has not been created yet

        highscores = np.sort(np.atleast_1d(highscores))[::-1] # this sorts the highscores by descending order
        show_scoreboard = True

        while show_scoreboard:
            for event in pg.event.get(): # this handles the game being quit while the scoreboard is shown
                if event.type == pg.QUIT:
                    GameVars.run = False
                    show_scoreboard = False
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN: # if the return/enter key is pressed, the game will revert to the main menu 
                        GameVars.state = 4 # transitions to the main menun
                        show_scoreboard = False

            # rendering of the title text on the scoreboard screen
            screen.blit(menu_background, (0, 0))
            scoreboard_text = "Top 5 Highscores"
            scoreboard_render = menu_font.render(scoreboard_text, True, Colors.WHITE)
            scoreboard_rect = scoreboard_render.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 6))
            screen.blit(scoreboard_render, scoreboard_rect)

            # goes through the top 5 scores stored in teh highscores array and displays them. If there are less than 5 scores, it displays however many there are
            for i, score in enumerate(highscores[:min(5, highscores.size)]): 
                score_text = f"{i + 1}. {score}"
                text = menu_font.render(score_text, True, Colors.BLACK)
                text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + i * 40))
                screen.blit(text, text_rect)

            # renders instructions o how to return to main menu
            back_text = "Press Enter for Main Menu"
            back_render = menu_font.render(back_text, True, Colors.WHITE)
            back_rect = back_render.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
            screen.blit(back_render, back_rect)

            pg.display.flip()
            clock.tick(60)
        
    elif GameVars.state in (1, 2, 3): 
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

        if GameVars.state == 2:
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
        

        elif GameVars.state == 3:
            for fragment in fragments:
                fragment.experience_gravity()
                fragment.move_horizontal(0, 0, wrap=False)
            GameVars.wait += 1
            if GameVars.wait > 90: # after 2 seconds, reset
                player.y_vel = player.x_vel = 0
                player.x = SCREEN_WIDTH // 2 - player.width // 2
                player.y = SCREEN_HEIGHT // 2
                platforms = generate_platforms()
                camera.follow_player(player, disable_horizontal=True, immediate=True)
                GameVars.state = 5
                save_highscore(GameVars.score)
                GameVars.highscore = max(GameVars.highscore, GameVars.score)
                GameVars.score = 0
                screen.fill(Colors.BLACK)

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
        highscorescore_surf = font2.render(f"Current Best-{GameVars.highscore}", False, Colors.GREEN)
        highscore_rect = highscorescore_surf.get_rect()
        highscore_rect.topleft = (13, 40)
        screen.blit(score_surf, score_rect)
        screen.blit(highscorescore_surf, highscore_rect)


    pg.display.flip()

    clock.tick(60) # limit fps to 60

pg.quit()
