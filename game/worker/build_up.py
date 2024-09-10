
from datetime import datetime, timedelta
import time
import pyautogui
from game.game_info import GameInfo


class BuildUpWorker:
    def __init__(self, game_info: GameInfo):
        self.game_info = game_info
        self.set_next_time_to_fight()

    def set_next_time_to_fight(self):
        self.next_time_to_fight = datetime.now() + timedelta(seconds=5)

    def is_time_to_collect(self) -> bool:
        return datetime.now() > self.next_time_to_fight

    def is_in_build_up(self) -> bool:
        try:
            pos = pyautogui.locateOnScreen(self.game_info.build_up_title_img_path, confidence=0.8)
            return True
        except pyautogui.ImageNotFoundException:
            return False

    def build_up(self) -> bool:

        if not self.is_time_to_collect():
            return False

        if not self.is_in_build_up():
            return False
        
        try:
            empty_slot_pos = pyautogui.locateOnScreen(self.game_info.build_up_empty_slot_img_path, confidence=0.8)
            button_center = pyautogui.center(empty_slot_pos)
            pyautogui.click(button_center)
            time.sleep(0.1)
        except pyautogui.ImageNotFoundException:
            return False
        
        try:
            pos = pyautogui.locateOnScreen(self.game_info.build_up_army8_img_path, confidence=0.8)
            button_center = pyautogui.center(pos)
            pyautogui.click(button_center)
            time.sleep(0.1)
            # fight button
            pyautogui.click((959, 491))
            
            self.set_next_time_to_fight()
            return True
        except pyautogui.ImageNotFoundException:
            return False
        
        
        