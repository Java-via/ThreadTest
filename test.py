# _*_ coding: utf-8 _*_

import urllib.request
import urllib.error
import threading
import logging
import queue
import time
import bs4
from db_config import *

ASO_HEADERS = {
    "Cookies": "PHPSESSID=btqkg9amjrtoeev8coq0m78396; "
               "USERINFO=n6nxTHTY%2BJA39z6CpNB4eKN8f0KsYLjAQTwPe%2BhLHLruEbjaeh4ulhWAS5RysUM%2B; "
               "Hm_lvt_0bcb16196dddadaf61c121323a9ec0b6=1472528976; "
               "Hm_lpvt_0bcb16196dddadaf61c121323a9ec0b6=1472534045; "
               "ASOD=xyCtGMkg%2BeAQu4jGhbEHbwEv",
    "User-Agent": "Chrome/52.0.2743.116"
}
logging.basicConfig(level=logging.DEBUG)
url_queue = queue.Queue()
save_queue = queue.Queue()


def get_url_queue():
    conn, cur = db_conn()
    sql = "SELECT bundleid, url FROM t_ios_classify"
    try:
        cur.execute(sql)
        for item in cur.fetchall():
            logging.debug("Url is %s", item)
            url_queue.put(item)
    except Exception as excep:
        logging.error("Get_Url_Queue Error: %s", excep)
    logging.debug("Get Url Queue done")


def get_bundleid_pkgname():
    time.sleep(5)
    while url_queue.qsize() > 0:
        url_item = url_queue.get()
        bundleid = url_item[0]
        ios_url = url_item[1]
        try:
            request = urllib.request.Request(url=ios_url, headers=ASO_HEADERS)
            response = urllib.request.urlopen(request)
            pkgname = ""
            andr_name = ""
            soup = bs4.BeautifulSoup(response, "html5lib")
            # ios_name = soup.find("h3", class_="appinfo-title").get_text()
            # detail_tr = soup.find_all("table", class_="base-info base-area")[0].find("tbody").find_all("tr")
            #
            # for item in detail_tr:
            #     for name in item.find("td", class_="name"):
            #         if name == "Bundle ID":
            #             bundleid = item.find_all("td")[1].get_text()
            # print(ios_name + "\t" + bundleid)
            li_soup = soup.find_all("li", role="presentation")
            if len(li_soup) == 2:
                url = li_soup[1].find("a")["href"]
                fetch_url = urllib.request.urljoin(base="http://aso100.com/rank", url=url)
                resp = urllib.request.urlopen(fetch_url)
                andr_soup = bs4.BeautifulSoup(resp, "html5lib")
                andr_name = andr_soup.find("h3", class_="appinfo-title").get_text()
                pkgname = andr_soup.find_all("div", class_="appinfo-auther")[1].find("p", class_="content text").get_text()
                logging.debug("Get pkgname done: %s, bundleid is %s", pkgname, bundleid)
                save_item = [bundleid, pkgname, andr_name]
                save_queue.put(save_item)
            else:
                logging.debug("Bundleid %s has no pkgname", bundleid)
        except urllib.error.HTTPError as excep:
            logging.error("When open %s Error %s", ios_url, excep)
            url_queue.put(bundleid, ios_url)


def update_item():
    conn, cur = db_conn()
    update_sql = "UPDATE t_ios_classify SET pkgname = %s, name_list = %s WHERE bundleid = %s;"
    update_count = 0
    while save_queue.qsize() > 0 or url_queue.qsize() > 0:
        print(save_queue.qsize())
        save_item = save_queue.get()
        print(save_item)
        bundleid = save_item[0]
        pkgname = save_item[1]
        andr_name = save_item[2]
        cur.execute(update_sql, (pkgname, andr_name, bundleid))
        logging.debug("Update_item success: %s", pkgname)
        update_count += 1
        if update_count % 50 == 0:
            logging.debug("Update item")
            conn.commit()
    conn.commit()
    logging.debug("Update done")


if __name__ == "__main__":
    get_url_queue()

    threads = [threading.Thread(target=get_bundleid_pkgname) for i in range(10)]
    threads.append(threading.Thread(target=update_item))

    for th in threads:
        th.setDaemon(1)
        th.start()

    for th in threads:
        if th.is_alive():
            print("is alive")
            th.join()

    exit()
