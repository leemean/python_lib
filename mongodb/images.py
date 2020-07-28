# -*- coding: utf-8 -*-

from pymongo import MongoClient
from gridfs import GridFS
import requests
import os


class MongoDBClient:
    def __init__(self):
        self.client = MongoClient('')
        self.db = self.client.mzitu

    def upload_images(self):
        # fs = GridFS(self.db, collection="images")
        dirs = r"C:\Code\leemean\python_programs\mongodb\images"
        files = os.listdir(dirs)
        for file in files:
            filename = dirs + '\\' + file
            f = file.split('.')
            datatemp = open(filename, 'rb')
            imgput = GridFS(self.db)
            insertimg = imgput.put(datatemp, content_type=f[1], filename=f[0])
            datatemp.close()

    def download_images(self):
        gridFS = GridFS(self.db, collection="fs")
        count = 0
        for grid_out in gridFS.find():
            count += 1
            print(count)
            data = grid_out.read()
            outf = open("outpic" + str(count) + ".jpg", 'wb')
            outf.write(data)
            outf.close()


mongo = MongoDBClient()
mongo.upload_images()
mongo.download_images()

# keyword argument
# client = MongoClient('example.com',
#                      username='user',
#                      password='password',
#                      authSource='the_database',
#                      authMechanism='SCRAM-SHA-1')
# MongoDB URI
