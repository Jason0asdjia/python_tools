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


def get_text(link):
    req = requests.get(link, headers=HEADERS)
    html = etree.HTML(req.text)
    print(type(html))
    text = html.xpath('//*[@id="content"]/text()')
    print(text)


async def get_link(url):
    req = requests.get(url, headers=HEADERS)
    req.encoding = 'gbk'
    Xpath = parsel.Selector(req.text)
    # title and link
    dd = Xpath.xpath('/html/body/div[4]')
    # extract()--> return a list
    links = Xpath.xpath('/html/body/div[4]/dl/dd/a/@href').extract()
    # print(links)
    full_links = [BASEURL + link for link in links]
    # print(full_links)
    names = Xpath.xpath('/html/body/div[4]/dl/dd/a/text()').extract()
    name_list = [name.strip() for name in names]
    # print(names)
    name_link = zip(full_links, name_list)
    async with httpx.AsyncClient() as client:
        task = []
        for link, name in name_link:
            task.append(get_text(client, name, link))
        await asyncio.wait(task)


# def get_text(name, link):
#     with httpx.Client() as client:
#         req =  client.get(link, headers=HEADERS)
#         html = etree.HTML(req.text)
#         text = html.xpath('//*[@id="content"]/text()')
#         print(text)
async def get_text(client, name, link):
    # async with httpx.AsyncClient() as client:
    response = await client.get(link)
    # print(response.text)
    # print(response.status)
    html = etree.HTML(response.text)
    # print(html)
    # text = html.xpath('/html/body/div[4]/div[2]')
    text = html.xpath('//*[@id="content"]/text()')
    print(text[:-2])


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_link("https://www.bqktxt.com/0_243/"))
    #get_text("https://www.bqktxt.com/0_243/387379078.html")
    #get_link("https://www.bqktxt.com/0_243/387379078.htm")
    # get_text("","https://www.bqktxt.com/0_243/387379078.html")