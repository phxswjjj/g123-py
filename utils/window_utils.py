import win32gui
import win32com.client
import pyautogui
import os
from datetime import datetime

def is_in_game(window_title):
    hwnd = win32gui.FindWindow(None, window_title)
    if not hwnd:
        return False
    
    if not win32gui.IsWindowVisible(hwnd):
        return False

    # window boundary
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)

    # get current cursor position
    x, y = pyautogui.position()
    # check if cursor is in window
    if left < x < right and top < y < bottom:
        return True
    else:
        return False

def bring_window_to_front(window_title):
    hwnd = win32gui.FindWindow(None, window_title)
    if hwnd:
        try:
            win32gui.SetForegroundWindow(hwnd)
            print(f"視窗 '{window_title}' 已帶至前台")
            return True
        except Exception as e:
            print(f"無法將視窗 '{window_title}' 帶至前台: {e}")
            try:
                # 嘗試使用另一種方法
                shell = win32com.client.Dispatch("WScript.Shell")
                shell.SendKeys('%')
                win32gui.SetForegroundWindow(hwnd)
                print(f"使用替代方法將視窗 '{window_title}' 帶至前台")
                return True
            except Exception as e2:
                print(f"替代方法也失敗: {e2}")
    else:
        print(f"找不到視窗 '{window_title}'")
    return False

def print_all_windows_title():
    def enum_windows_callback(hwnd, lParam):
        if win32gui.IsWindowVisible(hwnd):
            window_title = win32gui.GetWindowText(hwnd)
            if window_title:
                print(window_title)
    win32gui.EnumWindows(enum_windows_callback, None)

def capture_screenshot(e, image_path=None):
    # 獲取當前滑鼠位置
    x, y = pyautogui.position()
    
    image_size = 100
    # 截取滑鼠周圍100x100的區域,使用int()確保所有值都是整數
    screenshot = pyautogui.screenshot(region=(
        int(x-image_size/2), 
        int(y-image_size/2), 
        image_size, 
        image_size
    ))

    if image_path is None:
        image_path = ".\imgs_tmp"
    # 確保.\imgs目錄存在
    if not os.path.exists(image_path):
        os.makedirs(image_path)
    
    # 生成唯一的文件名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{image_path}\screenshot_{x}_{y}_{timestamp}.png"
    
    # 保存截圖
    screenshot.save(filename)
    print(f"截圖已保存: {filename}")