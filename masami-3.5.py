# -*- coding: utf-8 -*-
##############################
# by fermi
# 爬取豆瓣影人图片 例子：新垣结衣
###############################
import os
import re
import urllib
import urllib.request
from urllib.request import urlopen

import requests
from bs4 import BeautifulSoup

headers = {
    "referer": "https://movie.douban.com/",
    # 自己使用的浏览器
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0",
}


def getAllImageLink(url):
    response = urllib.request.Request(url, headers=headers)
    html = urlopen(response).read()
    soup = BeautifulSoup(html, "html.parser")

    # movie: cover, thumb->raw, 30
    # 用户相册: photo_wrap, /m/->/l/, 18
    divResult = soup.findAll('div', attrs={"class": "photo_wrap"})
    for div in divResult:
        imageEntityArray = div.findAll('img')
        for image in imageEntityArray:
            link = image.get('src')
            print(link)
            newLink = re.sub(r'/m/', '/l/', link)
            newLink_webp = re.sub(r'.jpg', '.webp', newLink)

            print(newLink)
            imageName = newLink[-15:]
            print(imageName)
            fileSavePath = './aragaki/%s' % imageName
            with open(fileSavePath, mode="wb") as f:
                # 将 jpg 图片写入在目标文件夹创建的文件
                f.write(requests.get(newLink, headers=headers).content)
            print(fileSavePath)

            print(newLink_webp)
            imageName = newLink_webp[-15:]
            print(imageName)
            fileSavePath = './aragaki/%s' % imageName
            with open(fileSavePath, mode="wb") as f:
                # 将 webp 图片写入在目标文件夹创建的文件
                f.write(requests.get(newLink_webp, headers=headers).content)
            print(fileSavePath)


def startSpider(url):
    # 启动爬虫
    try:
        os.mkdir("./aragaki/")
        print("目录创建成功")
    except FileExistsError:
        print("目录已经存在")
    url_process = url.split("&", 2)  # 分解目标url
    print(url_process)
    for x in range(0, 18 * 21, 18): # 每页图数: 18, 页数 21
        print("正在爬取第%s页..." % ((x / 18) + 1))
        url_new = url_process[0] + "?" + "m_start=" + \
                  str(x)
                  #+ "&" + url_process[2]  # 重组获得下一页的目标url
        print(url_new)
        getAllImageLink(url_new)
    print("完成，已爬完所以图片！")


if __name__ == '__main__':
    # 链接可以替换成你像爬取得豆瓣明星图片！
    startSpider('https://www.douban.com/photos/album/1872953257/')
    #startSpider('https://movie.douban.com/celebrity/1018562/photos/?type=C&start=0&sortby=vote&size=a&subtype=a')
