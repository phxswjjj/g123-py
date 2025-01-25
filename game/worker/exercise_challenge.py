
from datetime import datetime, timedelta
import logging
import time

import pyautogui
import inject
from game.game_info import GameInfo


class ExerciseChallengeWorker:
    @inject.params(game_info=GameInfo, logger=logging.Logger)
    def __init__(self, game_info: GameInfo, logger: logging.Logger):
        self.game_info = game_info
        self.logger = logger
        if self.game_info.is_immediate_run:
            self.next_time_to_work = datetime.now()
        else:
            self.set_next_time_to_work()

    def set_next_time_to_work(self):
        # self.next_time_to_work = datetime.now() + timedelta(hours=1)
        None

    def is_time_to_collect(self) -> bool:
        return datetime.now() > self.next_time_to_work
    
    def is_exercise_challenge(self) -> bool:
        try:
            pyautogui.locateOnScreen(self.game_info.exercise_challenge_img_path, confidence=0.9)
            return True
        except pyautogui.ImageNotFoundException:
            return False

    def challenge(self) -> bool:
        if not self.is_time_to_collect():
            return False

        if not self.game_info.is_in_game():
            return False
        
        if not self.is_exercise_challenge():
            return False
        
        try:
            button_location = pyautogui.locateOnScreen(self.game_info.exercise_challenge_free_img_path, confidence=0.9)
            button_center = pyautogui.center(button_location)
            pyautogui.click(button_center)
            self.logger.info("已点击跨戰區演習挑戰按钮")
        except pyautogui.ImageNotFoundException:
            return False

        time.sleep(0.3)

        # click 戰鬥
        pyautogui.click((960, 488))
        time.sleep(2)
        
        # click 跳過
        pyautogui.click((27, 269))
        time.sleep(0.3)
        
        # click 返回
        pyautogui.click((960, 922))
        time.sleep(0.3)
        
        self.set_next_time_to_work()

        return True