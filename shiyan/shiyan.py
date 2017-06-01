#!coding:utf-8
import re
import os
import time
starttime=time.time()
text=""
words=[]
wordsCount={}
def writeFile():
	with open("words.txt","w") as fp:
		for i in wordsCount:
			fp.write("%s:%s "%(i[0],i[1]))
#	os.system("cat words.txt")
	return 
def readfile(filename):
	global text
	with open(filename,"r") as fp:
		End=None
		while not End:
			buf=fp.readline()
			if buf:
				text+=buf
			else:
				End=True
def getWords():
	global text
	global words
	global wordsCount
	words=re.findall(r"\w+",text)
	for i in words:
		if not wordsCount.get(i):
			wordsCount[i]=0
def countWords():
	global wordsCount
	global words
	for i in words:
		wordsCount[i]+=1
if __name__=='__main__':
	readfile('test2.txt')
	getWords()
	countWords()
	wordsCount=sorted(wordsCount.items(),key=lambda y:y[1],reverse=True)
	writeFile()
	endtime=time.time()
	os.system("cat words.txt")
	print "所用时间：%s"%(endtime-starttime)
