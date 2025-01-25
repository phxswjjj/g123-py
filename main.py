import json
import logging
from game.worker.abnormal import AbnormalWorker
from game.worker.alliance_help import AllianceHelpWorker
from game.worker.build_up import BuildUpWorker
from game.worker.collect_alliance_gift import CollectAllianceGiftWorker
from game.worker.collect_expedition import CollectExpeditionWorker
from game.worker.collect_knivesout import CollectKnivesOutWorker
from game.worker.collect_money import CollectMoneyWorker
from game.game_info import GameInfo
import time
import keyboard
import inject
import seqlog
from win32api import GetKeyState
from win32con import VK_CAPITAL

from game.worker.eqp_material_collect import EqpMaterialCollectWorker
from game.worker.exercise_challenge import ExerciseChallengeWorker
from game.worker.treasure_raider import TreasureRaiderWorker

# global variable to control script running
running = True

def stop_script(e):
    global running
    running = False
    print("檢測到 F1 按鍵,腳本停止運行")

def configure_inject(binder):
    game_info = GameInfo()
    binder.bind(GameInfo, game_info)

    logger = configure_seq()
    binder.bind(logging.Logger, logger)

def configure_seq() -> logging.Logger:
    # seqlog.log_to_seq(
    #     server_url="http://seq.local:5341/",
    #     level=logging.INFO,
    #     batch_size=10,
    #     auto_flush_timeout=10,  # seconds
    #     override_root_logger=True,
    #     json_encoder_class=json.encoder.JSONEncoder,
    #     support_extra_properties=True
    # )

    logger = logging.getLogger('g123')
    
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logger.addHandler(console)

    return logger

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

    abnormal_worker = inject.instance(AbnormalWorker)
    collect_money_worker = inject.instance(CollectMoneyWorker)
    build_up_worker = inject.instance(BuildUpWorker)
    collect_expedition_worker = inject.instance(CollectExpeditionWorker)
    collect_alliance_gift_worker = inject.instance(CollectAllianceGiftWorker)
    collect_knives_out_worker = inject.instance(CollectKnivesOutWorker)
    alliance_help_worker = inject.instance(AllianceHelpWorker)
    eqp_material_collect_worker = inject.instance(EqpMaterialCollectWorker)
    treasure_raider_worker = inject.instance(TreasureRaiderWorker)
    exercise_challenge_worker = inject.instance(ExerciseChallengeWorker)

    while running:
        # caps lock on = pause, off = run
        if GetKeyState(VK_CAPITAL):
            time.sleep(1)
            continue

        # 連線中斷
        abnormal_worker.reconnection()
        # 取消遷城
        abnormal_worker.cancel_move_base()

        # 金幣收割
        # collect_money_worker.collect_money()
        # 集結
        build_up_worker.build_up()
        # 遠征行動
        # collect_expedition_worker.collect_expedition()
        # 聯盟禮物
        collect_alliance_gift_worker.collect_alliance_gift()
        # 荒野行動(一鍵領取)
        collect_knives_out_worker.collect_knives_out()
        # 聯盟封助
        # alliance_help_worker.help()
        # 裝備材料
        eqp_material_collect_worker.collect()

        # 奪寶奇兵-尋找敵方基地
        treasure_raider_worker.search_raider()

        # 跨戰區演習挑戰
        exercise_challenge_worker.challenge()

        time.sleep(1)

    print("程序已執行完畢。")

if __name__ == "__main__":
    main()

