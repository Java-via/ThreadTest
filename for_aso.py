# _*_ coding: utf-8 _*_

import bs4
import make_cookie

f = open("G:/tmp/detail_url", "a", encoding="utf-8")
out = open("G:/tmp/bundle", "a", encoding="utf-8")

COOKIE_STRING_ASO = "PHPSESSID=btqkg9amjrtoeev8coq0m78396; " \
                    "USERINFO=n6nxTHTY%2BJA39z6CpNB4eKN8f0KsYLjAQTwPe%2BhLHLruEbjaeh4ulhWAS5RysUM%2B; " \
                    "Hm_lvt_0bcb16196dddadaf61c121323a9ec0b6=1472528976; " \
                    "Hm_lpvt_0bcb16196dddadaf61c121323a9ec0b6=1472534045; " \
                    "ASOD=xyCtGMkg%2BeAQu4jGhbEHbwEv"
DOMAIN_ASO = "aso100.com"

cookiejar, opener = make_cookie.make_cookiejar_opener()
cookies_list = make_cookie.make_cookies_string(COOKIE_STRING_ASO, domain=DOMAIN_ASO)
for cookie in cookies_list:
    cookiejar.set_cookie(cookie)

opener.addheaders = make_cookie.make_headers(user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) "
                                                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                                                        "Chrome/52.0.2743.116 Safari/537.36").items()

url_list = []

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
        url_list.append(url)

for url in url_list:
    response = opener.open(url[0])
    if response:
        soup = bs4.BeautifulSoup(response, "html5lib")
        a_soup = soup.find_all("a", target="_blank")
        for a in a_soup:
            arr = a["href"].split("/")
            detail_url = "http://aso100.com/app/baseinfo/appid/" + arr[4] + "/country/cn"
            f.write(detail_url + "\n")
            print(detail_url)
            response = opener.open(detail_url)
            soup = bs4.BeautifulSoup(response, "html5lib")
            name = soup.find("h3", class_="appinfo-title").get_text()
            table = soup.find("table", class_="base-info base-area")
            tr = table.find("tbody").find_all("tr")
            # classify = tr[1].find_all("td")[1].get_text()
            bundleid = tr[4].find_all("td")[1].get_text()
            print(str(name) + "\t" + str(bundleid) + "\t" + str(url[1]) + "\n")
            out.write(str(name) + "\t" + str(bundleid) + "\t" + str(url[1]) + "\n")

print("save detail_url done")
