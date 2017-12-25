# -*- coding: utf-8 -*-
from nimin import app
from flask import Flask, g
import MySQLdb
import os

#链接和关闭数据库的两个函数
def get_db():
    if not hasattr(g, 'db'):
        g.db = connect_db()
    return g.db

def connect_db():
    rv = MySQLdb.connect(db='nimin',user='root',passwd=os.environ["DB_ENV_MYSQL_ROOT_PASSWORD"],host=os.environ["DB_PORT_3306_TCP_ADDR"],charset='utf8')
    return rv