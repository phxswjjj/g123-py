
from datetime import datetime, timedelta
import logging
import time
import inject
import pyautogui

from game.game_info import GameInfo


class AbnormalWorker:
    @inject.params(game_info=GameInfo, logger=logging.Logger)
    def __init__(self, game_info: GameInfo, logger: logging.Logger):
        self.game_info = game_info
        self.logger = logger
        if self.game_info.is_immediate_run:
            self.next_time_to_work = datetime.now()
        else:
            self.set_next_time_to_work()

    def set_next_time_to_work(self):
        self.next_time_to_work = datetime.now() + timedelta(minutes=1)

    def is_time_to_work(self) -> bool:
        return datetime.now() > self.next_time_to_work
    
    def is_disconnection(self) -> bool:
        try:
            pos = pyautogui.locateOnScreen(self.game_info.disconnection_img_path, confidence=0.9)
            button_center = pyautogui.center(pos)
            self.logger.info("連線中斷")
            return True
        except pyautogui.ImageNotFoundException:
            return False
    
    def reconnection(self) -> bool:
        if not self.is_time_to_work():
            return False

        if not self.game_info.is_in_game():
            return False
        
        if not self.is_disconnection():
            return False
        
        # 確定
        pyautogui.click((959, 660))
        time.sleep(1)

        return True