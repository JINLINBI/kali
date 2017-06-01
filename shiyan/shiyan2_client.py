#!/usr/bin/env python3
import socket
import sys
s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
with open("pswd.txt","r") as fp:
	passwords=fp.readlines()
for password in passwords:
	s.sendto(password.rstrip().encode(),('127.0.0.1',5000))
	data,addr=s.recvfrom(1024)
	data=data.decode()
	if data=="correct":
		print("{1}:Password is {0}".format(password.rstrip(),data))
		break
	else:
		print("{1}:Password is not {0}".format(password.rstrip(),data))
