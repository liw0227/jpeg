# coding=utf-8
import xlrd
import os
import sys
import datetime

wb = xlrd.open_workbook(r'/Users/liwenjie/Desktop/无人机飞行记录表(1).xlsx')
table = wb.sheets()[0]
rows = table.nrows
dirlists = []
dictlist = {}
for i in range(table.nrows):
    table.row_values(i)
    dirpath = '/Users/liwenjie/Documents/' + table.row_values(i)[3] + '/' + table.row_values(i)[4] + '/' + \
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
        print(startime, type(startime))
        endtime = datetime.datetime.strptime(endtime, '%Y年%m月%d日%H时%M分') + datetime.timedelta(0, 59)  # 增加59秒
        print(endtime, type(endtime))
    except:
        print('无效日期')
    dirlist = [dirpath, startime, endtime]
    dirlists.append(dirlist)
    # for t in dictlist:

print(dirlists)
print(type(dirlist[1]))
for i in dirlists:
    try:
        if i[1] != '拍照开始时间':
            os.makedirs(i[0])
    except:
        pass
