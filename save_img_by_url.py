# -*- coding: utf-8 -*-
# @File    : urlencode.py
# @Date    : 2019/9/26
# @Author  : HiCooper
# @Desc    :
import requests


def read_save(img_url):
    resp = requests.get(img_url)
    image = resp.content
    f = open('./1.jpg', 'wb')
    f.write(image)
    f.close()


if __name__ == '__main__':
    url = 'http://10.50.12.38:8077/ajax/bucket/file/pudong/310115-111-02/经营范围/1/1_1.jpg'
    # url = 'http://10.50.12.37/sjtu_image/201807/23/913982920c74482eb88fa8fa83a5e7cc.jpg'
    # url = 'http://10.50.12.38:8077/ajax/bucket/file/pudong/banner_bg.jpg'
    read_save(url)
