# -*- coding: utf-8 -*-
"""
Created on Sat Feb 29 14:55:54 2020

@author: Administrator
"""

import os

def getAllFileAndDirectorySize(filePath,size = 0):
    for root,dirs,files in os.walk(filePath):
        for f in files:
                size += os.path.getsize(os.path.join(root,f))
    return str(round(size / (1024 * 1024) ,2)) + "M"

def getCurrentFolders(path):
    with os.scandir(path) as dirlist:
        for dir in dirlist:
            if(dir.name not in {'Microsoft','OneDrive','Packages'}):
                target_path = os.path.join(path,dir)
                print(target_path,getAllFileAndDirectorySize(target_path))
    

#print(getAllFileAndDirectorySize("D:\\folder1\\folder2\\"))
getCurrentFolders(r"C:\ProgramData")


