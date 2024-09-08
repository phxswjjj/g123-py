from utils.window_utils import capture_screenshot, bring_window_to_front, is_in_game

# 建立 game info class
class GameInfo:
    def __init__(self):
        self.title = "鮮豔軍團 | 開始遊戲 - G123 - Google Chrome"
        self.img_root = ".\imgs"
        self.img_tmp = ".\imgs_tmp"
        self.back_home_img_path = rf"{self.img_root}\back_home.png"

    def create_screenshot_function(self):
        return lambda e: capture_screenshot(e, self.img_tmp)

    def bring_window_to_front(self):
        bring_window_to_front(self.title)

    def is_in_game(self):
        return is_in_game(self.title)