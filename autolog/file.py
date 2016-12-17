#coding:utf-8
#!/usr/bin/python 
fp=open("account.txt","r")
isU=True
username=[]
password=[]
xuetitle=[]
xuemessage=[]
biaotitle=[]
biaomessage=[]
for i in fp:
    if isU:
        username.append(i.rstrip())
    else :
        password.append(i.rstrip())
    isU=not isU
fp=open("wenan.txt","r")
isU=True
for i in fp:
	if isU:
		xuetitle.append(i.rstrip())
	else:
		xuemessage.append(i.rstrip())
	isU=not isU
fp=open("wenanbiaozhi.txt","r")
isU=True
for i in fp:
	if isU:
		biaotitle.append(i.rstrip())
	else:
		biaomessage.append(i.rstrip())
	isU=not isU
