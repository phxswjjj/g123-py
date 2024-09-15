
from datetime import datetime, timedelta
import logging
import time

import inject
import pyautogui
from game.game_info import GameInfo


class AllianceHelpWorker:
    @inject.params(game_info=GameInfo, logger=logging.Logger)
    def __init__(self, game_info: GameInfo, logger: logging.Logger):
        self.game_info = game_info
        self.logger = logger
        if self.game_info.is_immediate_run:
            self.next_time_to_help = datetime.now()
        else:
            self.set_next_time_to_help()

    def set_next_time_to_help(self):
        self.next_time_to_help = datetime.now() + timedelta(minutes=1)

    def is_time_to_help(self) -> bool:
        return datetime.now() > self.next_time_to_help
    
    def is_in_base_home(self) -> bool:
        try:
            pyautogui.locateOnScreen(self.game_info.money_left_top_img_path, confidence=1)
            return True
        except pyautogui.ImageNotFoundException:
            return False
        
    def help(self) -> bool:
        if not self.is_time_to_help():
            return False

        if not self.is_in_base_home():
            return False
        
        try:
            pos = pyautogui.locateOnScreen(self.game_info.alliance_help_img_path, confidence=0.9)
            button_center = pyautogui.center(pos)
            pyautogui.click(button_center)
            time.sleep(0.2)
            self.logger.info("幫助盟友")
        except pyautogui.ImageNotFoundException:
            return False

        self.set_next_time_to_help()
        return True