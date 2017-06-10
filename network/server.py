import socket,select
import time,hashlib,random,sys,struct
import redis,pymysql
import redis
class Table_ctrl():
    def __init__(self,tablename):
        self.tablename=tablename
        self.connect_db()
    def connect_db(self):
        self.conn=pymysql.connect(user="jin",password="123456",database="CHATROOM",charset="utf8")
        self.cur=self.conn.cursor()
    def get_timeId(self):
        now=time.time()
        intnow=int(now)
        ms=int((now-intnow)*1000)
        timeId=time.strftime("%y%m%d%H%M%S",time.localtime(time.time()))+str(ms)
        return timeId
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
    def query_db(self,kColumn,kValue,queryField):
        if type(kValue)==type("string"):
            sql="select %s from %s where %s='%s'"%(queryField,self.tablename,kColumn,kValue)
        else:
            sql="select %s from %s where %s=%s"%(queryField,self.tablename,kColumn,kValue)
        print(sql)
        try:
            self.cur.execute(sql)
            return self.cur.fetchone()[0]
        except:
            print("query Error!")
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
            return False
class Register(Table_ctrl):
    def __init__(self,username,password,niname):
        Table_ctrl.__init__(self,"USER")
        self.username=username
        self.password=password
        self.niname=niname
        self.age=0
        self.sex='N'
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
    global online
    for socket in CONNECTION_LIST:
        if socket != server_socket and socket != sock and socket!=sys.stdin and online.get(socket):
            try :
                if message:
                    message+="\n"
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
def parse_data(socket,data):
    global online
    global online_niname
    global CONNECTION_LIST
    datalist=data.split(",")
    print(datalist)
    try:
        mes=datalist[0].split(":")[0]
        if mes=="data":
            if not  online.get(socket):
                return "Error:loginFirst"
            print("get DATA!!!!")
        elif mes=="register":
            username=datalist[1].split(":")[1]
            password=datalist[2].split(":")[1]
            niname=datalist[3].split(":")[1]
            register_user=Register(username,password,niname)
            if register_user.register():
                return "register:successfully"
            else:
                return "register:failed"
        elif mes=="login":
            if online.get(socket):
                return "login:repeat"
            username=datalist[1].split(":")[1]
            password=datalist[2].split(":")[1]
            login_user=Login(username,password)
            if login_user.login():
                print("login successfully!")
                tc=Table_ctrl("USER")
                niname=tc.query_db("USERNAME",username,"NINAME")
                online[sock]=True
                if not  niname:
                    niname="NULL"
                online_niname[sock]=niname
                broadcast_data(sock,"[%s]entered room" %online_niname[sock])
                return "login:successfully,niname:%s"%niname
            else:
                del login_user
                return "login:Failed"
        elif mes=="update":
            if not  online.get(socket):
                return "Error:loginFirst"
            print("update!")
        elif mes=="query":
            if not  online.get(socket):
                return "Error:loginFirst"
            sentence=""
            for i in CONNECTION_LIST:
                if online_niname.get(i):
                    sentence+=","+online_niname.get(i)
            return "query:successfully"+sentence
        elif mes=="message":
            if not  online.get(socket):
                return "Error:loginFirst"
            broadcast_data(sock,"{0}:{1}".format(online_niname[sock],datalist[0].split(":")[1]))
            return "get:message"
        elif mes=="logout":
            broadcast_data(sock,"{0} left the room.".format(online_niname[sock],datalist[0].split(":")[1]))
            del online_niname[sock]
            del online[sock]
            return "logout:successfully"
        else:
            return "Error:Unknown"
    except Exception as e:
        print(" parse data Error:%s"%e)
        return "Error:Protocol Error!"
if __name__ == "__main__":
    CONNECTION_LIST = [sys.stdin]
    RECV_BUFFER = 4096 
    PORT = 5000
    r=redis.StrictRedis()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("0.0.0.0", PORT))
    server_socket.listen(10)
    online={}
    online_niname={}
 
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
            elif sock==sys.stdin:
                junk=sys.stdin.readline()
                if junk=="exit":
                    running=False
                else:
                    broadcast_data(sock,"testing\n")
            else:
                try:
                    data = sock.recv(RECV_BUFFER)
                    if data:
                        redata=parse_data(sock,data.decode().rstrip())+"\n"
                        sock.send(redata.encode())
                        print("data type is %s"%(type(data)))
#data=False#测试时用
#                   r=receive(sock).decode()
                    else:
                        if online.get(sock):
                            del online[sock]
                        if online_niname.get(sock):
                            broadcast_cast(sock,"user(%s) is offline."%online_niname)
                            print("Client (%s) is offline" % online_niname[sock])
                            del online_niname[sock]
                        sock.close()
                        CONNECTION_LIST.remove(sock)
                        continue
                except Exception as e:
                    print("Error:%s"%e)
                    if online.get(sock):
                        del online[sock]
                    if online_niname.get(sock):
                        print("Client (%s) disconnected." % online_niname[sock])
                        del online_niname[sock]
                    sock.close()
                    CONNECTION_LIST.remove(sock)
                    continue
    server_socket.close()
