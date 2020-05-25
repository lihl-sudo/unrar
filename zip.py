import os, zipfile


print("解压完成，开始转换编码了....")
'change charset'
for root_path, dir_names, file_names in os.walk('.'):
    # print("xx", file_names)
    for fn in file_names:
        path = os.path.join(root_path, fn)
        if not zipfile.is_zipfile(path):
            print("before:", fn)
            try:
                fn = fn.encode('cp437').decode('utf-8')
                print("after:", fn)
                new_path = os.path.join(root_path, fn)
                os.rename(path, new_path)
            except Exception as e:
                print('error:', e)
