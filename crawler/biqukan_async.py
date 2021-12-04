import httpx
import parsel
import requests
import asyncio
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#
from tools.headers import GetCookies, GetUserAgent
from rich.progress import track
from lxml import etree

HEADERS = {}
HEADERS['User-Agent'] = GetUserAgent()
HEADERS['Referer'] = "https://www.bqktxt.com/"

BASEURL = "https://www.bqktxt.com"
"""
获取小说章节链接
"""
dic = {}

async def get_link(url):
    req = requests.get(url, headers=HEADERS)
    req.encoding = 'gbk'
    Xpath = parsel.Selector(req.text)
    # title and link
    # extract()--> return a list
    links = Xpath.xpath('/html/body/div[4]/dl/dd/a/@href').extract()
    full_links = [BASEURL + link for link in links]
    names = Xpath.xpath('/html/body/div[4]/dl/dd/a/text()').extract()
    name_list = [name.strip() for name in names]
    name_link = zip(full_links[12:], name_list[12:])
    async with httpx.AsyncClient() as client:
        task = []
        for link, name in name_link:
            task.append(get_text(client, name, link))
        await asyncio.wait(task)
        # await asyncio.gather(*task)
    save_text(name_list[12:])


"""
获取每章节内容
httpx发送异步请求
"""


async def get_text(client, name, link):
    # async with httpx.AsyncClient() as client:
    req = await client.get(link, headers=HEADERS, timeout=None)
    # print(req)
    html = etree.HTML(req.text)
    text = html.xpath('//*[@id="content"]/text()')
    await save_text_dic(name, text[:-2])


"""
写入文件->字典做临时缓存
"""
async def save_text_dic(name, texts):
    # temp = ""
    # # dic[name] = texts
    # for text in texts:
    #     temp += text + "\n\n"
    # TODO:百分比显示进度
    dic[name] = texts
    # print(f'正在载入{name}')



"""
写入文件
将已经写入dic缓存的text按照爬取的name_list顺序写入
"""


def save_text(name_list):
    # TODO:文件目录更方便由用户创建
    path = "./python_tools/crawler/novel"
    if not os.path.exists(path):
        os.mkdir(path)
    f = open(f'{path}/伏天氏.txt', 'a', encoding='utf-8')
    # async with open(f"./result/{name}.txt", 'w', encoding="utf-8") as f:
    for name in track(name_list):
        f.write(name)
        f.write('\n\n')
        for text in dic[name]:
            # print(text)
            f.write(text)
            f.write('\n\n')
        f.write('\n')

if __name__ == '__main__':
    url = 'https://www.bqktxt.com/0_243/'
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_link(url))
