from flask import Flask,request
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
app = Flask(__name__)

sqlhost = os.getenv("MYSQL_HOST","localhost") 
port = os.getenv("MYSQL_PORT",3306) 
user = os.getenv("MYSQL_USER","user")
password = os.getenv("MYSQL_PASSWORD","")
database= os.getenv("MYSQL_DATABASE","DEMO")

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+mysqlconnector://{user}:{password}@{sqlhost}:{port}/{database}"
db = SQLAlchemy(app,engine_options={ 'connect_args': { 'connect_timeout': 5 }})
migrate = Migrate(app,db)

class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30))
    post = db.Column(db.String(80))
    pub_date = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)

    def __init__(self, title, post):
        self.post = post
        self.title = title

    def __repr__(self):
        return f"<POST: {self.post}>"



@app.route('/')
def startpage():
    return "Home : Post to /post to add a post\n\n"

@app.route('/healthcheck')
def healthcheck():
    return '{"status":"ok","sqlconnection":"ok"}'

@app.route('/get')
def get():
    posts = Post.query.all()
    return "<BR>\n".join([f"{post.id}:{post.title} le {post.pub_date} => {post.post}" for post in posts])+"\n"


@app.route('/post',methods = ['POST', 'GET'])
def post():
    if request.method == "GET":
        title=request.args.get("title","defaut title")
        post=request.args.get("post","defaut post")
        p=Post(title,post)
        db.session.add(p)
        db.session.commit()
        db.commit()
        return f"Add to database : {title} : {post}\n"

    if request.method == "POST":
       pass 

@app.route('/delete')
def delete_all():
    nb_delete=Post.query.delete() 
    db.session.commit()
    return f"Delete data ok : {nb_delete}\n"



if __name__ == '__main__':
    db.create_all() 
    app.run(host = "0.0.0.0", port = 5000)
