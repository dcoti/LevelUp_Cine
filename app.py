from flask import Flask, render_template, request, url_for, redirect,flash,session
from sqlalchemy.sql import select
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = "super secret key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:\\Users\Daniel Coti\\Documents\\Codigo\Level Up_ Proyecto1\\database\\cine.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False

db = SQLAlchemy(app)
user_=None
name=None
seats=("A1,A2,A3,A4,A5,A6,A7,A8,A9,A10,B1,B2,B3,B4,B5,B6,B7,B8,B9,B10,C1,C2,C3,C4,C5,C6,C7,C8,C9,C10,D1,D2,D3,D4,D5,D6,D7,D8,D9,D10,E1,E2,E3,E4,E5,E6,E7,E8,E9,E10")
val=["A1","A2","A3","A4","A5","A6","A7","A8","A9","A10","B1","B2","B3","B4","B5","B6","B7","B8","B9","B10","C1","C2","C3","C4","C5","C6","C7","C8","C9","C10","D1","D2","D3","D4","D5","D6","D7","D8","D9","D10","E1","E2","E3","E4","E5","E6","E7","E8","E9","E10"]

class User(db.Model):
    __tablename__ = 'users'
    username = db.Column(db.String(30))
    surname = db.Column(db.String(30))
    password = db.Column(db.String(60))
    email = db.Column(db.String(256),primary_key=True)
    phone = db.Column(db.Integer)
    created_at = db.Column(db.DateTime(), default=datetime.now())

class Movie(db.Model):
    __tablename__ = 'movies'
    id_movie= db.Column(db.Integer, primary_key = True, autoincrement = True)
    title = db.Column(db.String(256))
    img= db.Column(db.String(256))
    classification = db.Column(db.String(10))
    created_at = db.Column(db.DateTime(), default=datetime.now())
    
class Function(db.Model):
    __tablename__ = 'functions'
    id_function= db.Column(db.Integer, primary_key=True, autoincrement=True)
    seat = db.Column(db.String(256))
    datefuncion = db.Column(db.String(256))
    id_movie = db.Column(db.Integer, db.ForeignKey('movies.id_movie'))
    created_at = db.Column(db.DateTime(), default=datetime.now()) 

class Ticket(db.Model):
    __tablename__ = 'tickets'
    id_ticket= db.Column(db.Integer, primary_key = True)
    seat= db.Column(db.String(256))
    id_function = db.Column(db.Integer, db.ForeignKey('functions.id_function'))  
    user=db.Column(db.String(256))
    created_at = db.Column(db.DateTime(), default=datetime.now()) 

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        user= db.session.query(User).filter(User.email==request.form['username']).first()
        if user==None:
            flash("Username does not exist")
            return render_template('auth/login.html')
        else:
            if user.password==request.form['password']:
                session["user_session"]=request.form['username']
                global user_
                user_=request.form['username']
                return redirect('home')
                #return render_template('/inicio.html',us=us,em=em,movies=movies)
            else:
                flash("Password incorrect")
                return render_template('auth/login.html')  
    else:
        return render_template('auth/login.html')

@app.route('/home', methods=['GET'])
def home():
    movies=Movie.query.all()
    if 'user_session' in session:
        user= db.session.query(User).filter(User.email==user_).first()
        us=user.username;
        global name
        name=us
        em=user.email;
        return render_template('/inicio.html',us=us,em=em,movies=movies,user_=user_)
    else:
        us=None
        return render_template('/inicio.html',movies=movies,us=us)

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

@app.route('/upload_movie', methods=['GET','POST'])
def upload_upload():
    if request.method== 'POST':
        movie= Movie(title=request.form['title'],img=request.form['img'],classification=request.form['classification'])
        mov=db.session.query(Movie).filter(Movie.title==movie.title).first()
        if mov ==None:
            db.session.add(movie)
            db.session.commit()
            flash("movie added")
        else:
            flash("movie already exists")
        return render_template('auth/upload_movie.html')      
    else:
        return render_template('auth/upload_movie.html')

@app.route('/functions_movie', methods=['GET','POST'])
def functions_movie():
    if request.method== 'POST':
        movie=Function(seat=seats, datefuncion=request.form['DateFunction'],id_movie=request.form['id_movie'])
        val=request.form['id_movie']
        date=db.session.query(Function).filter(Function.datefuncion==movie.datefuncion).first()
        if date==None:
            db.session.add(movie)
            db.session.commit()
            flash("Function added")      
        else:
            if str(date.id_movie) == val:
                flash("Function already exists")
            else:
                print("entra aqui")
                print(val)
                print(date.id_movie)
                db.session.add(movie)
                db.session.commit()
                flash("Function added")       
        return render_template('auth/functions.html')
    else:
        return render_template('auth/functions.html')

@app.route('/logout', methods=['GET'])
def logout():
    session.pop('user_session', None)
    global user_
    user_= None
    return redirect('/login')

@app.route('/buy_ticket/<movies>', methods=['GET', 'POST'])
def buy_tickets(movies):
    movie= db.session.query(Movie).filter(Movie.id_movie==movies).first()
    functions=Function.query.all()
    if request.method == 'GET':
        if 'user_session' in session:
            return render_template('auth/buy_ticket.html',movie=movie,functions=functions,us=True)  
        else:
            return render_template('auth/buy_ticket.html',movie=movie,functions=functions,us=None)  
    else:
        if 'user_session' in session:
            fun=request.form['function']
            se=request.form['seat'].split(",")
            prueba=""
            aux=False
            for i in se:
                aux=db.session.query(Ticket).filter(Ticket.seat==str(i)).first()
                if aux!=None:
                    prueba+=str(i)+" "
            for i in se:
                for j in val:
                    if i == j:
                        aux=True
                        break
                    else:
                        aux=False
                if aux==False:
                    flash("out of range")
                    break
            if aux!=False:
                if prueba=="":
                    for i in se: 
                        f=db.session.query(Function).filter(Function.id_function==str(fun)).first()
                        tic=Ticket(seat=str(i),id_function=f.datefuncion,user=session['user_session'])
                        db.session.add(tic)
                        db.session.commit()
                    flash("Ok")
                else:
                    flash("Seats "+prueba+" occupied")
            return render_template('auth/buy_ticket.html',movie=movie,functions=functions,us=True)  
        else:
            flash("You must log in")
            return render_template('auth/buy_ticket.html',movie=movie,functions=functions,us=None) 

@app.route('/tickets', methods=['GET'])
def tickets():
    tic=Ticket.query.all()
    return render_template('/tickets.html',tic=tic,user_=user_)


@app.route('/delate/<id_ticket>',methods=['GET'])
def delate(id_ticket):
    db.session.query(Ticket).filter(Ticket.id_ticket==id_ticket).delete()
    db.session.commit()
    return redirect(url_for('tickets'))
    

if __name__ == '__main__':
    app.run(debug=True)

