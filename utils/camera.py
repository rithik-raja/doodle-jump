from utils.game_constants import SCREEN_WIDTH, SCREEN_HEIGHT

class Camera:

    def __init__(self, init_x=SCREEN_WIDTH // 2, init_y=SCREEN_HEIGHT // 2, follow_rate=20):
        self.x = self.x_temp = self.x_offset = init_x
        self.y = self.y_temp = self.y_offset = init_y
        self.follow_rate = follow_rate

    def follow_player(self, player, disable_horizontal=False, disable_vertical=False, immediate=False):
        if not disable_horizontal:
            self.x_temp += (player.x - self.x_temp) / (1 if immediate else self.follow_rate)
            self.x = self.x_temp - self.x_offset
        if not disable_vertical:
            self.y_temp += (player.y - self.y_temp) / (1 if immediate else self.follow_rate)
            self.y = self.y_temp - self.y_offset