
from datetime import datetime, timedelta
import logging
import time

import pyautogui
import inject
from game.game_info import GameInfo


class CollectAllianceGiftWorker:
    @inject.params(game_info=GameInfo, logger=logging.Logger)
    def __init__(self, game_info: GameInfo, logger: logging.Logger):
        self.game_info = game_info
        self.logger = logger
        if self.game_info.is_immediate_run:
            self.next_time_to_collect = datetime.now()
        else:
            self.set_next_time_to_collect()

    def set_next_time_to_collect(self):
        self.next_time_to_collect = datetime.now() + timedelta(hours=1)

    def is_time_to_collect(self) -> bool:
        return datetime.now() > self.next_time_to_collect

    def is_in_base_home(self) -> bool:
        try:
            pyautogui.locateOnScreen(self.game_info.money_left_top_img_path, confidence=0.9)
            return True
        except pyautogui.ImageNotFoundException:
            return False

    def collect_alliance_gift(self) -> bool:
        if not self.is_time_to_collect():
            return False

        if not self.game_info.is_in_game():
            return False

        if not self.is_in_base_home():
            return False
        
        try:
            button_location = pyautogui.locateOnScreen(self.game_info.alliance_img_path, confidence=0.9)
            button_center = pyautogui.center(button_location)
            pyautogui.click(button_center)
            self.logger.info("已点击联盟按钮")
        except pyautogui.ImageNotFoundException:
            return False

        time.sleep(0.3)

        # enter gift room
        pyautogui.click((1154, 739))
        time.sleep(0.3)

        # collect button
        pyautogui.click((1133, 882))
        time.sleep(0.5)
        
        # skip gift list
        pyautogui.click((1133, 882))
        time.sleep(0.5)

        # back home
        pyautogui.click((739, 149))
        time.sleep(0.2)
        pyautogui.click((739, 149))
        time.sleep(0.2)
        
        self.set_next_time_to_collect()

        return True