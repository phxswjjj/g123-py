
from game.game_info import GameInfo
import pyautogui


class ChangeWorldWorker:
    def __init__(self, game_info: GameInfo):
        self.game_info = game_info

    def go_home_by_click(self):
        try:
            button_location = pyautogui.locateOnScreen(self.game_info.back_home_img_path, confidence=0.8)
        except pyautogui.ImageNotFoundException:
            return False
        
        button_center = pyautogui.center(button_location)
        pyautogui.click(button_center)
        print("已点击返回主页按钮")
        return True

    def go_home(self) -> bool:
        if not self.game_info.is_in_game():
            return False
        
        return self.go_home_by_click()

    