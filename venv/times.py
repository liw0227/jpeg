import datetime

# str_p = '2019:10:31'
str_p = '2019:10:31 17:01:07'
date_p = datetime.datetime.strptime(str_p, '%Y:%m:%d %H:%M:%S')
print(date_p, type(date_p))  # 2019-01-30 <class 'datetime.date'>

str_p1 = '2019:10:31 17:09:43'
date_p1 = datetime.datetime.strptime(str_p1, '%Y:%m:%d %H:%M:%S')
print(date_p1, type(date_p1))  # 2019-01-30 <class 'datetime.date'>

str_p2 = '2019:10:31 17:05:43'
date_p2 = datetime.datetime.strptime(str_p2, '%Y:%m:%d %H:%M:%S')
print(date_p2, type(date_p2))

if date_p1 >= date_p2 >= date_p:
    print('在中间')
else:
    print('不在中间')
