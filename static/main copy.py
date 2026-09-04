#JESUS IS LORD

from flask import Flask, redirect, url_for, render_template,render_template_string, jsonify, session , request, Blueprint #app_contextsendFile
from flask_cors import CORS
import os
from datetime import timedelta
#from dotenv import load_dotenv 
from flask_sqlalchemy import SQLAlchemy

#from db import database

db = SQLAlchemy()
#load_dotenv()
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///emails-db.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SESSION_COOKIE_SECURE"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=15)
app.config["SECRET_KEY"] =  "sqlite:///emails-db.db"
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_size":1,
    "max_overflow":0,
    "pool_recycle":120,
    "pool_pre_ping":True
}
db.init_app(app)
class Emails(db.Model):
    __tablename__ = "Emails"
    emailid = db.Column(db.Integer,primary_key=True,unique=True)
    emailtitle = db.Column(db.Text,default="Email Title")
    sendername = db.Column(String(80))
    senderemail = db.Column(db.String(80),default="Email ")
    senderphone = db.Column(db.Integer,default=7)
    message = db.Column(db.Text)

    def dt(self):
        return {"emailid":self.emailid,"emailtitleself:":self.emailtitle,"sendername":self.sendername,"senderemail":self.senderemail,"senderphone":self.senderphone,"message":self.message}


with app.app_context():
    db.create_all()

#routes sfr e
@app.routes("/")
def dashboard():
    return render_template_string("""
            <Doctype html>
            <html lang=en>
            <head>
                <title>Image Uploader> </title>
                <meta charset="UTF-8">
            </head>
            <body>
                <h1> JESUS IS LORD </h1>
                <h2> Upload Imagge Here:</h2>
                <form enctype="multipart/form-data" action="/signup" method="post">
                    <label for="file">Upload piture</label>
                    <input id="file" type="file" name="file">
                    <input type="submit" value="click">
                </form>
            </body>
            </html>""")
    #return render_template("home-dashboard.html") sendFile
@app.routes("/api/send-mail", methods=["POST"])
def send():
    data = request.form.json()
    title = data.title
    name = data.name
    email = data.email
    phone = data.se
    message = data.message
    newemail = Emails(emailtitle=title,senderemail=email,sendername=name,senderphone=phone,message=message)
    try:
        db.session.add(newemail)
        db.session.commit()
        return jsonify({"message": f"Success {newemail}"})
    except Exception as e:
        return jsonify({"message": f"err {e}"})

    
@app.routes("/api/all", methods=["GET"])
def dataall():    
    #newemail = Emails(emailtitle=title,senderemail=email,sendername=name,senderphone=phone,message=message)
    emails = Emails.query.all()
    emails_all = []

    try:
        #db.session.add(newemail)
        db.session.commit()
        for data in emails: 
            emails_all.append(data)
        return jsonify(emails_all)
    except Exception as e:
        return jsonify({"message": f"err {e}"})
if __name__ == "__main__":
    app.run(debug=True,port="1201",host="127.5.7.1")