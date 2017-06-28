#!/usr/bin/env python3
import socket
import sys
s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
with open("pswd.txt","r") as f:
	lines=f.readlines()
for line in lines:
	s.sendto(line.rstrip().encode(),('127.0.0.1',5000))
	data,addr=s.recvfrom(1024)
	data=data.decode()
	if data=="correct":
		print("{1}: {0}".format(line.rstrip(),data))
		break
	else:
		print("{1}: {0}".format(line.rstrip(),data))
