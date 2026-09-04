#JESUS IS LORD

from flask import Flask, redirect, url_for, render_template,render_template_string, jsonify, session , request, Blueprint #app_contextsendFile
from flask_cors import CORS
import os
from datetime import timedelta
from dotenv import load_dotenv 
from flask_sqlalchemy import SQLAlchemy

#from db import database

db = SQLAlchemy()
load_dotenv()
app = Flask(__name__)

CORS(app, resources={r"/api/*":{
    "origins": [
        f"https://{ os.getenv('URIUPLOADED')}",
        "http://127.5.7.1:1201"
    ]
}})
app.config["SQLALCHEMY_DATABASE_URI"] =  os.getenv('SQLALCHEMY_DATABASE_URI')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SESSION_COOKIE_SECURE"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=15)
app.config["SECRET_KEY"] =   os.getenv('SECRETE_KEY')
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_size":1,
    "max_overflow":0,
    "pool_recycle":120,
    "pool_pre_ping":True
}
db.init_app(app)
#from db_models import Emails
#from flask_sqlalchemy import SQLAlchemy
#from db import database
#db = database()
class Emails(db.Model):
    __tablename__ = "Emails"
    emailid = db.Column(db.Integer,primary_key=True,unique=True)
    emailtitle = db.Column(db.Text,default="Email Title")
    sendername = db.Column(db.String(80))
    senderemail = db.Column(db.String(80),default="Email Title")
    senderphone = db.Column(db.Integer,default="Email Title")
    createdDate = db.Column(db.DateTime(timezone=True),default=db.func.now(),nullable=False)
    message = db.Column(db.Text)

    def dt(self):
        return {"emailid":self.emailid,"emailtitleself:":self.emailtitle,"sendername":self.sendername,"senderemail":self.senderemail,"senderphone":self.senderphone,"message":self.message,"createdDate":self.createdDate}

with app.app_context():
    db.create_all()

#routes sfr e
@app.route("/")
def dashboard():
    
    return render_template("home-dashboard.html") 
@app.route("/api/send-mail", methods=["POST"])
def send():
    #data = request.get_json()
    title = request.form['title']
    name = request.form['name']
    email = request.form['email']
    phone = request.form['se']
    message = request.form['message']
    newemail = Emails(emailtitle=title,senderemail=email,sendername=name,senderphone=phone,message=message)
    try:
        db.session.add(newemail)
        db.session.commit()
        print("message: Successful - Created New Email")
        return jsonify({"message": f"Success {newemail.dt()}"})
    except Exception as e:
        return jsonify({"message": f"err {e}"})

@app.route("/dashboard")
def dashboard_main():
    emails = Emails.query.all()
    emails_all = []

    try:
        #db.session.add(newemail)
        db.session.commit()
        for data in emails: 
            emails_all.append(data.dt())
        print("message: Successful - Loaded All Emails")

        return render_template("read-email.html",data=emails_all)
    except Exception as e:
        print("message: Err - Created New Email")

        return jsonify({"message": f"err {e}"})
    
@app.route("/api/all", methods=["GET"])
def dataall():    
    emails = Emails.query.all()
    emails_all = []

    try:
      
        db.session.commit()
        for data in emails: 
            emails_all.append(data.dt())
        print("message: Successful - Loaded All Emails")

        return jsonify(emails_all)
    except Exception as e:
        print("message: Err - Created New Email")

        return jsonify({"message": f"err {e}"})
@app.route("/api/email/<emailid>/all", methods=["GET"])
def dataemailall(emailid):    
    
    emails = Emails.query.get_or_404(emailid)
    emails_all = []

    try:
  
        db.session.commit()
       
        print("message: Successful - Loaded This and All Emails")
        return jsonify(emails.dt())
    except Exception as e:
        return jsonify({"err":e})
@app.route("/api/del/<emailid>", methods=["GET","POST"])
def dataemailde(emailid):    
    #newemail = Emails(emailtitle=title,senderemail=email,sendername=name,senderphone=phone,message=message)      #db.session.add(newemail)#newemail = Emails(emailtitle=title,senderemail=email,sendername=name,senderphone=phone,message=message)  #db.session.add(newemail)
    emails = Emails.query.get_or_404(emailid)
    emails_all = []

    try:
        db.session.delete(emails)
        db.session.commit()

        print("message: Successful - delete This and All Emails")
        return jsonify({"":"message: Successful - delete This and All Emails"})
    except Exception as e:
        return jsonify({"err":e})
            
if __name__ == "__main__":
    app.run(debug=True,port="1201",host="127.5.7.1")