# -*- coding:UTF-8 -*-
import requests
import re
from rich.progress import track
from bs4 import BeautifulSoup as bs


class download_novel:
    """
    函数说明:类初始化
    Parameters:
        catalog - 章节目录保存地址(txt))
        server - 小说网站主页
        target - 具体小说页面
    Returns:
        
    Modify:
        2021-11-22
    """
    def __init__(self):
        self.catalog = "./crawler/catalog.txt"
        # 网站首页
        self.server = 'http://www.biqukan.com'
        # 《伏天氏》小说页面
        self.target = 'https://www.bqktxt.com/0_243/'
        # 存放章节名和对应内容
        self.dic = {}

    """
    函数说明:保存目录和各章节网址
    Parameters:
        self:类对象
    Returns:
        txt:保存到文本中
    Modify:
        2021-11-22
    """

    def get_catalog(self):
        req = requests.get(url=self.target)
        # 根据网站header-meata中的charset配置
        req.encoding = 'gbk'
        html = req.text
        soup = bs(html, 'html.parser')
        div = soup.find_all('div', class_='listmain')
        # 获取到所有章节链接
        a = bs(str(div[0])).find_all('a')
        with open(self.catalog, 'w') as f:
            # 删除最新章节部分影响目录顺序
            for _a in a[12:]:
                f.write(_a.string + "  " + self.server + _a.get('href') + '\n')

    """
    函数说明:获取各章节下载连接、初始化字典
    Parameters:
        self:类对象
    Returns:
        dic:章节目录对应链接
    Modify:
        2021-11-22
    """

    def get_download_urls(self):
        req = requests.get(url=self.target)
        # 根据网站header-meata中的charset配置
        req.encoding = 'gbk'
        html = req.text
        soup = bs(html, 'html.parser')
        div = soup.find_all('div', class_='listmain')
        # 获取到所有章节链接
        a = bs(str(div[0])).find_all('a')
        for _a in a[12:]:
            self.dic[_a.string] = self.server + _a.get('href')

    """
    函数说明:获取章节内容
    Parameters:
        self:类对象
        target:各章节链接
    Returns:
        txt:下载的小说
    Modify:
        2021-11-22
    """

    def get_content(self, target):
        req = requests.get(url=target)
        # 根据网站header-meata中的charset配置
        req.encoding = 'gbk'
        html = req.text
        soup = bs(html, 'html.parser')
        div = soup.find_all('div', class_='showtxt')
        # 去除下方链接、在段落间添加换行符
        # TODO暂将"　"替换为换行符
        content = re.sub('\(http.*', "",
                         div[0].text).strip().replace("　" * 2, '\n\n')
        return content

    """
    函数说明:下载小说
    Parameters:
        self:类对象
        path:小说存放路径
    Returns:
    Modify:
        2021-11-22
    """

    def download(self, path):
        with open(path, 'a', encoding='utf-8') as f:
            self.get_download_urls()
            for name, link in track(self.dic.items()):
                f.write("「" + name + "」" + '\n\n')
                f.writelines(self.get_content(link))
                f.write('\n\n\n')


if __name__ == '__main__':
    # download_novel().get_content("https://www.bqktxt.com/0_243/387379078.html")
    download_novel().download("./crawler/novel.txt")