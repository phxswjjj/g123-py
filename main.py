from game.worker.build_up import BuildUpWorker
from game.worker.collect_alliance_gift import CollectAllianceGiftWorker
from game.worker.collect_expedition import CollectExpeditionWorker
from game.worker.collect_knivesout import CollectKnivesOutWorker
from game.worker.collect_money import CollectMoneyWorker
from game.game_info import GameInfo
import time
import keyboard
import inject

# global variable to control script running
running = True

def stop_script(e):
    global running
    running = False
    print("檢測到 F1 按鍵,腳本停止運行")

def configure_inject(binder):
    game_info = GameInfo()
    binder.bind(GameInfo, game_info)

def main():
    global running

    print("按下 F1 可以隨時停止腳本")
    print("按下 F2 可以截取滑鼠位置的100x100像素畫面")

    inject.configure(configure_inject)
    game_info = inject.instance(GameInfo)

    # register F1 and F2 key press events
    keyboard.on_press_key('f1', stop_script)
    keyboard.on_press_key('f2', game_info.create_screenshot_function())
    game_info.bring_window_to_front()

    collect_money_worker = inject.instance(CollectMoneyWorker)
    build_up_worker = inject.instance(BuildUpWorker)
    collect_expedition_worker = inject.instance(CollectExpeditionWorker)
    collect_alliance_gift_worker = inject.instance(CollectAllianceGiftWorker)
    collect_knives_out_worker = inject.instance(CollectKnivesOutWorker)

    while running:
        collect_money_worker.collect_money()
        build_up_worker.build_up()
        collect_expedition_worker.collect_expedition()
        collect_alliance_gift_worker.collect_alliance_gift()
        collect_knives_out_worker.collect_knives_out()
        time.sleep(1)

    print("程序已執行完畢。")

if __name__ == "__main__":
    main()

