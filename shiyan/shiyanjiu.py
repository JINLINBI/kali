#!coding:utf-8
import re
import os
import time
class CalFile:
	def __init__(self,filename):
		self.filename=filename
		self.text=""
		self.words=[]
		self.count={}
		self.readfile()
		self.getWords()
		self.countWords()
		self.writeFile()
	def readfile(self):
		with open(self.filename,"r") as fp:
			End=None
			while not End:
				buf=fp.readline()
				if buf:
					self.text+=buf
				else:
					End=True
	def getWords(self):
		self.words=re.findall(r"\w+",self.text)
		for i in self.words:
			if not self.count.get(i):
				self.count[i]=0
	def countWords(self):
		for i in self.words:
			self.count[i]+=1
		self.count=sorted(self.count.items(),key=lambda y:y[1],reverse=True)
	def writeFile(self):
		with open("words.txt","w") as fp:
			for i in self.count:
				fp.write("%s:%s "%(i[0],i[1]))
		os.system("cat words.txt")
if __name__=='__main__':
	starttime=time.time()
	calfile=CalFile('test.txt')
	endtime=time.time()
	print "\n所用时间：%s"%(endtime-starttime)
