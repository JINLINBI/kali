#coding:utf-8
#!/usr/bin/python
import requests,time
import re
import random
import threading
import time
class Auto(object):
	def __init__(self):
		self.s=requests.session()	
	def login(self,username,password):
		headers={
		    "Host":"passport3.pcauto.com.cn",
		    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36",
		    "Accept":"*/*",
		    "Accept-Language":"zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
		    "Accept-Encoding":"gzip, deflate",
		    "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
		    "X-Requested-With":"XMLHttpRequest",
		    "Connection":"keep-alive"
		}


		login_url=r'https://passport3.pcauto.com.cn/passport3/passport/login.jsp'

		html_txt = requests.get(login_url,verify=False).text

		#print xsrf
		#print html_txt


		url_data={
		    "return":"http://my.pcauto.com.cn/index.jsp",
		    "login_url":"http://my.pcauto.com.cn/login.jsp",
		    "username":username,
		    "password":password,
		    'auto_login':'3000'
		}

		s_login=self.s.post(login_url,data=url_data,headers=headers,verify=False)
		#html_soup = BeautifulSoup(s_login_text,'lxml')
		#xsrf = html_soup.find("script",{"":"href"})['value']
	def create(self,fid,title,message,albumid):
                create_url="http://bbs.pcauto.com.cn/action/topic/create.ajax"
		self.s.get("http://bbs.pcauto.com.cn/new/post.do?fid=%s"%fid)
		url_data={
			"sengmsg":'true',
			"fid":fid,
			"type":'',
			"topictitleMaxLength":"35",
			"category":'综合',
			"uploadKeepSource":"false",
			"topiccontentMinLength":"1",
			"topiccontentMaxLength":"500000",
			"title":title,
			"message":message,
			"upload2Album":albumid
		}
                page=self.s.post(create_url,data=url_data).text
                pattern=re.compile(r'</p>')
                match=pattern.findall(page)
                if match:
                    return False
                else :
                    return True
        def forum(self,fid):
            f_url="http://bbs.pcauto.com.cn/forum-%s.html"%fid
            page=self.s.get(f_url).text

            #pattern=re.compile(r'tid="(.+)" ')
            #pattern=re.compile(r'userID=(d+)')
            #pattern=re.compile(r'<tbody>(.+)</tbody>')
            match=pattern.findall(page)
            if match:
                return match
            else :
                return "not found"
        def comment(self,tid,fid,message):
            post_url="http://bbs.pcauto.com.cn/action/post/create.ajax"
	    url_data={
		    "tid":tid,
		    "fid":fid,
		    "message":message,
                    "needCaptcha":'false',
                    "captcha":'',
		    "sengMsg":'true',
                    "minContentLength":1,
                    "maxContentLength":500000
	    }
            page=self.s.post(post_url,url_data).text
            pattern=re.compile(r'</p>')
            match=pattern.findall(page)
            if match:
                return False
            else :
                return True
class Readfile(object):
	def __init__(self,filename):
		fp=open(filename,"r")
		isU=True
		self.username=[]
		self.password=[]
                self.comment=[]
                self.fid=[]
                self.tid=[]
		for i in fp:
		    if isU:
			self.username.append(i.rstrip())
		    else :
			self.password.append(i.rstrip())
		    isU=not isU
                fp=open("write.txt","r")
                isU=True
                for i in fp:
                    if isU:
                        self.tid.append(i.rstrip())
                    else:
                        self.fid.append(i.rstrip())
                    isU=not isU
                fp=open("comment.txt","r")
                for i in fp:
                    self.comment.append(i.rstrip())
def thr3ad(start):
        filename="account.txt"
	user=Readfile(filename)
        global count
        v=0
        for i in range(start,len(user.username)):
            if len(user.comment)>0 and len(user.tid)>0:
                auto=Auto()
                auto.login(user.username[i],user.password[i])
                for k in range(v,len(user.tid)) :
                    com=(int)(random.random()*len(user.comment))
                    if auto.comment(user.tid[k],user.fid[k],user.comment[com]):
                        print "%s:[\033[1;32m+\033[0;0m]%s一个回复帖子(%s):%s"%(count,user.username[i],user.tid[k],user.comment[com])
                        count+=1
                    else:
                        print "%s:[\033[1;31m-\033[0;0m]%s回复帖子(%s)失败!:"%(count,user.username[i],user.tid[k])
                        break
                    time.sleep(5)
                print "切换用户回复"
if __name__=='__main__':
    count=0
    t1=threading.Thread(target=thr3ad,args=(0,))
    t2=threading.Thread(target=thr3ad,args=(20,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
