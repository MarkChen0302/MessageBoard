from sqlalchemy import true
import config
from flask import Flask, redirect, render_template, request, url_for
from datetime import datetime
from flask_login import LOGIN_MESSAGE, LoginManager,UserMixin,login_user,current_user,login_required,logout_user
import os
class User(UserMixin):
    isAdmin=true
    pass

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

baseDir=os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config.from_object(config)
app.secret_key='123'

loginManager=LoginManager()
# loginManager=LoginManager(app)
loginManager.login_view='login'
loginManager.login_message_category='info'
loginManager.login_message='Access denied'
loginManager.init_app(app)

users={'mark':{'password':'123'}}
MessageList=[WebMessage('123','321',0)]

def quert_user(user_id):
    for user in users.keys():
        if user_id == user:
            return user
@loginManager.user_loader
def load_user(user_id):
    if quert_user(user_id) is not None:
        curr_user=User()
        curr_user.id=user_id
        return curr_user

@app.route('/Home/',methods=['GET'])
def home():
    if 'username' in request.args:
        username=request.args['username']
        return render_template('Home.html',posts=MessageList,isAdmin=True)
    return render_template('Home.html',posts=MessageList,isAdmin=False)

@app.route('/logout',methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))
    
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        name=request.form.get('username')
        password=request.form.get('password')
        user= quert_user(name)
        if user is not None and users[name]['password'] == password:
            curr_user=User()
            curr_user.id=name
            login_user(curr_user)
        return redirect(url_for('home'))
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


        