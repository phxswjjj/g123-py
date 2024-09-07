from utils.window_utils import bring_window_to_front, capture_screenshot
from game.game_info import GameInfo
import time
import keyboard

# create game info object
game_info = GameInfo()

# global variable to control script running
running = True

def stop_script(e):
    global running
    running = False
    print("檢測到 F1 按鍵,腳本停止運行")

def main():
    global running

    print("按下 F1 可以隨時停止腳本")
    print("按下 F2 可以截取滑鼠位置的100x100像素畫面")

    # register F1 and F2 key press events
    keyboard.on_press_key('f1', stop_script)
    keyboard.on_press_key('f2', capture_screenshot)
    bring_window_to_front(game_info.title)

    while running:
        time.sleep(5)  # every 5 seconds

    print("程序已執行完畢。")

if __name__ == "__main__":
    main()

