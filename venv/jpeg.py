# coding=utf-8
import exifread
import re
import json
import requests
import os
import sys
import datetime
import xlrd


def latitude_and_longitude_convert_to_decimal_system(*arg):
    """
    经纬度转为小数, param arg:
    :return: 十进制小数
    """
    return float(arg[0]) + ((float(arg[1]) + (float(arg[2].split('/')[0]) / float(arg[2].split('/')[-1]) / 60)) / 60)


def find_GPS_image(pic_path):
    GPS = {}
    date = ''
    with open(pic_path, 'rb') as f:
        tags = exifread.process_file(f)
        for tag, value in tags.items():
            if re.match('GPS GPSLatitudeRef', tag):
                GPS['GPSLatitudeRef'] = str(value)
            elif re.match('GPS GPSLongitudeRef', tag):
                GPS['GPSLongitudeRef'] = str(value)
            elif re.match('GPS GPSAltitudeRef', tag):
                GPS['GPSAltitudeRef'] = str(value)
            elif re.match('GPS GPSLatitude', tag):
                try:
                    match_result = re.match('\[(\w*),(\w*),(\w.*)/(\w.*)\]', str(value)).groups()
                    GPS['GPSLatitude'] = int(match_result[0]), int(match_result[1]), int(match_result[2])
                except:
                    deg, min, sec = [x.replace(' ', '') for x in str(value)[1:-1].split(',')]
                    GPS['GPSLatitude'] = latitude_and_longitude_convert_to_decimal_system(deg, min, sec)
            elif re.match('GPS GPSLongitude', tag):
                try:
                    match_result = re.match('\[(\w*),(\w*),(\w.*)/(\w.*)\]', str(value)).groups()
                    GPS['GPSLongitude'] = int(match_result[0]), int(match_result[1]), int(match_result[2])
                except:
                    deg, min, sec = [x.replace(' ', '') for x in str(value)[1:-1].split(',')]
                    GPS['GPSLongitude'] = latitude_and_longitude_convert_to_decimal_system(deg, min, sec)
            elif re.match('GPS GPSAltitude', tag):
                GPS['GPSAltitude'] = str(value)
            elif re.match('.*Date.*', tag):
                date = str(value)
    return {'GPS_information': GPS, 'date_information': date}


def find_address_from_GPS(GPS):
    """
    使用Geocoding API把经纬度坐标转换为结构化地址。
    :param GPS:
    :return:
    """
    secret_key = 'zbLsuDDL4CS2U0M4KezOZZbGUY9iWtVf'
    if not GPS['GPS_information']:
        return '该照片无GPS信息'
    lat, lng = GPS['GPS_information']['GPSLatitude'], GPS['GPS_information']['GPSLongitude']
    baidu_map_api = "http://api.map.baidu.com/geocoder/v2/?ak={0}&callback=renderReverse&location={1}," \
                    "{2}s&output=json&pois=0".format(
        secret_key, lat, lng)
    response = requests.get(baidu_map_api)
    content = response.text.replace("renderReverse&&renderReverse(", "")[:-1]
    baidu_map_address = json.loads(content)
    formatted_address = baidu_map_address["result"]["formatted_address"]
    province = baidu_map_address["result"]["addressComponent"]["province"]
    city = baidu_map_address["result"]["addressComponent"]["city"]
    district = baidu_map_address["result"]["addressComponent"]["district"]
    return formatted_address, province, city, district


def file_name(file_dir):
    File_Name = []
    for files in os.listdir(file_dir):
        # print(files)
        if os.path.splitext(files)[1] == '.JPG':
            File_Name.append(file_dir + files)
    # print(len(File_Name))
    return File_Name


def get_img_file(file_name):
    """
    查找文件夹下所有图片
    """
    imagelist = []
    for parent, dirnames, filenames in os.walk(file_name):
        for filename in filenames:
            if filename.lower().endswith('.jpg'):
                imagelist.append(os.path.join(parent, filename))
    return imagelist


file_dir = get_img_file('/Volumes/存放照片区/无人机原照片/2020.11.27')
# txt_file_name = file_name('/Volumes/未命名/无人机照片/')
# print("txt_file_name", txt_file_name)
# for i in file_dir:
#     pic_path = i
#     GPS_info = find_GPS_image(pic_path)
#     # address = find_address_from_GPS(GPS=GPS_info)
#     # print(GPS_info)
#     # print(address)
#
#     # x = list(GPS_info.values())
#     # print(x)
#
#     daytime = GPS_info['date_information']
#     # print(i, daytime)

# def file_name_walk(file_dir):
#     for root, dirs, files in os.walk(file_dir):
#         print("root", root)  # 当前目录路径
#         print("dirs", dirs)  # 当前路径下所有子目录
#         print("files", files)  # 当前路径下所有非目录子文件
#
#
# file_dir = '/Volumes/未命名/无人机照片'
# file_name_walk("./")
wb = xlrd.open_workbook(r'/Users/liwenjie/Desktop/无人机飞行记录表(1).xlsx')
table = wb.sheets()[0]
rows = table.nrows
dirlists = []
dictlist = {}
for i in range(table.nrows):
    table.row_values(i)
    dirpath = '/Volumes/存放照片区/' + table.row_values(i)[3] + '/' + table.row_values(i)[4] + '/' + \
              table.row_values(i)[5]
    startime = table.row_values(i)[6]
    endtime = table.row_values(i)[7]
    # print(dirpath)
    # print(startime)
    # print(endtime)
    # dictjpg = dict(pathipg=dirpath, startime=startime, endtime=endtime)
    # dictlist[dirpath] = startime, endtime
    # print(dictlist)

    try:
        startime = datetime.datetime.strptime(startime, '%Y年%m月%d日%H时%M分')
        # print(startime, type(startime))
        endtime = datetime.datetime.strptime(endtime, '%Y年%m月%d日%H时%M分') + datetime.timedelta(0, 59)  # 增加59秒
        # print(endtime, type(endtime))
    except:
        print('无效日期')
    dirlist = [dirpath, startime, endtime]
    dirlists.append(dirlist)
    # for t in dictlist:

print(dirlists)
# print(type(dirlist[1]))
for i in dirlists:
    try:
        if i[1] != '拍照开始时间':
            os.makedirs(i[0])
    except:
        pass
n = 0
for i in file_dir:
    pic_path = i
    GPS_info = find_GPS_image(pic_path)
    daytime = GPS_info['date_information']
    # print(i, daytime)
    # print(type(daytime))
    daytime = datetime.datetime.strptime(daytime, '%Y:%m:%d %H:%M:%S')
    for path in dirlists:
        if path[1] != '拍照开始时间':
            if path[1] <= daytime <= path[2]:
                n += 1
                print("复制图片" + i + str(n) + path[0])


print(i)
2

