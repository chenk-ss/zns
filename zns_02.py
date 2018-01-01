#!/user/bin/python3
#-*-coding:UTF-8-*-

#爬取http://yxpjw.club/index.html图片
#通过链接获取

import requests
import re
import os
from lxml import html

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
}

#获取当前文件路径
path=os.path.abspath('.')

img=[]

def open_url(url):
    response = requests.get(url,headers=headers).content
    sel = html.fromstring(response)
    bb=sel.xpath('//h1[@class="article-title"]/text()')
    #bb=sel.xpath('//p[@class="focus"]/a/@href')
    #获取标题和图片个数
    #name='摄影师EROONICHAN出品8月无圣光套图'
    #num=102
    for i in bb:
        try:
            name=i.split('[')[-2].split(']')[-1]
            num=i.split(name)[-1].split('[')[-1].split('P]')[-2]
        except Exception:
            print('没有获取到文件名！！！！！')
            pass
        print('标题：'+name+'['+str(num)+'P]')

    #全局变量img
    global img
    img=[]

    url=url.split('.html')[-2]
    print(url)

    #通过图片个数判断有多少页，默认每页三张图片
    get_url(url+'.html')
    for num1 in range(2,int(num)//3+2):
        get_url(url+'_'+str(num1)+'.html')

    #将路径设置为之前定义的路径下
    os.chdir(path)
    # 新建文件夹
    try:
        os.mkdir(name+'['+str(num)+'P]')
    except Exception:
        pass
    os.chdir(name+'['+str(num)+'P]')
    #下载
    for img in img:

        name=img.split('/')[-1]
        print('正在下载：'+img)
        with open(name, "wb+") as jpg:
                jpg.write(requests.get(img, headers=headers).content)
    
    print('---------------------------------------------------')
    print('下载完成')



def get_url(url):
    #print(url)
    try:
        response = requests.get(url,headers=headers).content
        sel = html.fromstring(response)
        #获取图片链接
        aa=sel.xpath('//p/img/@src')
        global img
        for i in aa:
            print(i)
            img.append(i)
    except Exception:
        pass



if __name__=='__main__':
    while(True):
        try:
            url=input('请输入url：')
            url='http://yxpjw.me/'+url.split('club/')[-1]
            open_url(url)
        except Exception:
            pass
