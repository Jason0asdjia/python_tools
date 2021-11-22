import threading
from src._Tools import _Tools


class ThreadRandom(threading.Thread):
    """ 
    子线程类
    用于在战斗时，随时随地移动鼠标
    在主线程结束时，无论该线程什么状态都返回
    """

    def __init__(self, event):
        super().__init__()
        self.event = event

    def run(self):
        while not self.event.is_set():
            _Tools.random_mouse()
            # print("移动一次鼠标")
            # print("当前线程id" + str(os.getpid()))
            # 每5-10s移动一次鼠标
            self.event.wait(_Tools.random_range(5, 5))
