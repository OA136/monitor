# coding: utf-8
# configuration for cloud_monitor and etc...

# 数据库配置
db_engine = 'mysql'
db_server = '10.10.17.9'
db_username = 'root'
db_password ='123456'
db_database = 'test'

#需要采集虚拟机信息所在的宿主机列表
hosts_list = ["192.168.75.136"]
# API端口配置
api_server_port = 9898

# nova配置
VERSION = '2'
USERNAME = 'admin'
PASSWORD = '123456'
PROJECT_ID = 'admin'
ADMIN_TOKEN = '47bc5eb069f8cbeb1ed9'
AUTH_URL = 'http://controller:35357/v2.0'
