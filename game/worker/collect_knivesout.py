
from datetime import datetime, timedelta
import time
import pyautogui

from game.worker.daily_military_intellgence import DailyMilitaryIntelligenceWorker
import inject
from game.game_info import GameInfo
import logging


class CollectKnivesOutWorker:
    @inject.params(game_info=GameInfo, daily_military_intelligence_worker=DailyMilitaryIntelligenceWorker, logger=logging.Logger)
    def __init__(self, game_info: GameInfo, daily_military_intelligence_worker: DailyMilitaryIntelligenceWorker, logger: logging.Logger):
        self.game_info = game_info
        self.daily_military_intelligence_worker = daily_military_intelligence_worker
        self.logger = logger
        if self.game_info.is_immediate_run:
            self.next_time_to_collect = datetime.now()
        else:
            self.set_next_time_to_collect()

    def set_next_time_to_collect(self):
        self.next_time_to_collect = datetime.now() + timedelta(hours=1)

    def is_time_to_collect(self) -> bool:
        return datetime.now() > self.next_time_to_collect

    def click_collect_all(self) -> bool:
        try:
            button_location = pyautogui.locateOnScreen(self.game_info.knivesout_collect_all_img_path, confidence=0.9)
            button_center = pyautogui.center(button_location)
            pyautogui.click(button_center)
            self.logger.info("已点击一鍵領取")
            return True
        except pyautogui.ImageNotFoundException:
            return False

    def collect_knives_out(self) -> bool:
        if not self.is_time_to_collect():
            return False

        if not self.game_info.is_in_game():
            return False
        
        if not self.game_info.is_in_base_home():
            return False
        
        if not self.daily_military_intelligence_worker.go_daily_military_intelligence():
            return False
        
        # 前往荒野行動
        self.logger.info("前往荒野行動")
        pyautogui.click((1097, 337))
        time.sleep(0.2)

        if not self.click_collect_all():
            # 返回主頁
            pyautogui.click((739, 145))
            time.sleep(0.2)

            self.set_next_time_to_collect()
            return False

        # 領取
        pyautogui.click((959, 846))
        time.sleep(0.5)
        # 確定
        pyautogui.click((971, 923))
        time.sleep(0.5)
        pyautogui.click((971, 923))
        time.sleep(0.2)

        # 返回主頁
        pyautogui.click((739, 145))
        time.sleep(0.2)

        self.set_next_time_to_collect()

        return True