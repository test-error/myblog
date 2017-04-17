# -*- coding: utf-8 -*-

import os

DB_USERNAME = 'root'
DB_PASSWORD = '0100'
DB_HOST = '127.0.0.1'
DB_PORT = '3306'
DB_NAME = 'sbbs'

DB_URI = 'mysql+mysqldb://%s:%s@%s:%s/%s' %(DB_USERNAME,DB_PASSWORD,DB_HOST,DB_PORT,DB_NAME)

SECRET_KEY = os.urandom(24)

SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False

SERVER_NAME = 'aska.com:5000'

#邮箱配置
MAIL_SERVER = 'smtp.qq.com'
MAIL_PORT = '465'
MAIL_USERNAME = '10512289@qq.com'
MAIL_PASSWORD = 'ypckphkgeodmbgea'
MAIL_DEFAULT_SENDER = '10512289@qq.com'
MAIL_USE_SSL = True

# MAIL_USE_TLS：端口号587
# MAIL_USE_SSL：端口号465
# QQ邮箱不支持非加密方式发送邮件

#celery
CELERY_BROKER_URL = 'redis://192.168.56.1:6379/0'
CELERY_RESULT_BACKEND = 'redis://192.168.56.1:6379/0'
