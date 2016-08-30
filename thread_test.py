# _*_ coding: utf-8 _*_

import threading
import queue
import bs4
import make_cookie


url_queue = queue.Queue()
save_queue = queue.Queue()
cookiejar, opener = make_cookie.make_cookiejar_opener()

out = open("G:/tmp/thread_test_bundle", "a", encoding="utf-8")


def make_url():

    cookie_string = "PHPSESSID=btqkg9amjrtoeev8coq0m78396; " \
                    "USERINFO=n6nxTHTY%2BJA39z6CpNB4eKN8f0KsYLjAQTwPe%2BhLHLruEbjaeh4ulhWAS5RysUM%2B; " \
                    "Hm_lvt_0bcb16196dddadaf61c121323a9ec0b6=1472528976; " \
                    "Hm_lpvt_0bcb16196dddadaf61c121323a9ec0b6=1472534045; " \
                    "ASOD=xyCtGMkg%2BeAQu4jGhbEHbwEv"
    cookiejar, opener = make_cookie.make_cookiejar_opener()
    cookies_list = make_cookie.make_cookies_string(cookie_string, domain="aso100.com")
    for cookie in cookies_list:
        cookiejar.set_cookie(cookie)

    for i in range(7001, 7020):
        title = ""
        if i == 7010:
            continue
        for page in range(1, 8):
            url = [1, 2]
            if page == 1:
                url[0] = "http://aso100.com/rank/index/device/iphone/country/cn/brand/free/genre/" + str(i)
                response = opener.open(url[0])
                soup = bs4.BeautifulSoup(response, "html5lib")
                title = soup.find("div", class_="title").get_text().split(" ")
                url[1] = title[2][2:-3]
            else:
                url[0] = "http://aso100.com/rank/more/device/iphone/country/cn/brand/free/genre/" + str(i) \
                         + "?page=" + str(page)
                url[1] = title[2][2:-3]
            print(str(url))
            url_queue.put(url)


def get_item():
    while url_queue.qsize() > 0:
        url = url_queue.get()
        response = opener.open(url[0])
        if response:
            soup = bs4.BeautifulSoup(response, "html5lib")
            a_soup = soup.find_all("a", target="_blank")
            for a in a_soup:
                arr = a["href"].split("/")
                detail_url = "http://aso100.com/app/baseinfo/appid/" + arr[4] + "/country/cn"
                print(detail_url)
                response = opener.open(detail_url)
                soup = bs4.BeautifulSoup(response, "html5lib")
                name = soup.find("h3", class_="appinfo-title").get_text()
                table = soup.find("table", class_="base-info base-area")
                tr = table.find("tbody").find_all("tr")
                # classify = tr[1].find_all("td")[1].get_text()
                bundleid = tr[4].find_all("td")[1].get_text()
                print(str(name) + "\t" + str(bundleid) + "\t" + str(url[1]) + "\n")
                item = str(name) + "\t" + str(bundleid) + "\t" + str(url[1]) + "\n"
                save_queue.put(item)
    else:
        print("Get item work done")


def save_item():
    while save_queue.qsize() > 0 or url_queue.qsize() > 0:
        out.write(save_queue.get())
        print("Save is running")
    print("Save work done")


if __name__ == '__main__':
    make_url()

    threads = [threading.Thread(target=get_item) for i in range(10)]
    threads.append(threading.Thread(target=save_item))

    for th in threads:
        th.setDaemon(1)
        th.start()

    for th in threads:
        if th.is_alive():
            th.join()

    exit()
