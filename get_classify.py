# _*_ coding: utf-8 _*_

import logging
from db_config import *

logging.basicConfig(level=logging.DEBUG)

conn, cur = db_conn()
ios_pkg_sql = "SELECT bundleid, pkgname FROM t_ios_classify WHERE pkgname IS NOT NULL;"
andr_sql = "SELECT pkgname, classify FROM t_pkg_classify_old;"
update_sql = "UPDATE t_ios_classify SET classify = %s WHERE bundleid = %s;"
count = 0

cur.execute(ios_pkg_sql)
bundle_pkg_dic = {}
for item in cur.fetchall():
    bundle_pkg_dic[item[0]] = item[1]

cur.execute(andr_sql)
pkg_cls_dic = {}
for item in cur.fetchall():
    pkg_cls_dic[item[0]] = item[1]

for key in bundle_pkg_dic:
    pkgname = bundle_pkg_dic[key]
    if pkgname in pkg_cls_dic:
        logging.debug("pkgname in android: %s", pkgname)
        classify = pkg_cls_dic[pkgname]
        cur.execute(update_sql, (classify, key))
    else:
        logging.debug("pkgname not in android: %s", pkgname)
    if count % 50 == 0:
        print("update")
        conn.commit()
    count += 1
conn.commit()
