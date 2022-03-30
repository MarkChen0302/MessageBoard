import this
import config
from operator import methodcaller
from flask import Flask, redirect, render_template, request, url_for
from datetime import datetime

class WebMessage:
    id=0
    author=''
    content=''
    createTime=''
    def __init__(self,author,content,id) :
        self.author=author
        self.content=content
        self.id=id
        self.createTime=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
app = Flask(__name__)
app.config.from_object(config)
user={'mark':'123'}
MessageList=[WebMessage('123','321',0)]
@app.route('/Home/',methods=['GET'])
def home():
    if 'username' in request.args:
        username=request.args['username']
        return render_template('Home.html',username=username,posts=MessageList,isAdmin=True)
    return render_template('Home.html',posts=MessageList,isAdmin=False)

@app.route('/logout',methods=['GET'])
def logout():
    return redirect(url_for('home'))
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        name=request.form.get('username')
        password=request.form.get('password')
        if name in user:
            if user[name] == password:
                result=name
        return redirect(url_for('home',username=result))
    else:
        return render_template('login.html')

@app.route('/posts/',methods=['GET','POST'])
def posts():
    if  request.method == 'POST':
        author=request.form.get('author')
        content=request.form.get('content')
        message=WebMessage(author,content,MessageList[-1].id+1)
        print(message.id)
        MessageList.append(message)
        return redirect(url_for('home'))
    else:
        if 'delete' in request.args:
            id=request.args.get('delete')
            for item in MessageList:
                if id == str(item.id):
                    MessageList.remove(item)
                    return redirect(url_for('home'))
        return render_template('newpost.html')


       

if __name__ == '__main__':
    app.run()


        