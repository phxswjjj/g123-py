
from datetime import datetime, timedelta
import time
import pyautogui
from game.game_info import GameInfo
import inject


class BuildUpWorker:
    @inject.params(game_info=GameInfo)
    def __init__(self, game_info: GameInfo):
        self.game_info = game_info
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

    def build_up(self) -> bool:

        if not self.is_time_to_fight():
            return False

        if not self.is_in_build_up():
            return False
        
        try:
            # 有空的位置
            empty_slot_pos = pyautogui.locateOnScreen(self.game_info.build_up_empty_slot_img_path, confidence=0.8)
            button_center = pyautogui.center(empty_slot_pos)
            pyautogui.click(button_center)
        except pyautogui.ImageNotFoundException:
            return False
        
        time.sleep(0.2)
        
        try:
            # 套用第8軍團
            pos = pyautogui.locateOnScreen(self.game_info.build_up_army8_img_path, confidence=0.8)
            button_center = pyautogui.center(pos)
            pyautogui.click(button_center)
        except pyautogui.ImageNotFoundException:
            print("找不到第8軍團圖片")
            return False
        
        time.sleep(0.2)

        # fight button
        pyautogui.click((959, 491))
        
        self.set_next_time_to_fight()
        return True
        
        
        