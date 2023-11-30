import random
from components.platform import Platform
from utils.game_constants import PLATFORM_OFFSCREEN_BUFFER, PLATFORM_SPACING, SCREEN_HEIGHT, SCREEN_WIDTH, Colors

rand_x = lambda: random.randint(0, SCREEN_WIDTH)

def generate_platforms():
    width = 60
    height = 20
    return [ # random platforms
        Platform(
            x=rand_x(),
            y=y,
            width=width,
            height=height,
            color=Colors.BLACK
        ) for y in range(0, SCREEN_HEIGHT + PLATFORM_OFFSCREEN_BUFFER, PLATFORM_SPACING)
    ] + [ # guaranteed platform below player
        Platform(
            x=SCREEN_WIDTH // 2 - (width + 20) // 2,
            y=SCREEN_HEIGHT // 2 + 100,
            width=width + 20,
            height=height,
            color=Colors.BLACK
        )
    ] + [
        Platform(
            x=i,
            y=SCREEN_HEIGHT,
            width=width,
            height=height * 2,
            color=Colors.RED,
            platform_type=2
        ) for i in range(0, SCREEN_WIDTH, width)
    ]