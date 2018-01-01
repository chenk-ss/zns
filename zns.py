#!/user/bin/python3
#-*-coding:UTF-8-*-

#爬取http://yxpjw.club/index.html图片
#通过页数爬取

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
    urllist=[]
    namelist=[]
    numlist=[]
    response = requests.get(url,headers=headers).content
    sel = html.fromstring(response)
    #print(sel)
    #获取链接
    aa=sel.xpath('//h2/a[@target="_blank"]/@href')
    #获取标题和图片个数
    bb=sel.xpath('//h2/a[@target="_blank"]/text()')
    #bb=sel.xpath('//p[@class="focus"]/a/@href')

    for i in bb:
        name=i.split('[')[-2].split(']')[-1]
        num=i.split(name)[-1].split('[')[-1].split('P]')[-2]
        #print(name)
        namelist.append(name)
        #print(num)
        numlist.append(num)
    for i in aa:
        url=i.split('.html')[-2]
        urllist.append('http://yxpjw.me'+url)

        
    for i in range(0,10):
        print('标题：'+namelist[i])

        #全局变量img
        global img
        img=[]
        
        #通过图片个数判断有多少页，默认每页三张图片
        get_url(urllist[i]+'.html')
        for num in range(2,int(numlist[i])//5+2):
            #print(urllist[i])
            get_url(urllist[i]+'_'+str(num)+'.html')

        #将路径设置为之前定义的路径下
        os.chdir(path)
        # 新建文件夹
        os.mkdir(namelist[i]+'['+numlist[i]+'P]')
        os.chdir(namelist[i]+'['+numlist[i]+'P]')
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
            img.append(i)
    except Exception:
        pass

if __name__=='__main__':
    num=input('请输入页数：')
    url='http://yxpjw.me/page/'+num+'.html'
    open_url(url)
