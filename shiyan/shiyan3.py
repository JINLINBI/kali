#!/usr/bin/env python3
import urllib.request
import argparse
parser=argparse.ArgumentParser()
parser.add_argument("-u",dest="url",type=str,default=None,)
parser.add_argument("-o",dest="outputfile",type=str,default=None,)

args=parser.parse_args()
user_agent="Mozilla/5.0(Windows NT 10.0;Win64;x64;rv:53.0)Gecko/20100101 Firefox/53.0"
if args.url.find("http://")==-1:
	args.url="http://"+args.url
headers={'User-Agent':user_agent}
req=urllib.request.Request(args.url,headers=headers)
with urllib.request.urlopen(req,timeout=30) as f:
	html=f.read().decode("utf-8")
	if args.outputfile:
		with open(args.outputfile,"w") as fp:
			fp.write(html)
	else:
		with open("spider.html","w") as fp:
			fp.write(html)
