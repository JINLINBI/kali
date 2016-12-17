#coding:utf-8
#!/usr/bin/python
import requests,time
import re
import random
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
                return page
class Readfile(object):
	def __init__(self):
		fp=open("account.txt","r")
		isU=True
		self.username=[]
		self.password=[]
		self.xuetitle=[]
		self.xuemessage=[]
		self.biaotitle=[]
		self.biaomessage=[]
		for i in fp:
		    if isU:
			self.username.append(i.rstrip())
		    else :
			self.password.append(i.rstrip())
		    isU=not isU
		fp=open("wenan.txt","r")
		isU=True
		for i in fp:
			if isU:
				self.xuetitle.append(i.rstrip())
			else:
				self.xuemessage.append(i.rstrip())
			isU=not isU
		fp=open("wenanbiaozhi.txt","r")
		isU=True
		for i in fp:
			if isU:
				self.biaotitle.append(i.rstrip())
			else:
				self.biaomessage.append(i.rstrip())
			isU=not isU
if __name__=='__main__':
	fid=["18555","14626","17644"]
	albumid="2129127"
	user=Readfile()
	for i in range(len(user.username)):
	        auto=Auto()
		auto.login(user.username[i],user.password[i])
                for k in range(0,3):
                        if k==0:
                            num=(int)(random.random()*len(user.biaomessage))
                            auto.create(fid[k],user.biaotitle[num],user.biaomessage[num],albumid).rstrip()
                            print "[+]帐号:"+user.username[i]+"发帖["+user.biaotitle[num]+"]"+user.biaomessage[num]
                        else :
                            num=(int)(random.random()*len(user.xuemessage))
        		    auto.create(fid[k],user.xuetitle[num],user.xuemessage[num],albumid).rstrip()
                            print "[+]帐号:"+user.username[i]+"发帖["+user.xuetitle[num]+"]"+user.xuemessage[num]
