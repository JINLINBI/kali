#coding:utf8
#!/usr/bin/python3
import urllib
import urllib2
import requests,time
import cookielib
import hashlib
import re
import os
class Web_pro(object):
    def __init__(self):
        self.cookie=cookielib.CookieJar()
        self.opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie))
    def index(self,index):
        socket=self.opener.open(index)
        print socket.getcode()
        page=unicode(socket.read(),"gbk").encode("utf-8")
        return page
    def login(self,username,password):
        url=""
        for i in self.cookie:
            Cookie=i.name+":"+i.value
	try:
            request=urllib2.Request("https://passport3.pcauto.com.cn/passport3/passport/login.jsp")
            request.add_header('Host','passport3.pcauto.com.cn')
            request.add_header('User-Agent','Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0Host')
            request.add_header('Accpt','text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
            request.add_header('Accept-Language','zh,en-US;q=0.7,en;q=0.3')
            request.add_header('Accept-Encoding','gzip.deflate')
            request.add_header('DNT','1')
            request.add_header('Referer','http://my.pcauto.com.cn/passport/login.jsp?return=http%3A%2F%2Fmy.pcauto.com.cn%2Findex.jsp')
            request.add_header('Cookie',Cookie)
            postdata=urllib.urlencode({
                'return':'http://my.pcauto.com.cn/index.jsp',
                'login_url':'http://my.pcauto.com.cn/login.jsp',
                'username':username,
                'password':password,
                'auto_login':'3000'
            })
            request.add_data(postdata)
            socket=urllib2.urlopen(request)
            page=socket.read()
        except urllib2.URLError as e:
            print e
if __name__=='__main__':
    index="http://bbs.pcauto.com.cn"
    web_pro=Web_pro()
    print  web_pro.index(index)
    for i in web_pro.cookie:
        print i.name+"="+i.value


