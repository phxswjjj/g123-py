import win32gui

def bring_window_to_front(window_title):
    hwnd = win32gui.FindWindow(None, window_title)
    if hwnd:
        win32gui.SetForegroundWindow(hwnd)
        print(f"視窗 '{window_title}' 已帶至前台")
        return True
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