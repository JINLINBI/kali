#!/usr/bin/env python3
import urllib.request
import sys
user_agent="Mozilla/5.0(Windows NT 10.0;Win64;x64;rv:53.0)Gecko/20100101 Firefox/49.0"
if sys.argv[1]:
	url=sys.argv[1]
	if sys.argv[2]:
		savefile=sys.argv[2]
	else:
		savefile="helloworld.html"
else:
	print("help:\n example:python shiyan3jiu.py http://www.baidu.com helloworld.html")
	sys.exit(0)
headers={"user_agent":user_agent}
req=urllib.request.Request(url,headers=headers)
try:
	with urllib.request.urlopen(req,timeout=60) as fp:
		result=fp.read().decode("utf-8")
		with open(savefile,"w") as f:
			f.write(result)
except urllib.error.URLError as e:
	print("Error：{0}".format(e))
