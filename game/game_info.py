import pyautogui
from utils.window_utils import capture_screenshot, bring_window_to_front, is_in_game

# 建立 game info class
class GameInfo:
    def __init__(self):
        self.title = "鮮豔軍團 | 開始遊戲 - G123 - Google Chrome"
        self.is_immediate_run = True
        self.img_root = ".\imgs"
        self.img_tmp = ".\imgs_tmp"
        self.back_home_img_path = rf"{self.img_root}\back_home.png"
        self.go_world_img_path = rf"{self.img_root}\go_world.png"
        self.go_world2_img_path = rf"{self.img_root}\go_world2.png"
        self.world_search_img_path = rf"{self.img_root}\world_search.png"
        self.money_collect_base_img_path = rf"{self.img_root}\money_collect_base.png"
        self.money_left_top_img_path = rf"{self.img_root}\money_left_top.png"
        self.build_up_title_img_path = rf"{self.img_root}\build_up_title.png"
        self.build_up_empty_slot_img_path = rf"{self.img_root}\build_up_empty_slot.png"
        self.build_up_army8_img_path = rf"{self.img_root}\build_up_army8.png"
        self.build_up_fight_img_path = rf"{self.img_root}\build_up_fight.png"
        self.build_up_joined_img_path = rf"{self.img_root}\build_up_joined.png"
        self.build_up_cancel_img_path = rf"{self.img_root}\build_up_cancel.png"
        self.build_up_back_img_path = rf"{self.img_root}\build_up_back.png"
        self.collect_expedition_img_path = rf"{self.img_root}\collect_expedition.png"
        self.alliance_img_path = rf"{self.img_root}\alliance.png"
        self.daily_task_img_path = rf"{self.img_root}\daily_task.png"
        self.close_window_button_img_path = rf"{self.img_root}\close_window_button.png"
        self.alliance_help_img_path = rf"{self.img_root}\alliance_help.png"
        self.knivesout_collect_all_img_path = rf"{self.img_root}\knivesOut_collect_all.png"
        self.eqp_material_collect_img_path = rf"{self.img_root}\eqp_material_collect.png"
        self.eqp_material_collect_production_img_path = rf"{self.img_root}\eqp_material_collect_production.png"
        self.eqp_material_collect_empty5_img_path = rf"{self.img_root}\eqp_material_collect_empty5.png"
        self.eqp_material_collect_back_img_path = rf"{self.img_root}\eqp_material_collect_back.png"
        self.disconnection_img_path = rf'{self.img_root}\disconnection.png'
        self.move_base_img_path = rf'{self.img_root}\move_base.png'
        self.map_watch_full_img_path = rf'{self.img_root}\map_watch_full.png'
        self.map_treasure_raider_img_path = rf'{self.img_root}\map_treasure_raider.png'
        self.map_thor_mine_img_path = rf'{self.img_root}\map_thor_mine.png'
        self.exercise_challenge_img_path = rf'{self.img_root}\exercise_challenge.png'
        self.exercise_challenge_free_img_path = rf'{self.img_root}\exercise_challenge_free.png'

    def create_screenshot_function(self):
        return lambda e: capture_screenshot(e, self.img_tmp)

    def bring_window_to_front(self):
        bring_window_to_front(self.title)

    def is_in_game(self):
        return is_in_game(self.title)

    def is_in_base_home(self) -> bool:
        try:
            pyautogui.locateOnScreen(self.money_left_top_img_path, confidence=0.99)
        except pyautogui.ImageNotFoundException:
            return False
        
        try:
            pyautogui.locateOnScreen(self.go_world_img_path, confidence=0.99)
        except pyautogui.ImageNotFoundException:            
            try:
                pyautogui.locateOnScreen(self.go_world2_img_path, confidence=0.99)
            except pyautogui.ImageNotFoundException:
                return False
        
        return True