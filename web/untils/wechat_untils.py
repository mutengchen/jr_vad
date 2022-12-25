import win32gui as gui
import win32con as con
from time import sleep
import pyautogui


def callWechat(call_name):
    # 记录次数
    count = 0
    # 查找好友聊天窗口
    win = gui.FindWindow(None,call_name)
    while win == 0 and count <= 5:
        count += 1
        win = gui.FindWindow(None,call_name)
    sleep(1)
    # 窗口置顶
    gui.SetForegroundWindow(win)
    # 窗口最大化
    gui.ShowWindow(win, con.SW_SHOWMAXIMIZED)
    # 获取windows坐标
    local = gui.GetWindowRect(win)
    print(local)
    sleep(1)
    x = local[2]/1.04
    y = local[3]/1.389
    # pyautogui.move(20,20)
    pyautogui.click(x,y)
    # 窗口最大化
    gui.ShowWindow(win, con.SW_SHOWNORMAL)
    gui.ShowWindow(win, con.SW_SHOWMINIMIZED)


# # 修改call_name为对方微信昵称
# call_name = "老婆多吃点"
# callname = callWechat()
# callname.click_video(call_name)
