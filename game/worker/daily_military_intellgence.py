
import pyautogui


class DailyMilitaryIntelligenceWorker:
    def __init__(self, game_info):
        self.game_info = game_info

    def go_daily_military_intelligence(self) -> bool:
        try:
            button_location = pyautogui.locateOnScreen(self.game_info.daily_task_img_path, confidence=1)
            button_center = pyautogui.center(button_location)
            pyautogui.click(button_center[0] - 61, button_center[1])
            print("已点击每日軍情按鈕")
            return True
        except pyautogui.ImageNotFoundException:
            return False

