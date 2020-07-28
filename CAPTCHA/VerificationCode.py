# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 17:09:09 2020

@author: minglee
"""

import re
from PIL import Image
import pytesseract
from selenium import webdriver
import time

class VerificationCode:
    def __init__(self):
        self.driver = webdriver.Chrome('C:\Programs\webdriver\chromedriver.exe')
        self.find_element = self.driver.find_element_by_css_selector
        
    def get_picture(self):
        self.driver.get('https://www.flightontime.cn/')
        self.driver.save_screenshot('1.png')
        page_snap_obj = Image.open('1.png')
        img = self.find_element("input[type='image']")
        time.sleep(1)
        location = img.location
        size = img.size
        left = location['x']
        top = location['y']
        right = left + size['width']
        bottom = top + size['height']
        print(left,top,right,bottom)
        image_obj = page_snap_obj.crop((left,top,right,bottom))
        image_obj.show()
        self.driver.close()
        return image_obj


vc = VerificationCode()
vc.get_picture()
        
        


