#coding:utf-8
#!/usr/bin/python
import requests,time
import re
import random
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
        def join(self,name,phone,qqnum,message):
            post_url="http://bbs.pcauto.com.cn/activity/join.ajax"
	    url_data={
		    "tid":12939683,
                    "name":name,
                    "phone":phone,
                    "persons":1,
                    "qqNum":qqnum,
                    "description":message
	    }
            page=self.s.post(post_url,url_data).text
            print page
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
                self.xing=[]
                self.zi=[]
                self.descib=[]
		for i in fp:
		    if isU:
			self.username.append(i.rstrip())
		    else :
			self.password.append(i.rstrip())
		    isU=not isU
                fp=open("xing.txt","r")
		for i in fp:
		    self.xing.append(i.rstrip())
                fp=open("zi.txt","r")
                for i in fp:
                    self.zi.append(i.rstrip())
                fp=open("join.txt","r")
                for i in fp:
                    self.descib.append(i.rstrip())
if __name__=='__main__':
        filename="account.txt"
	user=Readfile(filename)
        for i in range(len(user.username)):
                auto=Auto()
                auto.login(user.username[i],user.password[i])
                phone=(int)(random.random()*84564805)+15500000000
                qq=(int)(random.random()*19878797)+65749878
                name=user.xing[(int)(random.random()*len(user.xing))]+user.zi[(int)(random.random()*len(user.zi))]+user.zi[(int)(random.random()*len(user.zi))]
                if auto.join(name,phone,qq,user.descib[i]):
                    print "%s:[\033[1;32m+\033[0;0m]报名成功"%(user.username[i])
                else:
                    print "%s:[\033[1;31m-\033[0;0m]报名失败!"%(user.username[i])
