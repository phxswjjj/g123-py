

from datetime import datetime, timedelta
import logging
import time
import cv2
import inject
import numpy as np
import pyautogui

from game.game_info import GameInfo


class EqpMaterialCollectWorker:
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
    
    def click_return_button(self) -> bool:
        try:
            button_location = pyautogui.locateOnScreen(self.game_info.eqp_material_collect_back_img_path, confidence=0.9)
            button_center = pyautogui.center(button_location)
            pyautogui.click(button_center)
            time.sleep(0.5)
            return True
        except pyautogui.ImageNotFoundException:
            return False
    
    def enter_eqp_material_ui(self) -> bool:
        scales = [1.0 + 0.16 * i for i in range(8)]
        template = cv2.imread(self.game_info.eqp_material_collect_img_path, 0)
        
        for scale in scales:
            try:
                screenshot = pyautogui.screenshot()
                screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)
                resized_template = cv2.resize(template, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
                
                result = cv2.matchTemplate(screenshot, resized_template, cv2.TM_CCOEFF_NORMED)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
                
                if max_val > 0.8:  # 使用与之前相同的置信度
                    button = (max_loc[0] + resized_template.shape[1] // 2 - 20 * scale,
                                     max_loc[1] + resized_template.shape[0] // 2 - 50 * scale)
                    self.logger.info(f"已点击收集裝備材料按钮（缩放比例：{scale}）")
                    # pyautogui.moveTo(button)
                    # 可能有完成的材料
                    for _ in range(3):
                        pyautogui.click(button)
                        time.sleep(0.3)
                    if not self.is_production_ui():
                        # 不小心進入專精畫面要返回 2 次
                        for _ in range(2):
                            self.click_return_button()
                    return True
            except Exception as e:
                self.logger.error(f"尝试缩放比例 {scale} 时出错：{str(e)}")
                continue
        
        self.logger.error("未找到收集裝備材料按钮")
        return False
    
    def is_production_ui(self) -> bool:
        try:
            pyautogui.locateOnScreen(self.game_info.eqp_material_collect_production_img_path, confidence=0.9)
            return True
        except pyautogui.ImageNotFoundException:
            return False
        
    def add_material_if_empty(self) -> bool:
        try:
            button_location = pyautogui.locateOnScreen(self.game_info.eqp_material_collect_production_img_path, confidence=0.9)
            button_center = pyautogui.center(button_location)
            # 隨便收集材料*2
            pyautogui.click(1127, 798)
            time.sleep(0.2)
            pyautogui.click(1127, 798)
            time.sleep(0.2)
            self.logger.info("增加生產材料")
            for _ in range(2):
                self.click_return_button()
            return True
        except pyautogui.ImageNotFoundException:
            return False

    def collect(self) -> bool:
        if not self.is_time_to_collect():
            return False

        if not self.game_info.is_in_game():
            return False

        if not self.game_info.is_in_base_home():
            return False
        
        if not self.enter_eqp_material_ui():
            return False
        
        self.add_material_if_empty()
        
        self.set_next_time_to_collect()
        
        return True