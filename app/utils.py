# _*_ coding: utf-8 _*_
from datetime  import datetime

# 处理datetime格式
def formatTime(strline):
    return datetime.strftime(strline, '%Y-%m-%d %H:%M:%S')
