# 使用pyautogui 实现windows自动点击
import time
import os
import threading

from src._Tools import _Tools
from src._Thread import ThreadRandom
from src._ProgressBar import _ProgressBar
import keyboard as kb


class OnmyojiLogic(object):
    @classmethod
    def begin(cls, one_time, name, role, times):
        """
        开始多局
        鼠标位置，魂土阵容秒数,副本名称,次数
        11-魂土
        """
        # 各副本对应函数
        # TODO 完善其他副本
        print("华人牌导航为您服务~")
        excute = {
            "hun11": lambda one_time, role: cls.begin_hun11(one_time, role)
        }
        progress = _ProgressBar(times, fmt=_ProgressBar.FULL)
        for tm in range(times):
            # 执行函数
            excute[name](one_time, role)
            # 每局结束增加缓和时间
            time.sleep(0.4)
            # 显示进度条
            progress.current += 1
            progress()
            time.sleep(0.1)
        progress.done()
        print("导航结束，祝您生活愉快，下次再见~")

    @classmethod
    def begin_hun11(cls, one_time, role):
        """
        开始一局
        鼠标位置，魂土阵容秒数
        """
        # 各个情况对应函数

        excute = {
            "1": lambda one_time, role: cls.begin_single(one_time, role),
            "21": lambda one_time, role: cls.begin_team_1(one_time, role),
            "22": lambda one_time, role: cls.begin_team_2(one_time - 2, role)
        }
        # 执行对应副本，传入阵容时间和角色/情况
        excute[role](one_time, role)

    @classmethod
    def sleep_main(cls, one_time):
        """ 此时随机移动鼠标 5-10s一次
        开始战斗，进入休眠状态
        每次开局都新建一个线程 
        """
        event = threading.Event()
        thread_random = ThreadRandom(event)
        thread_random.start()

        # 主线程休眠
        # 波动休眠时间
        time.sleep(_Tools.random_time(4.5) + one_time + 2)
        # 向鼠标随机移动线程发送通知 setEvent
        # 使其线程结束
        event.set()
        # 休眠状态结束，鼠标返回开始位置
        time.sleep(0.1)

    @classmethod
    def begin_single(cls, one_time, role):
        """ 单人做队长 """
        # 由窗口获得挑战按钮位置
        start = _Tools.calculate_mouse_start(role)
        # one_time = _Tools.random_range(one_time, 1)
        # _Tools.click(start, 2, 0.5)
        _Tools.start_click(one_time, role)
        cls.sleep_main(one_time)
        _Tools.click(start, 3, 2)
        # 最后增加中间位置的双击，保证退出一局
        center = _Tools.calculate_mouse_center()
        _Tools.click(center, 2, 1)

    @classmethod
    def begin_team_1(cls, one_time, role):
        """ 多人组队作队长的情况 """
        _Tools.start_click(one_time, role)
        cls.sleep_main(one_time)
        _Tools.end_click()
        # end = _Tools.calculate_mouse_end()
        # _Tools.click(end, 3, 2)
        # _Tools.click(end, 2, 1)

    @classmethod
    def begin_team_2(cls, one_time, role):
        """ 多人组队不作队长的情况 """
        _Tools.start_click(one_time, role)
        cls.sleep_main(one_time)
        # 点击三次退出一局
        _Tools.end_click(3, 1)
