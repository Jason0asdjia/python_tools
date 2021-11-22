from src.onmyoji_logic import OnmyojiLogic

if __name__ == '__main__':
    # 魂土
    # old:鼠标位置（挑战按钮中间位置信息），魂土阵容秒数,副本名称,次数
    # now:魂土阵容秒数,副本名称,情况/角色,次数
    """ 情况字典
        dict = {
            "1" : "单人作队长",
            "21" : "组队作队长",
            "22" : "组队非队长：进入插画启动程序"
        }
    """
    OnmyojiLogic.begin(22, "hun11", "21", 10)
