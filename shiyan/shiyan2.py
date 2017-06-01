#!/usr/bin/env python3
import socket
s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.bind(('',5000))
while True:
	data,addr=s.recvfrom(1024)
	data=data.decode()
	print('received message:{0} from PORT {1[1]} on {1[0]}'.format(data,addr))
	if data=="123456":
		message="correct"
	else:
		message="false"
	s.sendto(message.encode(),addr)

