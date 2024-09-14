import time
import inject
from game.game_info import GameInfo
from game.worker.change_world import ChangeWorldWorker
from datetime import datetime, timedelta
import pyautogui
import cv2
import numpy as np

class CollectMoneyWorker:
    @inject.params(game_info=GameInfo)
    def __init__(self, game_info: GameInfo):
        self.game_info = game_info
        self.go_home_worker = ChangeWorldWorker(game_info)
        if self.game_info.is_immediate_run:
            self.next_time_to_collect = datetime.now()
        else:
            self.set_next_time_to_collect()

    def set_next_time_to_collect(self):
        self.next_time_to_collect = datetime.now() + timedelta(minutes=10)

    def is_time_to_collect(self) -> bool:
        return datetime.now() > self.next_time_to_collect

    def is_in_base_home(self) -> bool:
        try:
            button_location = pyautogui.locateOnScreen(self.game_info.money_left_top_img_path, confidence=0.8)
            return True
        except pyautogui.ImageNotFoundException:
            return False

    def collect_money_by_click(self) -> bool:
        scales = [1.0 + 0.16 * i for i in range(8)]
        template = cv2.imread(self.game_info.money_collect_base_img_path, 0)
        
        for scale in scales:
            try:
                screenshot = pyautogui.screenshot()
                screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)
                resized_template = cv2.resize(template, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
                
                result = cv2.matchTemplate(screenshot, resized_template, cv2.TM_CCOEFF_NORMED)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
                
                if max_val > 0.8:  # 使用与之前相同的置信度
                    button = (max_loc[0] + resized_template.shape[1] // 2,
                                     max_loc[1] + resized_template.shape[0] // 2 - 70 * scale)
                    # pyautogui.moveTo(button)
                    pyautogui.click(button)
                    print(f"已点击收集金钱按钮（缩放比例：{scale}）")
                    time.sleep(0.5)
                    self.close_no_money_window()
                    self.set_next_time_to_collect()
                    time.sleep(0.2)
                    return True
            except Exception as e:
                print(f"尝试缩放比例 {scale} 时出错：{str(e)}")
                continue
        
        print("未找到收集金钱按钮")
        return False
    
    def close_no_money_window(self) -> bool:
        try:
            button_location = pyautogui.locateOnScreen(self.game_info.close_window_button_img_path, confidence=0.9)
            pyautogui.click(button_location)
            return True
        except pyautogui.ImageNotFoundException:
            return False

    def collect_money(self) -> bool:
        if not self.is_time_to_collect():
            return False

        if not self.game_info.is_in_game():
            return False
        
        # self.go_home_worker.go_home()

        if not self.is_in_base_home():
            return False
        
        return self.collect_money_by_click()

