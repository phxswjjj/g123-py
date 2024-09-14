
import logging
import inject
import pyautogui

from game.game_info import GameInfo


class DailyMilitaryIntelligenceWorker:
    @inject.params(game_info=GameInfo, logger=logging.Logger)
    def __init__(self, game_info: GameInfo, logger: logging.Logger):
        self.game_info = game_info
        self.logger = logger

    def go_daily_military_intelligence(self) -> bool:
        try:
            button_location = pyautogui.locateOnScreen(self.game_info.daily_task_img_path, confidence=0.9)
            button_center = pyautogui.center(button_location)
            pyautogui.click(button_center[0] - 61, button_center[1])
            self.logger.info("已点击每日軍情按鈕")
            return True
        except pyautogui.ImageNotFoundException:
            return False

