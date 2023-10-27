from utils.game_constants import SCREEN_WIDTH, SCREEN_HEIGHT

class Camera:

    def __init__(self, follow_rate=20):
        self.x = self.x_temp = self.x_offset = SCREEN_WIDTH // 2
        self.y = self.y_temp = self.y_offset = SCREEN_HEIGHT // 2
        self.follow_rate = follow_rate

    def follow_player(self, player):
        self.x_temp += (player.x - self.x_temp) / self.follow_rate
        self.x = self.x_temp - self.x_offset
        self.y_temp += (player.y - self.y_temp) / self.follow_rate
        self.y = self.y_temp - self.y_offset