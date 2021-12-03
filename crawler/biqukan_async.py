import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import asyncio
import requests
import parsel
import httpx

from lxml import etree
from tools.headers import GetCookies, GetUserAgent
from rich.progress import track

HEADERS = {}
HEADERS['User-Agent'] = GetUserAgent()
HEADERS['Referer'] = "https://www.bqktxt.com/"

BASEURL = "https://www.bqktxt.com"
"""
获取小说章节链接
"""


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
        # await asyncio.wait(task)
        await asyncio.gather(*task)


"""
获取每章节内容
httpx发送异步请求
"""


async def get_text(client, name, link):
    # async with httpx.AsyncClient() as client:
    req = await client.get(link, headers=HEADERS)
    html = etree.HTML(req.text)
    text = html.xpath('//*[@id="content"]/text()')
    await save_text(name, text[:-2])


"""
写入文件
TODO：存入文件乱序
    加入一个“缓存”队列，使用TODO:多线程取值
    使用标识，比当前表示大一，写入
    
当前处理方式：对存入的各章节文件在进行读取，同时进行排序合并为一个文件
"""


async def save_text(name, text):
    #TODO:文件目录更方便由用户创建
    path = "./python_tools/crawler/novel-伏天氏"
    if not os.path.exists(path):
        os.mkdir(path)
    f = open(f'{path}/{name}.txt', 'a', encoding='utf-8')
    # async with open(f"./result/{name}.txt", 'w', encoding="utf-8") as f:
    for texts in track(text):
        f.write(texts)
        f.write('\n\n')
        print(f'正在爬取{name}')


if __name__ == '__main__':
    url = 'https://www.bqktxt.com/0_243/'
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_link(url))