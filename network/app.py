import datetime
import flask
import redis
import pymysql
import random
import math

app = flask.Flask('Helloworld!')
app.secret_key = 'shiyanlou'
# 设置 redis 链接，使用 redis-py: https://github.com/andymccurdy/redis-py
r = redis.StrictRedis()
class Table_ctrl():
    def __init__(self,tablename):
        self.connect_db()
        self.tablename=tablename
    def get_randomId(self):
        randomId=1000000000+math.floor(random.random()*999999999)
        sql="select * from "+self.tablename+" where ID='"+str(randomId)+"'"
        print(sql)
        self.cur.execute(sql)
        while self.cur.fetchone():
                print("fetch again")
                randomId=self.get_randomId()
        return randomId
    def connect_db(self):
        self.conn=pymysql.connect(user="jin",password="123456",database="CHATROOM")
        self.cur=self.conn.cursor()
    def write_db(self,*data):
        sql="INSERT INTO "+str(self.tablename)+" VALUES('"+str(self.get_randomId())+"'"
        for i in range(len(data)):
            if type(data[i])==type("string"):
                sql+=",'"+str(data[i])+"'"
            else:
                sql+=","+str(data[i])
        sql+=")"
        print(sql)
        try:
            self.cur.execute(sql)
            self.conn.commit()
        except:
            print("writting  database error:%s")
    def checkExist(self,column,value):
        Exist=False
        if type(value)==type("string"):
            sql="select * from "+str(self.tablename)+" where "+str(column)+"='"+str(value)+"'"
        else:
            sql="select * from "+str(self.tablename)+" where "+str(column)+"="+str(value)
        print(sql)
        try:
            self.cur.execute(sql)
            if self.cur.fetchone():
                    Exist=True
        except:
            print("check value Error!")
        return Exist
    def __del__(self):
        self.conn.close()
# 消息生成器
def event_stream():
    pubsub = r.pubsub()
    # 订阅'chat'频道
    pubsub.subscribe('chat')
    # 开始监听消息，如果有消息产生在返回消息
    for message in pubsub.listen():
        # Server-Send Event 的数据格式以'data:'开始
        yield 'data: %s\n\n' % message['data']


# 登陆函数，首次访问需要登陆
@app.route('/login', methods=['GET','POST'])
def login():
    if flask.request.method == 'POST':
        # 将用户信息记录到 session 中
        flask.session['user'] = flask.request.form['user']
        return flask.redirect('/')
    return '<form action="" method="post">user: <input name="user">'


# 接收 javascript post 过来的消息
@app.route('/post', methods=['POST'])
def post():
    message = flask.request.form['message']
    try:
        write_db(message)
        print("wrote data to db!")
    except:
        print("error while writting data!")
    user = flask.session.get('user', 'anonymous')
    now = datetime.datetime.now().replace(microsecond=0).time()
    # 将消息发布到'chat'频道中
    r.publish('chat', u'[%s] %s: %s' % (now.isoformat(), user, message))
    return flask.Response(status=204)


# 事件流接口
@app.route('/stream')
def stream():
    # 返回的类型是'text/event-stream'，否则浏览器不认为是 SSE 事件流
    return flask.Response(event_stream(),
                          mimetype="text/event-stream")


@app.route('/')
def home():
    # 如果用户没有登陆的话，则强制登陆
    if 'user' not in flask.session:
        return flask.redirect('/login')
    return u"""
        <!doctype html>
        <title>chat</title>
        <script src="http://labfile.oss.aliyuncs.com/jquery/2.1.3/jquery.min.js"> </script>
        <style>body { max-width: 500px; margin: auto; padding: 1em; background: black; color: #fff; font: 16px/1.6 menlo, monospace; }</style>
        <p><b>hi, %s!</b></p>
        <p>Message: <input id="in" /></p>
        <pre id="out"></pre>
        <script>
            function sse() {
                // 接入服务器的事件流
                var source = new EventSource('/stream');
                var out = document.getElementById('out');
                source.onmessage = function(e) {
                    out.innerHTML =  e.data + '\\n' + out.innerHTML;
                };
            }
            // POST 消息到服务端
            $('#in').keyup(function(e){
                if (e.keyCode == 13) {
                    $.post('/post', {'message': $(this).val()});
                    $(this).val('');
                }
            });
            sse();
        </script>

    """ % flask.session['user']


if __name__ == '__main__':
    user=Table_ctrl("USER")
#user.write_db("jiu","password","NINAME",12,"f","123412341234")
    app.debug = True
    app.run('0.0.0.0',8989,threaded=True)
