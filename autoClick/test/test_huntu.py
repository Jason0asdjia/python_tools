import re
import pyautogui as pyg
import random
import time
from ..src._Tools import _Tools
import pywintypes
import win32gui
# str = 'Progress: %(bar)s %(percent)3d%%'

# # print(re.search('(?P<name>.*))','Progress: %(bar)s %(percent)3d%%'))
# total = 80
# match = re.search('(?P<name>%\(.+?\))', 'Progress: %(bar)s %(percent)3d%%')
# fmt = 'Progress:s %(percent)3d%%'
# res = re.sub(r'(?P<name>%\(.+?\))d', r'\g<name>%dd' % 23, fmt)

# _, _, width, hight = win32gui.GetClientRect(win32gui.GetDesktopWindow())

# print(width, hight)

import win32gui
import win32api
import win32con
import win32process
import psutil

# time.sleep(2)
# # jubing
# hwnd = win32gui.GetForegroundWindow()
# # if win32gui.IsWindowVisible(hwnd):
# #     if '程序标题' in win32gui.GetWindowText(hwnd):  # 判断是否符合
# #         _, PID = win32process.GetWindowThreadProcessId(
# #             hwnd)  # 通过句柄ID查询进程PID（第0个元素不管，第1个元素是PID）
# #         p = psutil.Process(PID)  # 实例化PID
# #         p.terminate()  # 关闭PID进程
# hld = win32gui.FindWindow(None, u"阴阳师-网易游戏")  #返回窗口标题为阴阳师-网易游戏的句柄
# print(win32gui.GetClientRect(hld))

# TODO多开获取全部窗口句柄
hld1 = win32gui.FindWindow(None, u"阴阳师-网易游戏")  # 返回窗口标题为阴阳师-网易游戏的句柄
print(hld1)
win32gui.ShowWindow(hld1, win32con.SW_MINIMIZE)  # 可以从最小化变回
hld2 = win32gui.FindWindow(None, u"阴阳师-网易游戏")  # 返回窗口标题为阴阳师-网易游戏的句柄
print(hld2)
win32gui.ShowWindow(hld1, win32con.SW_SHOWNORMAL)

# win32gui.SetForegroundWindow(hld)  # 无法将窗口从最小化变回
# _, _, width, high = win32gui.GetClientRect(hld)
# left, top, right, botton = win32gui.GetWindowRect(hld)
# # print(win32gui.GetClientRect(hld))
# # win32api.SetCursorPos([left + width // 2, top + high // 2])
# win32api.SetCursorPos([left + int(width * 0.95304), top + int(high * 0.94538)])
# mouse_x = left + width / 2
# mouse_y = top + high / 2
# print(_Tools.random_range(mouse_x, 4))
# print(mouse_y)
# print(left + int(width * 0.91304))
# print(top + int(high * 0.94538))
# print(str(width) + "--" + str(high))
# 挑战按钮占比
# 0.91304 0.94538
# print(_Tools.random_time(left + int(width * 0.91304), 1))

# print(str(width // 2) + "---" + str(high // 2))
# # print(str(left) + "---" + str(top))\
# print(win32gui.GetWindowRect(hld))
# print(str(left + width) + "---" + str(top + high))

# win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
# _Tools.click_here(2, 0)
# 1802 629
# 861 502
# str = "阴阳师-网易游戏"
# print(type(str))
# unicode = str.encode('utf-8').decode('utf-8')
# print(type(unicode))

# print(_Tools.random_range(10, 1))

# for _ in range(4):
#     print(random.random())
