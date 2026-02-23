import mss
import cv2
import numpy as np
import win32gui

def capture_window_mss(window_title):
    """使用 mss 截取特定窗口"""
    # 查找窗口位置
    def find_window_by_title(title):
        def callback(hwnd, windows):
            if win32gui.IsWindowVisible(hwnd):
                window_text = win32gui.GetWindowText(hwnd)
                if title.lower() in window_text.lower():
                    rect = win32gui.GetClientRect(hwnd)
                    pos = win32gui.ClientToScreen(hwnd, (rect[0], rect[1]))
                    size_pos = win32gui.ClientToScreen(hwnd, (rect[2], rect[3]))
                    windows.append({
                        'handle': hwnd,
                        'rect': (pos[0], pos[1], size_pos[0]-pos[0], size_pos[1]-pos[1])
                    })
            return True
        
        windows = []
        win32gui.EnumWindows(callback, windows)
        return windows[0] if windows else None

    window_info = find_window_by_title(window_title)
    if not window_info:
        print(f"找不到标题包含 '{window_title}' 的窗口")
        return None

    # 获取窗口句柄和位置信息
    hwnd = window_info['handle']
    x, y, width, height = window_info['rect']
    print(f"窗口客户区大小: {width} x {height}")

    # 将窗口置顶
    try:
        win32gui.BringWindowToTop(hwnd)
        win32gui.SetForegroundWindow(hwnd)
    except Exception as e:
        print(f"窗口置顶失败: {e}")

    with mss.mss() as sct:
        monitor = {"top": y, "left": x, "width": width, "height": height}
        screenshot = sct.grab(monitor)
        img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_BGRA2BGR)
        return img