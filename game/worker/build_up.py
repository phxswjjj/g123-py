
from datetime import datetime, timedelta
import time
import pyautogui
from game.game_info import GameInfo
import inject
import logging


class BuildUpWorker:
    @inject.params(game_info=GameInfo, logger=logging.Logger)
    def __init__(self, game_info: GameInfo, logger: logging.Logger):
        self.game_info = game_info
        self.logger = logger
        if self.game_info.is_immediate_run:
            self.next_time_to_fight = datetime.now()
        else:
            self.set_next_time_to_fight()

    def set_next_time_to_fight(self):
        self.next_time_to_fight = datetime.now() + timedelta(seconds=5)

    def is_time_to_fight(self) -> bool:
        return datetime.now() > self.next_time_to_fight

    def is_in_build_up(self) -> bool:
        try:
            pos = pyautogui.locateOnScreen(self.game_info.build_up_title_img_path, confidence=0.8)
            return True
        except pyautogui.ImageNotFoundException:
            return False
        
    def is_joined(self) -> bool:
        try:
            pos = pyautogui.locateOnScreen(self.game_info.build_up_joined_img_path, confidence=0.8)
            return True
        except pyautogui.ImageNotFoundException:
            return False
        
    def click_empty_slot(self) -> bool:
        try:
            pos = pyautogui.locateOnScreen(self.game_info.build_up_empty_slot_img_path, confidence=0.8)
            button_center = pyautogui.center(pos)
            pyautogui.click(button_center)
            time.sleep(0.2)
            return True
        except pyautogui.ImageNotFoundException:
            return False

    def build_up(self) -> bool:

        if not self.is_time_to_fight():
            return False

        if not self.is_in_build_up():
            return False
        
        if self.is_joined():
            return False
        
        if not self.click_empty_slot():
            return False
        
        try:
            # 套用第8軍團
            pos = pyautogui.locateOnScreen(self.game_info.build_up_army8_img_path, confidence=0.8)
            button_center = pyautogui.center(pos)
            pyautogui.click(button_center)
            time.sleep(0.2)
        except pyautogui.ImageNotFoundException:
            self.logger.error("找不到第8軍團圖片")
            return False
        
        # fight button
        pyautogui.click((959, 491))
        time.sleep(0.2)
        
        self.set_next_time_to_fight()
        return True
        
        
        