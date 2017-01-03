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
	def create(self,fid,title,message,albumid,fp):
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
                tidpattern=re.compile(r'"tid":(\d+)')
                match=pattern.findall(page)
                tidmatch=tidpattern.findall(page)
               # if tidmatch:
                #    for i in tidmatch:
                 #       fp.write("%s\n%s\n")%(i,fid)
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
		self.xuetitle=[]
		self.xuemessage=[]
		self.biaotitle=[]
		self.biaomessage=[]
                self.matitle=[]
                self.mamessage=[]
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

if __name__=='__main__':
        #filename=raw_input("Account filename:")
        filename="account.txt"
        #fp=open(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())+".log","w+")
        #fid={'mazida':'19536','biaozhi':'16725','xuefolan':"14626",'xuefolan':"17644",'xuefolan':'20338',"xuefolan":"16300"}
        fid=['19536','14626','16725','17644','24056','17670','19865','20360','15151','17686','17128','17085','17287','17654','19565','20095','14360','14793','21685','17695','17281','16300','17278','17643','18555','16885','17282','23956','17297','17160','17271','14678','17285','00000','23106','15221','23565','17005','24715','20330','20338']
	albumid="2129127"
	user=Readfile(filename)
        #test=True
        test=False
        fp=''
	for i in range(len(user.username)):
	        auto=Auto()
		auto.login(user.username[i],user.password[i])
                end=False
                for k in range(0,len(fid)):
                    if not end and not test:
                        if fid[k]=='00000':
                            end=True
                        elif k==0:
                            num=i#(int)(random.random()*2)+i
                            if auto.create(fid[k],user.matitle[num],user.mamessage[num],albumid,fp):
                                print "[\033[1;32m+\033[0;0m]帐号:"+user.username[i]+"发帖["+user.matitle[num]+"]"+user.mamessage[num]
                            else:
                                print "[\033[1;31m-\033[0;0m]帐号:"+user.username[i]+"发帖失败!"
                                break
                        elif k%2==0:
                            num=i#(int)(random.random()*2)+i
                            if auto.create(fid[k],user.biaotitle[num],user.biaomessage[num],albumid,fp):
                                print "[\033[1;32m+\033[0;0m]帐号:"+user.username[i]+"发帖["+user.biaotitle[num]+"]"+user.biaomessage[num]
                            else:
                                print "[\033[1;31m-\033[0;0m]帐号:"+user.username[i]+"发帖失败!"
                                break
                        elif k%2==1:
                            num=i#(int)(random.random()*2)+i
                            if auto.create(fid[k],user.xuetitle[num],user.xuemessage[num],albumid,fp):
                                print "[\033[1;32m+\033[0;0m]帐号:"+user.username[i]+"发帖["+user.xuetitle[num]+"]"+user.xuemessage[num]
                            else :
                                print "[\033[1;31m-\033[0;0m]帐号:"+user.username[i]+"发帖失败!"
                                break
                    elif not test:
                            num=i#(int)(random.random()*2)+i
                            if auto.create(fid[k],user.xuetitle[num],user.xuemessage[num],albumid,fp):
                                print "[\033[1;32m+\033[0;0m]帐号:"+user.username[i]+"发帖["+user.xuetitle[num]+"]"+user.xuemessage[num]
                            else :
                                print "[\033[1;31m-\033[0;0m]帐号:"+user.username[i]+"发帖失败!"
                                break
                    ran=random.random()*5
                    time.sleep(2+ran)
        #fp.close()
