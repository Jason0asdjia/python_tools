import re
import pyautogui as pyg
import random
import time
from src._Tools import _Tools
import pywintypes
import win32gui
import win32api
import win32con
import win32process
import psutil
import os

import cv2
""" 测试困28探索处理过程 """
# 采用图片匹配，匹配到打斗标志即点击


def imgAutoCick_start(tempFile, debug=False):
    '''
        temFile :需要匹配的小图
        whatDo  :需要的操作
                pyg.moveTo(w/2, h/2)# 基本移动
                pyg.click()  # 左键单击
                pyg.doubleClick()  # 左键双击
                pyg.rightClick() # 右键单击
                pyg.middleClick() # 中键单击
                pyg.tripleClick() # 鼠标当前位置3击
                pyg.scroll(10) # 滚轮往上滚10， 注意方向， 负值往下滑
        更多详情：https://blog.csdn.net/weixin_43430036/article/details/84650938
        debug   :是否开启显示调试窗口

        # 6种算法的列表
methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
            'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']

    '''
    # (0, 0, 738, 416)
    # (22, 233, 776, 688)
    hld = win32gui.FindWindow(None, u"阴阳师-网易游戏")  # 返回窗口标题为阴阳师-网易游戏的句柄
    # print(hld)
    _, _, width1, high1 = win32gui.GetClientRect(hld)
    # print(win32gui.GetClientRect(hld))
    left1, top1, right1, botton1 = win32gui.GetWindowRect(hld)
    # print(win32gui.GetWindowRect(hld))
    flag = False
    if width1 < 700:
        # win32gui.MoveWindow(hld, left1, top1, 738, 416, False)
        print("请放大窗口！")
        flag = True
        # 增加窗口判定
        while flag:
            _, _, width1, high1 = win32gui.GetClientRect(hld)
            if width1 >= 700:
                flag = False

    # 读取屏幕，并保存到本地
    # 设置只截取窗口屏幕，非全屏
    # region参数，截图区域，由左上角坐标、宽度、高度4个值确定，
    # 如果指定区域超出了屏幕范围，超出部分会被黑色填充，默认`None`,截全屏
    pyg.screenshot('big.png', region=(left1+10, top1, width1, high1+30))
    # pyg.screenshot('big.png')

    # 读入背景图片
    gray = cv2.imread("big.png", 0)
    # 读入需要查找的图片
    img_template = cv2.imread(tempFile, 0)

    # 得到图片的高和宽
    w, h = img_template.shape[::-1]

    # 模板匹配操作
    res = cv2.matchTemplate(gray, img_template, cv2.TM_SQDIFF)

    # 得到最大和最小值得位置
    # TM_SQDIFF结果在最小值中
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    left = min_loc[0]
    top = min_loc[1]
    # print("top-"+str(left)+"-left-"+str(top))

    x = [left, top, w, h]

    top_left = min_loc  # 左上角的位置
    bottom_right = (top_left[0] + w, top_left[1] + h)  # 右下角的位

    # 先移动再操作
    # print(str(left1+left+w/2)+"--"+str(top1+top+h/2))

    # if pyg.click(left1+left+w/2, top1+top+h/2) != None:
    # 判断坐标是否在窗口内
    """ 更改判断机制 """
    if left1+left+w/2 > 8 and left1+left+w/2 < 768 and top1+top+h/2 > 287 and top1+top+h/2 < 745:
        print(str(left1+left+w/2)+"--"+str(top1+top+h/2))
        pyg.click(left1+left+w/2, top1+top+h/2)
        return True
    print("没找到坐标")
    return False
    # whatDo(x)

    if debug:
        # 读取原图
        img = cv2.imread("big.png", 1)
        # 在原图上画矩形
        cv2.rectangle(img, top_left, bottom_right, (0, 0, 255), 2)
        # 调试显示
        img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5,
                         interpolation=cv2.INTER_NEAREST)
        cv2.imshow("processed", img)
        cv2.waitKey(0)
        # 销毁所有窗口
        cv2.destroyAllWindows()
    os.remove("big.png")


