# -*- coding: utf-8 -*-

"""
    @author akira <i@zqhong.com>
    @date   2016-01-05
"""

try:
    import requests
    import Cookie
    import cookielib
    import time
    import json
    import sys
    import re
    import dill
except Exception, e:
    print >> sys.stderr, sys.exc_info()
    sys.exit(1)




class Weibo(object):
    def __init__(self):
        # 登陆新浪微博后得到的 cookies
        self.cookie_file = "weibo.dat"
        try:
            with open(self.cookie_file, "r") as r:
                cookies = r.read()
        except Exception, e:
            print >> sys.stderr, """\
Please create a file named 'weibo.dat', and then write your weibo cookies to it."""
            sys.exit(1)

        domain  = "www.weibo.com"
        # 解析原始的cookies字符串，设置只允许在 weibo.com 这个域名下面使用该 cookies
        cookie_jar = self.parse(cookies,domain)

        headers = {
            'User-Agent':'Mozilla/5.0 (X11; Linux i686; rv:8.0) Gecko/20100101 Firefox/8.0',
            'X-Requested-With': 'XMLHttpRequest',
            # 需要带上 Referer，不能回出现 系统繁忙 的错误
            'Referer': 'http://weibo.com',
        }

        self.s = requests.session()
        self.s.cookies = cookie_jar
        self.s.headers.update(headers)

        self.home_page = self.get_home()

    def post(self, message):
        """
        发送微博
        """
        # location=v6_content_home&appkey=&style_type=1&pic_id=&text=%E4%B8%AD%E6%96%87%E6%B5%8B%E8%AF%952&pdetail=&rank=0&rankid=&module=stissue&pub_source=main_&pub_type=dialog&_t=0
        data = {
            "location"   : "v6_content_home",
            "appkey"     : "",
            "style_type" : 1,
            "pic_id"     : "",
            "text"       : message,
            "rank"       : 0,
            "module"     : "stissue",
            "pub_source" : "main_",
            "pub_type"   : "dialog",
            "_t"         : 0,
            "pdetail"    : "",
            "rankid"     : "",
        }

        url = "http://weibo.com/aj/mblog/add?ajwvr=6&__rnd=%d" % (int(time.time()*1000))
        r = self.s.post(url, data=data)
        self.print_error("post method", r.text)

    def del_post(self, mid):
        """
        删除微博
        @params mid      微博id
        @return boolean  删除成功与否
        """
        data = {
            "mid" : int(mid),
        }

        url = "http://weibo.com/aj/mblog/del?ajwvr=6"
        r = self.s.post(url, data=data)

        self.print_error("del_post method", r.text)

    def del_all_post(self):
        """
        删除该用户发过的所有微博，慎用！
        """
        mids = self.list()
        while len(mids) != 0:
            print mids
            for mid in mids:
                print "删除 mid 为：%d 的微博中..." % (int(mid))
                self.del_post(mid)
            mids = self.list()
        print "成功删除所有微博"

    def list(self, url=""):
        """
        遍历单页微博
        @return list 返回微博的mid列表
        """
        if url == "":
            url = self.home_page
        r = self.s.get(url)
        html = r.text

        pattern = r"mid=(\d+)"
        mids = re.findall(pattern, html)
        mids = list(set(mids))
        return mids


    def get_home(self):
        """
        获取当前用户的首页URL
        首页 URL 类似：http://weibo.com/username/profile?is_all=1
        @return string 用户首页的URL
        """
        r = self.s.get("http://www.weibo.com")

        # 在微博首页中，在 JavaScript 中存有用户名，直接在里面提取用户名即可
        # $CONFIG['domain']='usename';

        pattern = r"CONFIG\['domain'\]='(.*)';"
        r = re.search(pattern, r.text)

        if not r:
            print "Can't get the username from the html page. It is probable you offer a invalid cookies. Please check the file named 'weibo.dat'"
            exit()
        username = r.group(1)

        url = "http://weibo.com/%s/profile?is_all=1" % (username)
        return url

    def print_error(self, method, r):
        """
        打印错误
        备注：code 等于 100000 表示成功
        @params method  哪个方法发生错误
        @params r       请求微博api返回的json数据
        """
        try:
            d = json.loads(r)
        except ValueError, e:
            print >> sys.stderr, "can't decode the json data"
            raise e


        if int(d["code"]) != 100000:
            print >> sys.stderr, "Method name: %s\nError code: %d\n Msg: %s\n" % (method, int(d["code"]), d["msg"])

    def parse(self, rawstr,url):
        """
        @params rawstr    原始的cookie字符串
        @params url       该cookie允许哪个站点使用
        @return CookieJar
        """
        url = '.'+'.'.join(url.split('.')[1:])
        c = Cookie.SimpleCookie()
        c.load(rawstr)
        ret = []
        for k in c:
            v = c[k]
            ret.append(cookielib.Cookie(
                        name=v.key,
                        value = v.value,
                        version=0,
                        port=None,
                        port_specified = False,
                        domain=url,
                        domain_specified=True,
                        domain_initial_dot=True,
                        path='/',
                        path_specified=True,
                        secure=False,
                        expires=None,
                        discard=False,
                        comment=None,
                        comment_url=None,
                        rest={'HttpOnly': None},
                        rfc2109=False,
            ))
        cookie = cookielib.CookieJar()
        for c in ret:
            cookie.set_cookie(c)
        return cookie
