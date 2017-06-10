from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import *
import socket, select, string, sys,struct
import pickle
 
def send(channel,*args):
    buffers=pickle.dumps(args)
    value=socket.htonl(len(buffers))
    size=struct.pack("L",value)
    channel.send(size)
    channel.send(buffers)
def prompt():
    sys.stdout.write('<Username>')
    sys.stdout.flush()
class LoginWindow(QMainWindow):
        close_signal=pyqtSignal()
        def __init__(self,*args,**kwargs):
            super().__init__(*args,**kwargs)
            self.setWindowTitle("544聊天室")
            usernameLabel=QLabel("用户名：")
            passwdLabel=QLabel("用户名：")
            self.username=QLineEdit()
            self.password=QLineEdit()
            self.password.setEchoMode(2)
            layout=QGridLayout()
            self.btnSend=QPushButton("登录")
            self.btnQuit=QPushButton("退出")
            self.btnSend.pressed.connect(self.onBtnSend)
            self.btnQuit.pressed.connect(self.onBtnQuit)
            layout.addWidget(usernameLabel,0,0)
            layout.addWidget(self.username,0,1)
            layout.addWidget(passwdLabel,1,0)
            layout.addWidget(self.password,1,1)
            layout.addWidget(self.btnSend,2,0)
            layout.addWidget(self.btnQuit,2,1)
            widget=QWidget()
            widget.setLayout(layout)
            self.setCentralWidget(widget)
            self.btnSend.setStyleSheet("QPushButton:pressed{color:black;background-color:white;}")
            self.btnQuit.setStyleSheet("QPushButton:pressed{color:black;background-color:white;}")
            self.username.setStyleSheet("QLineEdit{border:1px solid rgb(210,255,240)}")
            self.password.setStyleSheet("QLineEdit{border:1px solid rgb(210,255,240)}")
            #self.resize(250,50)
            self.setFixedSize(250,100)
            self.center()
            self.setStyleSheet("color:rgb(210,225,240);background-color:black")
        def center(self):
                qr=self.frameGeometry()
                cp=QDesktopWidget().availableGeometry().center()
                qr.moveCenter(cp)
                self.move(qr.topLeft())
        def onBtnSend(self):
                usernamestr = self.username.text()
                print(usernamestr)
                passwordstr = self.password.text()
                print(passwordstr)
                print("sending")
        def onBtnQuit(self):
                self.close()
        def closeEvent(self,Event):
            #self.close_signal.emit()
            #self.close()
            pass
class ChatWindow(QMainWindow):
    def __init__(self,*args,**kwargs):
        super(ChatWindow,self).__init__(*args,**kwargs)
        self.view=QTreeView(self)
        self.chat=QTreeView(self)
        self.btnSend=QPushButton("send")
        layout=QGridLayout()
        layout.addWidget(self.view, 0, 0)
        layout.addWidget(self.view,1,0)
        layout.addWidget(self.chat, 0,1)
        layout.addWidget(self.btnSend, 1,1)
        widget=QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.center()
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    def handle_click(self):
        if not self.isVisible():
            self.show()
    def handle_close(self):
        self.close()
if __name__ == "__main__":
        app=QApplication(sys.argv)
        loginWindow=LoginWindow()
        chatWindow=ChatWindow()
        loginWindow.btnSend.clicked.connect(chatWindow.handle_click)
        loginWindow.btnSend.clicked.connect(loginWindow.hide)
        loginWindow.close_signal.connect(loginWindow.close)
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
