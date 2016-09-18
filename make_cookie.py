# _*_ coding: utf-8 _*_

import http.cookiejar
import urllib.request
import time
import random
import config


def make_cookie(name, value, domain, port=None, path=None, expires=None):
    path = "/" if not path else path
    expires = (time.time() + 3600 * 24 * 30) if not expires else expires
    cookie = http.cookiejar.Cookie(
        version=0,
        name=name,
        value=value,
        port=port,
        port_specified=False,
        domain=domain,
        domain_specified=False,
        domain_initial_dot=False,
        path=path,
        path_specified=True,
        secure=False,
        expires=expires,
        discard=True,
        comment=None,
        comment_url=None,
        rest=None
    )
    return cookie


def make_cookies_string(cookie_string, domain):
    frags = [item.strip() for item in cookie_string.strip("; ").split(";") if item.strip()]
    return [make_cookie(k.strip(), v.strip(), domain) for k, v in [item.split("=") for item in frags] if k and v]


def make_cookiejar_opener(is_cookie=True, proxies=None):
    assert is_cookie or proxies, "make_cookiejar_opener: one of parameters(is_cookie, proxies) must be True"
    cookie_jar, opener = None, None
    if is_cookie:
        cookie_jar = http.cookiejar.CookieJar()
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))
    if proxies:
        if opener:
            opener.add_handler(urllib.request.ProxyHandler(proxies=proxies))
        else:
            opener = urllib.request.build_opener(urllib.request.ProxyHandler(proxies=proxies))

    return cookie_jar, opener


def make_headers(user_agent, **kwargs):
    """
    make a dictionary headers for requesting, user_agent: "pc", "phone", "all" or a ua_string
    """
    kwargs["user_agent"] = random.choice(config.CONFIG_USERAGENT_ALL) if user_agent == "all" else (
        random.choice(config.CONFIG_USERAGENT_PC) if user_agent == "pc" else (
            random.choice(config.CONFIG_USERAGENT_PHONE) if user_agent == "phone" else user_agent
        )
    )
    return {config.CONFIG_HEADERS_MAP[key]: kwargs[key] for key in kwargs if key in config.CONFIG_HEADERS_MAP}

