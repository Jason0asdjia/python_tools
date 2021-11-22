import time
import random
import pyautogui as pyg
import threading

import pywintypes
import win32gui
import win32api
import win32con


class _Tools(object):
    # 取消鼠标移至边角停止任务标志
    pyg.FAILSAFE = False
    # 获取屏幕分辨率
    screenWidth, screenhight = pyg.size()
    title = "阴阳师-网易游戏"
    # 使用pywin32 模块（需要提前import pywintypes）
    # 获取游戏窗口，并取得窗口参数
    hld = win32gui.FindWindow(
        None,
        title.encode('utf-8').decode('utf-8'))  # 返回窗口标题为阴阳师-网易游戏的句柄
    # 获取窗口大小参数
    _, _, width, high = win32gui.GetClientRect(hld)
    # 获取窗口位置参数
    left, top, right, botton = win32gui.GetWindowRect(hld)

    @classmethod
    def set_parameter(cls):
        """ 改变初始参数 """
        _, _, cls.width, cls.high = win32gui.GetClientRect(cls.hld)
        cls.left, cls.top, cls.right, cls.botton = win32gui.GetWindowRect(
            cls.hld)

    @classmethod
    def click_here(cls, times, interval):
        for tm in range(times):
            pyg.click()
            time.sleep(interval)

    @classmethod
    def click(cls, position, clicks, interval):
        """
        执行左键点击，坐标已经模糊过+2*range
        返回Int型坐标
        """
        x = cls.random_range(position[0], 2)
        y = cls.random_range(position[1], 2)
        # 设置窗口从最小化退出
        win32gui.ShowWindow(cls.hld, win32con.SW_SHOWNORMAL)
        # 设置窗口置顶
        win32gui.SetForegroundWindow(cls.hld)
        print("当前鼠标位置[" + str(int(x)) + "，" + str(int(y)) + "]")
        pyg.click(int(x),
                  int(y),
                  clicks=clicks,
                  interval=interval,
                  button='left')

    @classmethod
    def create_start(cls, position, extent):
        """
        传入数组[x,y]
        entent 波动基数，缩放越小extent越小越不容易出界
        """
        x = extent * random.random() + position[0]
        y = extent * random.random() + position[1]
        return [x, y]

    @classmethod
    def wait_time(cls, one_time):
        """
        点击挑战后开始计时
        此时间 > 御魂显示时间:one_time（多少秒阵容）
        到结算界面结束
        """
        wait_time = one_time
        return wait_time

    @classmethod
    def random_range(cls, number, range):
        """ 将原值+/-2*[range）
            return 传入值类型（int或float）
        """
        number = number + random.random() * range + random.random() * range
        # 区分加减法
        if random.random() < 0.50:
            number = random.uniform(
                number - 0.5,
                number + random.random() * range + random.random() * range)
        elif random.random() >= 0.50:
            number = random.uniform(
                number + 0.5,
                number - random.random() * range - random.random() * range)
        return number

    @classmethod
    def random_time(cls, time):
        """ 将原时间波动
        """
        range = time + random.random()
        time = random.uniform(time, range)
        return time

    @classmethod
    def random_mouse(cls):
        """
        在战斗时，随机移动鼠标
        范围是屏幕分辨率内
        """
        # 设置鼠标移动坐标
        x = random.uniform(0 + 1, cls.screenWidth - 10)
        y = random.uniform(0 + 1, cls.screenhight - 10)
        # 移动鼠标
        pyg.moveTo(x, y)

    @classmethod
    def calculate_mouse_start(cls, role, name=title):
        """ 将鼠标设置在挑战按钮处(位置单人魂土挑战按钮)
            传入窗口标题
            return 鼠标坐标，交由pyautogui点击（可以增加偏移，防止检测）
            TODO 提供其他寻找窗口的选项：pid，句柄等
            role ={
                "1" : [xi=0.91304, yi=0.94538]
                "21-22": [xi=0.95304, yi=0.94538]
            }
        """
        dict = {
            "1": [0.91304, 0.94538],
            "21": [0.95304, 0.94538],
            "22": [0.95304, 0.94538]
        }
        # 返回鼠标在挑战按钮处坐标（float）
        # 按比例计算的位置，缩放仍可用
        if cls.if_moved():
            # 判断是否移动窗口
            cls.set_parameter()
        mouse_x = cls.left + cls.width * dict[role][0]
        mouse_y = cls.top + cls.high * dict[role][1]
        return [mouse_x, mouse_y]
        # win32api.SetCursorPos(
        #     [, ])

    @classmethod
    def calculate_mouse_center(cls, name=title):
        """ 将鼠标设置在窗口中心
            传入窗口标题
            return 鼠标坐标，交由pyautogui点击（可以增加偏移，防止检测）
            TODO 提供其他寻找窗口的选项：pid，句柄等
        """

        # # 返回鼠标在窗口中心位置（float）
        # win32api.SetCursorPos([left + width // 2, top + high // 2])
        if cls.if_moved():
            # 判断是否移动窗口
            cls.set_parameter()
        mouse_x = cls.left + cls.width / 2
        mouse_y = cls.top + cls.high / 2
        return [
            _Tools.random_range(mouse_x, 1),
            _Tools.random_range(mouse_y, 1)
        ]

    @classmethod
    def calculate_mouse_end(cls, xi=0.86304, yi=0.94538, name=title):
        """ 将鼠标设置在挑战按钮左侧偏移（）
            传入窗口标题
            return 鼠标坐标，交由pyautogui点击（可以增加偏移，防止检测）
            TODO 提供其他寻找窗口的选项：pid，句柄等
        """
        # 返回鼠标在挑战按钮处坐标（float）
        # 按比例计算的位置，缩放仍可用
        if cls.if_moved():
            # 判断是否移动窗口
            cls.set_parameter()
        xi = random.uniform(xi-0.15, xi)
        yi = random.uniform(yi-0.15, yi)
        mouse_x = cls.left + cls.width * xi
        mouse_y = cls.top + cls.high * yi
        return [mouse_x, mouse_y]

    @classmethod
    def start_click(cls, one_time, role, clicks=2, interval=0.5):
        """ 开始界面的所有点击
            one_time:阵容时间
            clicks：点击次数
            interval：点击间隔
        """
        # 由窗口获得挑战按钮位置
        start = cls.calculate_mouse_start(role)
        one_time = cls.random_range(one_time, 1)
        cls.click(start, clicks, interval)

    @classmethod
    def end_click(cls,
                  click_last=2,
                  interval_last=1,
                  click_first=3,
                  interval_first=2):
        """ 结束界面的所有点击
            参数1：点击次数
            参数2：点击间隔
        """
        end = cls.calculate_mouse_end()
        # 点击三次退出一局
        cls.click(end, click_first, interval_first)
        # 最后增加挑战按钮偏左位置的双击，保证退出一局
        cls.click(end, click_last, interval_last)

    @classmethod
    def if_moved(cls):
        """ 每次点击前需判断窗口是否被移动 """
        left, top, _, _ = win32gui.GetWindowRect(cls.hld)
        if left == cls.left and top == cls.top:
            return False
        return True

# def pic_begin() :
#     path = os.getcwd()
#     new_path = path + '\\autoClick\\'

#     while True :

#         s_pos = pyg.locateOnScreen(new_path + 'start.png',grayscale=True)
#         print(s_pos)
#         if s_pos != None :
#             s_x, s_y = pyg.center(s_pos)
#             pyg.moveTo(s_x,s_y)
#             # pyg.click(s_x, s_y, clicks=1, interval=0.0, button='left')
#             print(s_x,s_y)

#         # pos = pyg.locateOnScreen(new_path + 'finish.jpg')
#         # if pos != None :
#         #     x, y = pyg.center(pos)
#         #     # pyg.click(x, y)
#         #     print(x,y)
