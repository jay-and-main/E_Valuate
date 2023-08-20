from flask import Flask, render_template, redirect, url_for, request,flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Length, Email
from flask_sqlalchemy  import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename
import os
from preprocessor import PreProcess
import cv2
from model import E_valuate
import sqlite3 as sql

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "static/UploadedImages"
app.config['SECRET_KEY'] = 'aadhavanissupercool'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Class 12 CS/CS Project/E_Valuate/E_valuate/database1.db'
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    prevscore = db.Column(db.Integer)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])

class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Length(max=50)])
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))

        return '<h1>Invalid username or password</h1>'
        #return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return '<h1>New user has been created!</h1>'
        #return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'

    return render_template('signup.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', name=current_user.username)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/display', methods = ['GET', 'POST'])
def save_file():
    if request.method == 'POST':
        f = request.files['file']
        filename = secure_filename(f.filename)
        f.save(app.config['UPLOAD_FOLDER'] + filename)
        file = cv2.imread(app.config['UPLOAD_FOLDER'] + filename)
        PreProcess(file)
        l=E_valuate()
        s=''
        for i in l:
            s+=i
        count=0
        ans_key=list('MYNAMEIS')
        for i in range(len(l)):
            if l[i]==ans_key[i]:
                count+=1
        per=int((count/len(ans_key))*100)
        con = sql.connect('database1.db')
        c =  con.cursor()
        c.execute("select prevscore from user where username='%s'"%(current_user.username))
        rows=c.fetchall()
        for i in rows:
            my_prev_score=i
        c.execute("UPDATE user SET prevscore = %s WHERE username = '%s'" %(per,current_user.username))
        con.commit()
        con.close()
        content="Your answer is: "+str(per)+"% correct"+"\n"+"\n"+"The correct answer is: MYNAMEIS "+"Your answer was read as: "+s+"\n"+"\n"+"Your previous answer was: "+str(my_prev_score[0])+"% correct"
    return render_template('content.html',content=content)


if __name__ == '__main__':
    app.run(debug=True)
