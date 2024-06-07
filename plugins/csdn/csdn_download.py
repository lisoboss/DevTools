#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Zimo
# @Time    : 2024/6/7 11:09
# @File    : csdn_download.py
# @Software: PyCharm
# @contact : 2319899766@qq.com
# @Site    : https://blog.csdn.net/qq_39799322

import requests
import parsel
import tomd
import os
import re


def spider_csdn(title_url, path):  # 目标文章的链接

    def download_img(title, link):
        file_name_re = re.compile('cn/(.*)\?')
        try:
            file_name = re.findall(file_name_re, link)[0]
        except Exception as e:
            file_name = re.findall(re.compile('net/(\d+)\?'), link)[0] + ".png"
        head = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36 Edg/84.0.522.52",
            "Referer": "https://blog.csdn.net/tansty_zh"
        }
        res = requests.get(url=link, headers=head).content
        print(path + "/" + title + ".assets/" + file_name)
        with open(path + "/" + title + ".assets/" + file_name, "wb") as f:
            f.write(res)
            f.flush()

    def zhengli_img(title, text):
        # text = text.replace("<img", "&&&<img").replace('" alt="在这里插入图片描述">', '" alt="在这里插入图片描述">&&&')
        img_src_re = re.compile('img src="(.*?)" alt')
        img_src = re.findall(img_src_re, text)
        print(img_src)
        # 下载所有图片
        for link in img_src:
            # time.sleep(2)
            download_img(title, link)
            try:
                text = text.replace('<img src="' + link + '" alt="在这里插入图片描述"style="">',
                                    '![在这里插入图片描述](' + title + '.assets/' +
                                    re.findall(re.compile("cn/(.*?)\.png"), link)[0] + '.png)')
                text = text.replace('<img src="' + link + '" alt=""style="">',
                                    '![在这里插入图片描述](' + title + '.assets/' +
                                    re.findall(re.compile("cn/(.*?)\.png"), link)[0] + '.png)')

            except:
                text = text.replace('<img src="' + link + '" alt="在这里插入图片描述"style="">',
                                    '![在这里插入图片描述](' + title + '.assets/' +
                                    re.findall(re.compile("net/(\d+)\?watermark"), link)[0] + '.png)')
                text = text.replace('<img src="' + link + '" alt=""style="">',
                                    '![在这里插入图片描述](' + title + '.assets/' +
                                    re.findall(re.compile("net/(\d+)\?watermark"), link)[0] + '.png)')
        return text
        # 将之前的图片进行替换
        # '<img src="https://img-blog.csdnimg.cn/ad125850b658456aa040aadc1bfe71c9.png" alt="在这里插入图片描述"style="">','![在这里插入图片描述](IOS - 某驾宝典篇.assets/b3ab2391d5b2433b958fdd939acdf07a.png)'

    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36 Edg/84.0.522.52",
        "Referer": "https://blog.csdn.net/tansty_zh"
    }
    html = requests.get(url=title_url, headers=head).text
    page = parsel.Selector(html)
    # 创建解释器
    title = page.css(".title-article::text").get().replace(" ", "")
    os.makedirs(title + ".assets", exist_ok=True)
    content = page.css("article").get()
    content = re.sub("<a.*?a>", "", content)
    content = re.sub("<br>", "", content)
    content = re.sub("<", "<", content)  # 新增
    content = re.sub(">", ">", content)  # 新增
    # print(content)
    text = tomd.Tomd(content).markdown
    text_succ = zhengli_img(title, text).replace("<!-- -->", "")
    print(text_succ, type(text_succ))
    # 转换为markdown 文件

    try:
        os.mkdir(path)
        print('创建成功！')
    except:
        print('目录已经存在或异常')

    with open(path + f"/" + title + ".md", mode="w", encoding="utf-8") as f:
        f.write("#" + title)
        f.write(text_succ)
