from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import *
from PyQt5.QtNetwork import *
import socket, select, string, sys,struct
import pickle

class LoginWindow(QMainWindow):
        close_signal=pyqtSignal()
        def __init__(self,*args,**kwargs):
            super().__init__(*args,**kwargs)
            self.setWindowTitle("544ChatRoom")
            #usernameLabel=QLabel("用户名：")
            #passwdLabel=QLabel("用户名：")
            self.username=QLineEdit()
            self.username.setPlaceholderText("username")
            self.password=QLineEdit()
            self.password.setPlaceholderText("password")
            self.password.setEchoMode(2)
            layout=QGridLayout()
            self.btnSend=QPushButton("login")
            self.btnQuit=QPushButton("quit")
            self.btnSend.pressed.connect(self.onBtnSend)
            self.btnQuit.pressed.connect(self.close)
            #layout.addWidget(usernameLabel,0,0)
            layout.addWidget(self.username,0,0,2,2)
            #layout.addWidget(passwdLabel,1,0)
            layout.addWidget(self.password,2,0,2,2)
            layout.addWidget(self.btnSend,4,0)
            layout.addWidget(self.btnQuit,4,1)
            widget=QWidget()
            widget.setLayout(layout)
            self.setCentralWidget(widget)
            self.btnSend.setStyleSheet("QPushButton:pressed{color:black;background-color:rgb(210,255,240);}")
            self.btnQuit.setStyleSheet("QPushButton:pressed{color:black;background-color:rgb(210,255,240);}")
            self.username.setStyleSheet("QLineEdit{border:1px solid rgba(210,255,240,0.7)},QLineEdit:focus{border:2px solid rgba(210,255,240)}")
            self.password.setStyleSheet("QLineEdit{border:1px solid rgba(210,255,240,0.7)},QLineEdit:focus{border:2px solid rgba(210,255,240)}")
            self.setStyleSheet("color:rgb(210,225,240);background-color:black")
            #self.resize(250,50)
            self.setFixedSize(280,120)
            self.center()
            self.setWindowOpacity(0.9)
            self.loginDialog=LoginDialog()
        def center(self):
                qr=self.frameGeometry()
                cp=QDesktopWidget().availableGeometry().center()
                qr.moveCenter(cp)
                self.move(qr.topLeft())
        def onBtnSend(self):
                usernamestr = self.username.text()
                passwordstr = self.password.text()
                self.loginDialog.connect()
                print("sending")
        def closeEvent(self,Event):
                self.close_signal.emit()
                print("loginwindow close")
                self.close()
        def keyPressEvent(self,QKeyEvent):
                if QKeyEvent.key()==Qt.Key_Return:
                    self.btnSend.animateClick()
class LoginDialog(QDialog):
    def __init__(self,parent=None):
        QDialog.__init__(self,parent)
        self.sock = QTcpSocket()
        print("init successfully!")
    def connect(self):
        self.sock.connectToHost("localhost", 5000)
        #if not self.sock.isWritable():
        loginMessage = "login:1,username:" + loginWindow.username.text() + ",password:" + loginWindow.password.text()
        print(loginMessage)
        if  self.sock.isWritable():
            self.sock.write(loginMessage.encode())
            self.sock.readyRead.connect(self.slotReadyRead)
        else:
            self.close()
        #else:
        #print("connection broke!")
    def slotReadyRead(self):
        if self.sock.bytesAvailable()>0:
            data=bytes(self.sock.readAll()).decode()
            print(data)
            head=data.split(":")[0]
            if head=="system":
                print("Login Failed!")
                print("niname"+data[1].split(":")[1])
            elif data[0].split(":")[1]=="successfully":
                niname=data[1].split(":")[1]
                chatWindow.show()
                chatWindow.view.append("<h3>"+niname+" enter ChatRoom</h3>")
                loginWindow.hide()
                self.close()
                print("Login successfully!")
    def send(self,data,type):
        if type=="data":
            pass
        elif type=="message":
            if self.sock.isWritable():
                self.sock.write(type.encode()+":".encode()+data.encode())
class ChatWindow(QMainWindow):
    def __init__(self,*args,**kwargs):
        super(ChatWindow,self).__init__(*args,**kwargs)
        self.setWindowTitle("ChatRoom")
        self.view = QTextBrowser(self)
        self.chat = QTextBrowser(self)
        self.content=QLineEdit()
        self.btnSend = QPushButton("send")
        layout = QGridLayout()
        layout.setContentsMargins(10,10,10,10)
        layout.addWidget(self.view,0,0,4,2)
        layout.addWidget(self.chat, 0,2,3,4)
        layout.addWidget(self.content, 3,2,1,3)
        layout.addWidget(self.btnSend, 3,5)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.center()
        self.setStyleSheet("ChatWindow{background-color:black}")
        self.setFixedSize(600,480)
        self.content.setFocus(Qt.ActiveWindowFocusReason)
    def slotReadyRead(self):
        if self.sock.bytesAvailable()>0:
            data=bytes(self.sock.readLine()).decode()
            mes=data.split(":")[1]
            if mes=="message":
                data="<h4>"+data.split(",")[0].split(":")[1]+"</h4>"
                self.chat.append(data)
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    def handle_click(self):
        if not self.isVisible():
            self.show()
        else:
            QMessageBox.warning(self,"Tips:","Service Down",QMessageBox.Cancel)
            self.close()
    def handle_close(self):
        self.close()
    def keyPressEvent(self,QKeyEvent):
        if QKeyEvent.key()==Qt.Key_Return:
            if self.content.hasFocus():
                loginWindow.loginDialog.send(self.content.text(),"message")
                self.chat.append("<h4 style='text-align:right'>"+self.content.text()+"</h4>")
                self.content.clear()
if __name__ == "__main__":
        app=QApplication(sys.argv)
        loginWindow=LoginWindow()
        chatWindow=ChatWindow()
        #loginWindow.btnSend.clicked.connect(chatWindow.handle_click)
        #loginWindow.btnSend.clicked.connect(loginWindow.close)
        #loginWindow.close_signal.connect(loginWindow.close)



        loginWindow.show()
        app.exec_()
'''
if(len(sys.argv) < 3) :
        print('Usage : filename hostname port ' )
        sys.exit()
    host = sys.argv[1]
    port = int(sys.argv[2])
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    try :
        s.connect((host, port))
    except :
        print('Unable to connect')
        sys.exit()
    print( 'Connected to remote host. Start sending messages' )
    prompt()
    while True:
        rlist = [sys.stdin, s]
        read_list, write_list, error_list = select.select(rlist , [], [])
        for sock in read_list:
            if sock == s:
                data = sock.recv(4096)
                if not data :
                    print ('\nDisconnected from chat server')
                    sys.exit()
                else :
                    sys.stdout.write(data.decode()+"\n")
                    prompt()
            else :
                msg = sys.stdin.readline()
                s.send(msg.encode())
                prompt()'''
