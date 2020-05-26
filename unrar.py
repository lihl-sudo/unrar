#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# unrar.py

import rarfile
import zipfile
import fastzipfile
import os
import sys
import re
import shutil
from multiprocessing.dummy import Pool


def un_rar(file_name, pwd=None):
    """解压文件到当前路径"""
    target = file_name.split('.')[0]
    try:
        # if file_name.split('.')[-1] == 'rar':
        if rarfile.is_rarfile(file_name):
            files = rarfile.RarFile(file_name)
        else:
            files = zipfile.ZipFile(file_name)
        file_list = files.namelist()
        po = Pool()
        for file in file_list:
            try:
                # rar.extractall(path=target, pwd=None)
                po.apply_async(files.extract(file, target, None))
            except Exception:
                # rar.extractall(path=target, pwd=pwd)
                po.apply_async(files.extract(file, target, pwd))
        # for zip_file in zip.namelist():
        #     try:
        #         print(zip.filelist)
        #         zip_file = zip_file.encode('cp437').decode('utf-8')
        #         print(zip_file)
        #         print(zip.namelist())
        #
        #     except Exception as e:
        #         print(e)
        #         print('7')
        #         try:
        #             zip_file = zip_file.encode('utf-8').decode('utf-8')
        #         except Exception as i:
        #             print(i)
    except Exception as e:
        print(e)
        print(f'Fail:{file_name}')
    else:
        print(f'Success:{file_name}')
        po.close()


def point_file_name(path):
    """获取压缩文件路径"""
    return [os.path.join(item[0], file_name)
            for item in os.walk(path)
            for file_name in item[-1]
            if re.search(r'.rar$|.zip$', file_name)]


def get_pwd():
    """从终端输入获取密码"""
    pwd = ""
    if len(sys.argv) > 2:
        if sys.argv[2] != "rm":
            pwd = sys.argv[2].encode('gbk')
        elif sys.argv[2] == "rm":
            if len(sys.argv) == 4:
                pwd = sys.argv[3].encode('gbk')
    return pwd


def rm_file(files):
    """删除源文件"""
    if len(sys.argv) > 2:
        if sys.argv[2] == "rm":
            for file in files:
                os.remove(file)


if __name__ == '__main__':
    path = sys.argv[1]
    pwd = get_pwd()
    # with open(r'UnRAR.exe','rb') as f:
    #     with open(os.path.join(path,'UnRAR.exe'),'wb') as other:
    #         other.write(f.read())
    file_names = point_file_name(path)
    while file_names:
        pool = Pool()
        pool.starmap_async(un_rar, zip(file_names, [pwd] * len(file_names)))
        pool.close()
        pool.join()
        rm_file(file_names)
        for name in file_names:
            file_names = point_file_name(name.split(".")[0])
