
from datetime import datetime, timedelta
import time
import cv2
import numpy as np
import pyautogui
from game.game_info import GameInfo
import inject
import logging


class CollectExpeditionWorker:
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
        
    def collect_expedition_by_click(self) -> bool:
        scales = [1.0 + 0.16 * i for i in range(8)]
        template = cv2.imread(self.game_info.collect_expedition_img_path, 0)
        
        for scale in scales:
            try:
                screenshot = pyautogui.screenshot()
                screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)
                resized_template = cv2.resize(template, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
                
                result = cv2.matchTemplate(screenshot, resized_template, cv2.TM_CCOEFF_NORMED)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
                
                if max_val > 0.8:  # 使用与之前相同的置信度
                    button = (max_loc[0] + resized_template.shape[1] // 2 - 10 * scale,
                                     max_loc[1] + resized_template.shape[0] // 2 - 60 * scale)
                    # pyautogui.moveTo(button)
                    pyautogui.click(button)
                    self.logger.info(f"已点击收集遠征按钮（缩放比例：{scale}）")
                    self.set_next_time_to_collect()
                    return True
            except Exception as e:
                self.logger.error(f"尝试缩放比例 {scale} 时出错：{str(e)}")
                continue
        
        self.logger.error("未找到收集遠征按钮")
        return False

    def collect_expedition(self) -> bool:
        if not self.is_time_to_collect():
            return False

        if not self.game_info.is_in_game():
            return False

        if not self.game_info.is_in_base_home():
            return False
        
        if not self.collect_expedition_by_click():
            return False
        
        time.sleep(0.2)

        # 點卡車
        pyautogui.click((842, 884))
        time.sleep(0.5)

        # 領取
        pyautogui.click((961, 930))
        time.sleep(0.5)

        # exit
        pyautogui.click((742, 146))
        time.sleep(0.2)

        return True