
from datetime import datetime, timedelta
import logging
import time

import inject
import pyautogui
from game.game_info import GameInfo


class TreasureRaiderWorker:
    @inject.params(game_info=GameInfo, logger=logging.Logger)
    def __init__(self, game_info: GameInfo, logger: logging.Logger):
        self.game_info = game_info
        self.logger = logger
        if self.game_info.is_immediate_run:
            self.next_time_to_fire = datetime.now()
        else:
            self.set_next_time_to_fire()

    def set_next_time_to_fire(self):
        self.next_time_to_fire = datetime.now() + timedelta(seconds=10)

    def is_time_to_fire(self) -> bool:
        return datetime.now() > self.next_time_to_fire
    
    def is_in_big_map(self) -> bool:
        try:
            pos = pyautogui.locateOnScreen(self.game_info.map_watch_full_img_path, confidence=0.9)
            return True
        except pyautogui.ImageNotFoundException:
            return False
        
    def search_and_click_raider(self) -> bool:
        try:
            pos = pyautogui.locateOnScreen(self.game_info.map_treasure_raider_img_path, confidence=0.9)
            button_center = pyautogui.center(pos)
            pyautogui.click(button_center)
            time.sleep(1)
            return True
        except pyautogui.ImageNotFoundException:
            return False

    def search_raider(self) -> bool:
        if not self.is_time_to_fire():
            return False

        if not self.game_info.is_in_game():
            return False
        
        if not self.is_in_big_map():
            return False
        
        if not self.search_and_click_raider():
            return False

        self.logger.info("找到敵方奪寶基地")
        self.set_next_time_to_fire()
        return True
