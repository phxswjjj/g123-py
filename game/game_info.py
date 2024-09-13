from utils.window_utils import capture_screenshot, bring_window_to_front, is_in_game

# 建立 game info class
class GameInfo:
    def __init__(self):
        self.title = "鮮豔軍團 | 開始遊戲 - G123 - Google Chrome"
        self.img_root = ".\imgs"
        self.img_tmp = ".\imgs_tmp"
        self.back_home_img_path = rf"{self.img_root}\back_home.png"
        self.go_world_img_path = rf"{self.img_root}\go_world.png"
        self.world_search_img_path = rf"{self.img_root}\world_search.png"
        self.money_collect_base_img_path = rf"{self.img_root}\money_collect_base.png"
        self.money_left_top_img_path = rf"{self.img_root}\money_left_top.png"
        self.build_up_title_img_path = rf"{self.img_root}\build_up_title.png"
        self.build_up_empty_slot_img_path = rf"{self.img_root}\build_up_empty_slot.png"
        self.build_up_army8_img_path = rf"{self.img_root}\build_up_army8.png"
        self.build_up_fight_img_path = rf"{self.img_root}\build_up_fight.png"
        self.collect_expedition_img_path = rf"{self.img_root}\collect_expedition.png"
        self.alliance_img_path = rf"{self.img_root}\alliance.png"
        self.daily_task_img_path = rf"{self.img_root}\daily_task.png"

    def create_screenshot_function(self):
        return lambda e: capture_screenshot(e, self.img_tmp)

    def bring_window_to_front(self):
        bring_window_to_front(self.title)

    def is_in_game(self):
        return is_in_game(self.title)