def imgAutoCick_win(tempFile, debug=False):
    '''
        temFile :需要匹配的小图
        whatDo  :需要的操作
                pyg.moveTo(w/2, h/2)# 基本移动
                pyg.click()  # 左键单击
                pyg.doubleClick()  # 左键双击
                pyg.rightClick() # 右键单击
                pyg.middleClick() # 中键单击
                pyg.tripleClick() # 鼠标当前位置3击
                pyg.scroll(10) # 滚轮往上滚10， 注意方向， 负值往下滑
        更多详情：https://blog.csdn.net/weixin_43430036/article/details/84650938
        debug   :是否开启显示调试窗口

        # 6种算法的列表
methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
            'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']

    '''
    # (0, 0, 738, 416)
    # (22, 233, 776, 688)
    hld = win32gui.FindWindow(None, u"阴阳师-网易游戏")  # 返回窗口标题为阴阳师-网易游戏的句柄
    # print(hld)
    _, _, width1, high1 = win32gui.GetClientRect(hld)
    # print(win32gui.GetClientRect(hld))
    left1, top1, right1, botton1 = win32gui.GetWindowRect(hld)
    # print(win32gui.GetWindowRect(hld))
    flag = False
    if width1 < 700:
        # win32gui.MoveWindow(hld, left1, top1, 738, 416, False)
        print("请放大窗口！")
        flag = True
        # 增加窗口判定
        while flag:
            _, _, width1, high1 = win32gui.GetClientRect(hld)
            if width1 >= 700:
                flag = False

    # 读取屏幕，并保存到本地
    # 设置只截取窗口屏幕，非全屏
    # region参数，截图区域，由左上角坐标、宽度、高度4个值确定，
    # 如果指定区域超出了屏幕范围，超出部分会被黑色填充，默认`None`,截全屏
    pyg.screenshot('big.png', region=(left1+10, top1, width1, high1+30))
    # pyg.screenshot('big.png')

    # 读入背景图片
    gray = cv2.imread("big.png", 0)
    # 读入需要查找的图片
    img_template = cv2.imread(tempFile, 0)

    # 得到图片的高和宽
    w, h = img_template.shape[::-1]

    # 模板匹配操作
    res = cv2.matchTemplate(gray, img_template, cv2.TM_SQDIFF)

    # 得到最大和最小值得位置
    # TM_SQDIFF结果在最小值中
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    left = min_loc[0]
    top = min_loc[1]
    # print("top-"+str(left)+"-left-"+str(top))

    x = [left, top, w, h]

    top_left = min_loc  # 左上角的位置
    bottom_right = (top_left[0] + w, top_left[1] + h)  # 右下角的位

    # 先移动再操作
    # print(str(left1+left+w/2)+"--"+str(top1+top+h/2))

    # if pyg.click(left1+left+w/2, top1+top+h/2) != None:
    # 判断坐标是否在画面比例的图标内
    # if left1+left+w/2 > 381 and left1+left+w/2 < 493 and top1+top+h/2 > 568 and top1+top+h/2 < 661:
    #     print(str(left1+left+w/2)+"--"+str(top1+top+h/2))
    #     pyg.click(left1+left+w/2, top1+top+h/2)
    #     return True
    #     # break
    # print("没找到坐标")
    # return False
    pyg.click(left1+left+w/2, top1+top+h/2)
    # whatDo(x)

    if debug:
        # 读取原图
        img = cv2.imread("big.png", 1)
        # 在原图上画矩形
        cv2.rectangle(img, top_left, bottom_right, (0, 0, 255), 2)
        # 调试显示
        img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5,
                         interpolation=cv2.INTER_NEAREST)
        cv2.imshow("processed", img)
        cv2.waitKey(0)
        # 销毁所有窗口
        cv2.destroyAllWindows()
    os.remove("big.png")


def click(left1, left, top1, top, w, h):
    flag = True
    while flag:
        if pyg.click(left1+left+w/2, top1+top+h/2) != None:
            flag = False
    print(str(left1+left+w/2)+"--"+str(top1+top+h/2))


def click_centerx(hld):
    """ 在画面没怪时点击窗口中心偏右位置 """
    _, _, width1, high1 = win32gui.GetClientRect(hld)
    left1, top1, right1, botton1 = win32gui.GetWindowRect(hld)
    pyg.click(left1+width1/2+100, top1+high1-80)
    print(str(left1+width1/2+100)+"=="+str(top1+high1-80))


async def logic():
    for _ in range(3):

        """ 点击顺序

            手动进入kun28-点击怪物头上战斗按钮
            点击胜利鼓图标
            点击结算达摩肚子
            整体结算时，点击纸人战利品
        """
        # pyg.PAUSE = 1
        for _ in range(4):
            click_centerx(hld)
            time.sleep(1)
        await imgAutoCick("autoClick\\smallfight2.png", False)
        time.sleep(2)
        await imgAutoCick("autoClick\\win.png", False)
        time.sleep(2)
        await imgAutoCick("autoClick\\result.png", False)
        # imgAutoCick("autoClick\\trophy.png", True)
if __name__ == '__main__':
    hld = win32gui.FindWindow(None, u"阴阳师-网易游戏")  # 返回窗口标题为阴阳师-网易游戏的句柄
    # 将代码窗口最小化
    # Minimize = win32gui.GetForegroundWindow()
    # win32gui.ShowWindow(Minimize, win32con.SW_MINIMIZE)

    # for _ in range(2):
    # imgAutoCick_start("autoClick\\static\\smallfight2.png", False)
    # """ 点击开始后，等两秒进行结算点击 """
    # time.sleep(5.5)
    imgAutoCick_win("autoClick\\static\\result.png", True)
    # while True:
    #     if imgAutoCick_win("autoClick\\static\\result.png", True):
    #         break
    # time.sleep(1)
    """ 点击后就出现达摩开门，可等一秒或点击一次 """
    # pyg.click()
    # imgAutoCick("autoClick\\static\\result.png", False)
    # # 异步测试u
    # import asyncio
    # loop = asyncio.get_event_loop()
    # res = loop.run_until_complete(logic())
    # loop.close()


# left(286, 385)
# right(376, 385)
# top(328, 340)
# bottom(328, 420)
