
from datetime import datetime, timedelta
import time
import pyautogui

from game.worker.daily_military_intellgence import DailyMilitaryIntelligenceWorker
import inject
from game.game_info import GameInfo


class CollectKnivesOutWorker:
    @inject.params(game_info=GameInfo)
    def __init__(self, game_info: GameInfo):
        self.game_info = game_info
        self.daily_military_intelligence_worker = DailyMilitaryIntelligenceWorker(game_info)
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
            button_location = pyautogui.locateOnScreen(self.game_info.money_left_top_img_path, confidence=0.8)
            return True
        except pyautogui.ImageNotFoundException:
            return False

    def collect_knives_out(self) -> bool:
        if not self.is_time_to_collect():
            return False

        if not self.game_info.is_in_game():
            return False
        
        if not self.is_in_base_home():
            return False
        
        if not self.daily_military_intelligence_worker.go_daily_military_intelligence():
            return False
        
        # 前往荒野行動
        pyautogui.click((1097, 337))
        time.sleep(0.2)

        # 前往領取畫面
        pyautogui.click((755, 303))
        time.sleep(0.2)

        # 領取
        pyautogui.click((963, 860))
        time.sleep(0.5)
        pyautogui.click((963, 860))
        time.sleep(0.2)

        # 返回主頁
        pyautogui.click((739, 145))
        time.sleep(0.2)
        pyautogui.click((739, 145))
        time.sleep(0.2)

        self.set_next_time_to_collect()

        return True