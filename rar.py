#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# rar.py

from multiprocessing.dummy import Pool, RLock
# from multiprocessing import RLock
import zipfile
import fastzipfile
import os
import sys


class Zip:
    def __init__(self, file_name, pwd=None):
        self.file_name = file_name
        self.path = file_name.split('.')[0]
        self.lock = RLock()
        self.pwd = pwd
        self.zip = zipfile.ZipFile(self.file_name)
        self.zip.setpassword(pwd=self.pwd)
        self.files = self.zip.namelist()

    # def get_file(self):
    #     for self.file in self.files:
    #         yield self.file

    def un_zip(self, file):
        # with self.lock:
        self.zip.extract(file, self.path)

    def extr_all(self):
        self.zip.extractall(path=self.path, pwd=self.pwd)


if __name__ == "__main__":
    file_name = r"/Users/lihailong/Desktop/未命名文件夹/用户画像.zip"
    orpwd = "cnd2018知识库"
    pwd = orpwd.encode("gbk")
    unzip = Zip(file_name, pwd)
    po = Pool(10)
    files = unzip.files
    # unzip.extr_all()
    po.starmap_async(unzip.un_zip, zip(files))
    po.close()
    po.join()
