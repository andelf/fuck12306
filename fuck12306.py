#!/usr/bin/python
# #  FileName    : fuck12306.py
# #  Author      : ShuYu Wang <andelf@gmail.com>
# #  Created     : Mon Mar 16 22:08:41 2015 by ShuYu Wang
# #  Copyright   : Feather (c) 2015
# #  Description : fuck fuck 12306
# #  Time-stamp: <2015-03-16 22:08:54 andelf>


from PIL import Image
import urllib
import urllib2
import re
import json
# hack CERTIFICATE_VERIFY_FAILED
# https://github.com/mtschirs/quizduellapi/issues/2
import ssl
if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context


UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36"

pic_url = "https://kyfw.12306.cn/otn/passcodeNew/getPassCodeNew?module=login&rand=sjrand&0.21191171556711197"


def get_img():
    resp = urllib.urlopen(pic_url)
    raw = resp.read()
    with open("./tmp.jpg", 'wb') as fp:
        fp.write(raw)

    return Image.open("./tmp.jpg")


def get_sub_img(im, x, y):
    assert 0 <= x <= 3
    assert 0 <= y <= 2
    WITH = HEIGHT = 68
    left = 5 + (67 + 5) * x
    top = 41 + (67 + 5) * y
    right = left + 67
    bottom = top + 67

    return im.crop((left, top, right, bottom))


def baidu_stu_lookup(im):
    url = "http://stu.baidu.com/n/image?fr=html5&needRawImageUrl=true&id=WU_FILE_0&name=233.png&type=image%2Fpng&lastModifiedDate=Mon+Mar+16+2015+20%3A49%3A11+GMT%2B0800+(CST)&size="
    im.save("./query_temp_img.png")
    raw = open("./query_temp_img.png", 'rb').read()
    url = url + str(len(raw))
    req = urllib2.Request(url, raw, {'Content-Type':'image/png', 'User-Agent':UA})
    resp = urllib2.urlopen(req)

    resp_url = resp.read()      # return a pure url


    url = "http://stu.baidu.com/n/searchpc?queryImageUrl=" + urllib.quote(resp_url)

    req = urllib2.Request(url, headers={'User-Agent':UA})
    resp = urllib2.urlopen(req)

    html = resp.read()

    return baidu_stu_html_extract(html)

def baidu_stu_html_extract(html):
    #pattern = re.compile(r'<script type="text/javascript">(.*?)</script>', re.DOTALL | re.MULTILINE)
    pattern = re.compile(r"keywords:'(.*?)'")
    matches = pattern.findall(html)
    if not matches:
        return '[UNKOWN]'
    json_str = matches[0]

    json_str = json_str.replace('\\x22', '"').replace('\\\\', '\\')

    #print json_str

    result = [item['keyword'] for item in json.loads(json_str)]

    return '|'.join(result) if result else '[UNKOWN]'


if __name__ == '__main__':
    im = get_img()
    #im = Image.open("./tmp.jpg")
    for y in range(2):
        for x in range(4):
            im2 = get_sub_img(im, x, y)
            result = baidu_stu_lookup(im2)
            print (y,x), result
