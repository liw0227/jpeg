import os

# 查找文件夹下所有黑乎乎
def get_img_file(file_name):
    imagelist = []
    for parent, dirnames, filenames in os.walk(file_name):
        for filename in filenames:
            if filename.lower().endswith('.jpg'):
                imagelist.append(os.path.join(parent, filename))
    return imagelist


print(len(get_img_file('/Volumes/未命名/备份/无人机原始照片/')))
