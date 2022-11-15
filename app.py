from flask import Flask, render_template, request, url_for, redirect,flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
app.secret_key = "super secret key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:\\Users\Daniel Coti\\Documents\\Codigo\Level Up_ Proyecto1\\database\\cine.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    username = db.Column(db.String(30))
    surname = db.Column(db.String(30))
    password = db.Column(db.String(60))
    email = db.Column(db.String(256),primary_key=True)
    phone = db.Column(db.Integer)
    created_at = db.Column(db.DateTime(), default=datetime.now())

"""

class Movie(db.Model):
    __tablename__ = 'movies'
    id_movie= db.Column(db.Integer, primary_key = True, autoincrement = True)
    title = db.Column(db.String(256))
    img= db.Column(db.String(max))
    classification = db.Column(db.String(10))
    created_at = db.Column(db.DateTime(), default=datetime.now())
    
class Function(db.Model):
    __tablename__ = 'functions'
    id_function= db.Column(db.Integer, primary_key=True, autoincrement=True)
    seat = db.Column(db.String(256))
    datefuncion = db.Column(db.DateTime())
    #id_movie = db.Column(db.Integer, db.ForeignKey('movies.id_movie'))
    created_at = db.Column(db.DateTime(), default=datetime.now()) 

class Ticket(db.Model):
    __tablename__ = 'tickets'
    id_ticket= db.Column(db.Integer, primary_key = True)
    seat= db.Column(db.String(256))
    #id_function = db.Column(db.Integer, db.ForeignKey('functions.id_function'))  
    created_at = db.Column(db.DateTime(), default=datetime.now()) """

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        pass
    else:
        return render_template('auth/login.html')

@app.route('/sing_up', methods=['GET','POST'])
def sing_up():
    if request.method == 'POST':
        user=User(username=request.form['username'],surname=request.form['surname'],password=request.form['password'],email=request.form['email'],phone=request.form['phone'])
        email=db.session.query(User).filter(User.email == user.email).first()
        if email == None:
            db.session.add(user)
            db.session.commit()
            flash("Congratulations!!")
        else: 
            flash("User already exists")  
        return render_template('auth/sing_up.html')
    else:
        return render_template('auth/sing_up.html')


if __name__ == '__main__':
    app.run(debug=True)

