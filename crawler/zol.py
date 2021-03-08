# -*- coding: utf-8 -*-
"""
Created on Fri Mar  5 14:31:49 2021
@author: leemeany
"""

import requests
from bs4 import BeautifulSoup
import re

import sys
import csv
import time

import os

product_name = "hannspree"
url = "https://detail.zol.com.cn/digital_tv/"+ product_name +"/"

funList = ["server"]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36",
    "Content-Type": "text/html; charset=GBK"
}

def request_zol(url):
    request_session = requests.session()
    request_session.headers.update(headers)
    response = request_session.get(url = url)
    if response.status_code == 200:
        text = str(response.content,encoding='gbk')
        #获取本页所有页数
        text = str(response.content,encoding='gbk')
        #本页产品列表循环
        soup = BeautifulSoup(text, 'lxml')
        css = 'html body div.wrapper.clearfix div.content div.page-box div.pagebar a'
        page_list = list(map(lambda x: x.text, soup.select(css)))
        if page_list[-1] == '下一页':
            total_page = page_list[-2]
            current_page = 1
            create_dir('.\\' + product_name)
            print('download start...')
            for current_page in range(1,int(total_page) + 1):
                get_page_products(url + str(current_page) + ".html")
            print('download complete...')
    else:
        print('request error')
        
#获取本页所有产品        
def get_page_products(url):
    request_session = requests.session()
    request_session.headers.update(headers)
    response = request_session.get(url = url)
    if response.status_code == 200:
        text = str(response.content,encoding='gbk')
        #本页产品列表循环
        soup = BeautifulSoup(text, 'lxml')
        css = 'html body div.wrapper.clearfix div.content div.pic-mode-box ul#J_PicMode li'
        products_list = list(map(lambda x: get_content(x), soup.select(css)))
        for product in products_list:
            if product:
                #print(product["alt"]+ ":" + product[".src"])

                download_image(product[".src"],product["alt"])
        
    else:
        print('request error')
        
def get_content(x):
    if x.a:
        return x.a.img
    else:
        return None
    
def download_image(image_url,image_name):
    r = requests.get(image_url,headers=headers,stream = True)
    if r.status_code == 200:
        open('.\\' + product_name + '\\' + image_name + '.jpg','wb').write(r.content)
    del r
    
def create_dir(path):
    path = path.strip()
    path = path.rstrip("\\")
    isExists = os.path.exists(path)
    
    if not isExists:
        os.makedirs(path)
    else:
        print('目录已存在')
                
request_zol(url)        
    



