# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 17:09:09 2020

@author: minglee

安装tesseract：https://digi.bib.uni-mannheim.de/tesseract/

"""


import re
from PIL import Image
import pytesseract
from selenium import webdriver
import time
import win32gui
import win32print
import win32con
import win32api

class VerificationCode:
    def __init__(self):
        self.driver = webdriver.Chrome('E:\webdriver\chromedriver.exe')
        self.find_element = self.driver.find_element_by_css_selector
        
    #获取验证码
    def get_picture(self):
        self.driver.maximize_window()
        self.driver.get('https://www.flightontime.cn/')
        self.driver.save_screenshot('1.png')
        page_snap_obj = Image.open('1.png')
        img = self.find_element("img#imgValidationCode")
        time.sleep(1)
        location = img.location
        size = img.size
        left = location['x']
        top = location['y']
        right = left + size['width']
        bottom = top + size['height']
        #缩放转换，因为有的电脑分辨率太高进行缩放后实际分辨率和获取的分辨率不一致，导致截图位置错误。
        hDC = win32gui.GetDC(0)
        HORZRES = win32print.GetDeviceCaps(hDC, win32con.DESKTOPHORZRES)
        screen_scale_rate = round(HORZRES / win32api.GetSystemMetrics(0), 2)  #1.25
        #print(screen_scale_rate)
        #print(left,top,right,bottom)
        #print(left*screen_scale_rate,top*screen_scale_rate,right*screen_scale_rate,bottom*screen_scale_rate)
        image_obj = page_snap_obj.crop((left*screen_scale_rate,top*screen_scale_rate,right*screen_scale_rate,bottom*screen_scale_rate))
        image_obj.show()
        self.driver.close()
        return image_obj
    
    #灰度处理
    def processing_image(self):
        image_obj = self.get_picture() #获取图片
        img = image_obj.convert("L") #转灰度
        pixdata = img.load()
        w,h = img.size
        threshold = 160
        for y in range(h):
            for x in range(w):
                if pixdata[x,y] < threshold:
                    pixdata[x,y] = 0
                else:
                    pixdata[x,y] = 255
        return img
    
    #去除噪点
    def delete_spot(self):
        images = self.processing_image()
        data = images.getdata()
        w, h = images.size
        black_point = 0
        for x in range(1, w - 1):
            for y in range(1, h - 1):
                mid_pixel = data[w * y + x]  # 中央像素点像素值
                if mid_pixel < 50:  # 找出上下左右四个方向像素点像素值
                    top_pixel = data[w * (y - 1) + x]
                    left_pixel = data[w * y + (x - 1)]
                    down_pixel = data[w * (y + 1) + x]
                    right_pixel = data[w * y + (x + 1)]
                    # 判断上下左右的黑色像素点总个数
                    if top_pixel < 10:
                        black_point += 1
                    if left_pixel < 10:
                        black_point += 1
                    if down_pixel < 10:
                        black_point += 1
                    if right_pixel < 10:
                        black_point += 1
                    if black_point < 1:
                        images.putpixel((x, y), 255)
                    black_point = 0
        # images.show()
        return images
    
    def image_transform_to_str(self):
        image = self.delete_spot()
        pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        result = pytesseract.image_to_string(image) #图片转文字
        resultj = re.sub(u"([^\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a])", "", result)  # 去除识别出来的特殊字符
        result_four = resultj[0:4]  # 只获取前4个字符
        # print(resultj)  # 打印识别的验证码
        return result_four
        
if __name__ == '__main__':
    a = VerificationCode()
    str = a.image_transform_to_str()
    print(str)
        
        


