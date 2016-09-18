# _*_ coding: utf-8 _*_

import pymysql


def db_conn():
    db_host = "127.0.0.1"
    db_user = "root"
    db_passwd = "123"
    db_db = "app_db"
    db_charset = "utf8"
    conn = pymysql.connect(host=db_host, user=db_user, passwd=db_passwd, db=db_db, charset=db_charset)
    cur = conn.cursor()
    return conn, cur
