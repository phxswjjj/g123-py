# class to collect money
from game.game_info import GameInfo
from game.worker.change_world import ChangeWorldWorker


class CollectMoneyWorker:
    def __init__(self, game_info: GameInfo):
        self.game_info = game_info
        self.go_home_worker = ChangeWorldWorker(game_info)

    def is_time_to_collect(self):
        return True

    def collect_money_by_click(self):
        return True

    def collect_money(self) -> bool:

        if not self.game_info.is_in_game():
            return False
        
        if not self.is_time_to_collect():
            return False
        
        if not self.go_home_worker.go_home():
            return False
        
        return self.collect_money_by_click()

