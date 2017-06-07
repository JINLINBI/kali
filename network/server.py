import socket, select
import time,hashlib,random,sys,struct
import redis,pymysql
import redis
class Table_ctrl():
    def __init__(self,tablename):
        self.tablename=tablename
        self.connect_db()
    def get_timeId(self):
        now=time.time()
        intnow=int(now)
        ms=int((now-intnow)*1000)
        timeId=time.strftime("%y%m%d%H%M%S",time.localtime(time.time()))+str(ms)
        return timeId
#    def get_randomId(self):
#        randomId=1000000000+math.floor(random.random()*999999999)
#        sql="select * from "+self.tablename+" where ID='"+str(randomId)+"'"
#        print(sql)
#        self.cur.execute(sql)
#        while self.cur.fetchone():
#                print("fetch again")
#                randomId=self.get_randomId()
#        return randomId
    def connect_db(self):
        self.conn=pymysql.connect(user="jin",password="123456",database="CHATROOM",charset="utf8")
        self.cur=self.conn.cursor()
    def write_db(self,*data):
        sql="INSERT INTO "+str(self.tablename)+" VALUES('"+self.get_timeId()+"'"
        for i in range(len(data)):
            if type(data[i])==type("string"):
                sql+=",'"+data[i]+"'"
            else:
                sql+=","+str(data[i])
        sql+=")"
        try:
            self.cur.execute(sql.encode('utf-8'))
            self.conn.commit()
        except Exception as e:
            print("writting  database error:%s"%e)
    def checkExist(self,column,value):
        Exist=False
        if type(value)==type("string"):
            sql="select * from "+str(self.tablename)+" where "+str(column)+"='"+str(value)+"'"
        else:
            sql="select * from "+str(self.tablename)+" where "+str(column)+"="+str(value)
        try:
            self.cur.execute(sql)
            if self.cur.fetchone():
                    Exist=True
        except:
            print("check value Error!")
        return Exist
    def __del__(self):
        self.conn.close()
class Login(Table_ctrl):
    def __init__(self,username,password):
        Table_ctrl.__init__(self,"USER")
        self.username=username
        self.password=password
    def login(self):
        sha1=hashlib.sha1()
        sha1.update(self.password.encode('utf-8'))
        self.password=sha1.hexdigest()
        return self.isLegal(self.username,self.password)
    def isLegal(self,username,password):
        sql="SELECT * FROM USER WHERE USERNAME='{0}' AND PASSWORD='{1}'".format(username,password)
        print(sql)
        self.cur.execute(sql)
        result=self.cur.fetchone()
        if result:
            self.niname=result[3]
            return True
        else:
            print("Login Error!")
class Register(Table_ctrl):
    def __init__(self,username,password,niname):
        Table_ctrl.__init__(self,"USER")
        self.username=username
        self.password=password
        self.niname=niname
        self.age=0
        self.sex='NUll'
        self.picId='NULL'
    def register(self):
        sha1=hashlib.sha1()
        sha1.update(self.password.encode('utf-8'))
        self.password=sha1.hexdigest()
        return self.isLegal()
    def isLegal(self):
        if self.checkExist("USERNAME",self.username) or  self.checkExist("NINAME",self.niname):
           return False
        self.write_db(self.username,self.password,self.niname,self.age,self.sex,self.picId)
        return True
def broadcast_data (sock, message):
    for socket in CONNECTION_LIST:
        if socket != server_socket and socket != sock and socket!=sys.stdin:
            try :
                socket.send(message.encode())
#send(socket,message.encode())
            except Exception as e:
                print("Error:%s"%e)
                socket.close()
                CONNECTION_LIST.remove(socket)
def send(channel,*args):
    buffers=pickle.dumps(args)
    value=socket.htonl(len(buffers))
    size=struct.pack("L",value)
    channel.send(size)
    channel.send(buffers)
def receive(channel):
    size=struct.calcsize("L")
    size=channel.recv(size)
    try:
        size=socket.ntohl(struct.unpack("L",size)[0])
    except struct.error as e:
        return ''
    buf=""
    while len(buf)<size:
        buf+=channel.recv(size-len(buf))
    return pickle.loads(buf)[0]
if __name__ == "__main__":
    CONNECTION_LIST = [sys.stdin]
    RECV_BUFFER = 4096 
    PORT = 5000
    r=redis.StrictRedis()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("0.0.0.0", PORT))
    server_socket.listen(10)
 
    CONNECTION_LIST.append(server_socket)
 
    print("Chat server started on port " + str(PORT) )
    running=True
    while running:
        read_sockets,write_sockets,error_sockets = select.select(CONNECTION_LIST,[],[])
 
        for sock in read_sockets:
            if sock == server_socket:
                sockfd, addr = server_socket.accept()
                CONNECTION_LIST.append(sockfd)
                message="Client (%s, %s) connected\t" % addr
                print(message)
                tc=Table_ctrl("RECORD")
                tc.write_db(message)
                broadcast_data(sockfd, "[%s:%s] entered room\n" % addr)
            elif sock==sys.stdin:
                junk=sys.stdin.readline()
                running=False
            else:
                try:
                    data = sock.recv(RECV_BUFFER)
#data=False#测试时用
#                   r=receive(sock).decode()
#                   print(type(r))
                    if data:
                        tc=Table_ctrl("RECORD")
                        tc.write_db(data.decode().rstrip())
                        del tc
                        broadcast_data(sock, "\r" + '<' + str(sock.getpeername()) + '> ' + data.decode())
                except Exception as e:
                    print("Error:%s"%e)
                    broadcast_data(sock, "Client (%s, %s) is offline" % addr)
                    print("Client (%s, %s) is offline" % addr)
                    sock.close()
                    CONNECTION_LIST.remove(sock)
                    continue
    server_socket.close()
