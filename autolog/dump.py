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
        def getuserid(self):
            topic_url="http://my.pcauto.com.cn/forum/index.jsp"
            page=self.s.get(topic_url).text
            pattern=re.compile(r'userId=(.+)&')
            match=pattern.findall(page)[0]
            if match:
                return match
            else:
                return "not found"
        def gettid(self,userid):
            topic_url="http://bbs.pcauto.com.cn/intf/user/_topics.jsp?unreviewActivity=1&userId=%s&callback=show&pageSize=1500&pageNo=1"%userid
            page=self.s.get(topic_url).text
            pattern=re.compile(r'"topicId":(\d+),')
            fidpattern=re.compile(r'"fid":(\d+),')
            #pattern=re.compile(r'userId=(d+)')
            self.tid=pattern.findall(page)
            self.fid=fidpattern.findall(page)
class Readfile(object):
	def __init__(self,filename):
		fp=open(filename,"r")
		isU=True
		self.username=[]
		self.password=[]
		self.xuetitle=[]
		self.xuemessage=[]
		self.biaotitle=[]
		self.biaomessage=[]
                self.matitle=[]
                self.mamessage=[]
                self.fid=[]
                self.tid=[]
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
		fp=open("wenanmazida.txt","r")
		isU=True
		for i in fp:
			if isU:
				self.matitle.append(i.rstrip())
			else:
				self.mamessage.append(i.rstrip())
			isU=not isU
                fp=open("write.txt","r")
                isU=True
                for i in fp:
                    if isU:
                        self.tid.append(i.rstrip)
                    else :
                        self.fid.append(i.rstrip)
if __name__=='__main__':
        #filename=raw_input("Account filename:")
        filename="account.txt"
        #fid={'mazida':'19536','biaozhi':'16725','xuefolan':"14626",'xuefolan':"17644",'xuefolan':'20338',"xuefolan":"16300"}
        fid=['19536','14626','16725','17644','24056','17670','19865','20360','15151','17686','17128','17085','17287','17654','19565','20095','14360','14793','21685','17695','17281','16300','17278','17643','18555','16885','17282','23956','17297','17160','17271','14678','17285','00000','23106','15221','23565','17005','24715','20330','20338']
	user=Readfile(filename)
        #test=True
        test=False
        fp=open("write.txt","w")
	for i in range(len(user.username)):
	        auto=Auto()
		auto.login(user.username[i],user.password[i])
                end=False
                if not  test:
                    #tid=auto.forum(fid[k])
                    userid=auto.getuserid()
                    print "userid:"+userid
                    if userid:
                        tid=auto.gettid(userid)
                        for i,j in zip(auto.tid,auto.fid):
                            fp.write("%s\n%s\n"%(i,j))
        fp.close()
