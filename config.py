# _*_ coding: utf-8 _*_
import os

basedir = os.path.abspath(os.path.dirname(__file__))
DEBUG = True
SECRET_KEY = 'arrange_for_room'
# os.urandom(24)
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@localhost:3306/arg4rm?charset=utf8'
# 主意这里的charset为utf8，而不是utf-8
