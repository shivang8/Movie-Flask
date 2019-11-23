import os
from flask import Flask, request, redirect, url_for, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

class Users(db.Model):
	username = db.Column(db.String(20), primary_key=True)
	password = db.Column(db.String(20), nullable=False)
	genre = db.Column(db.String(30), nullable=False, default=0)
	
	def __repr__(self):
		return "Users('{}','{}','{}')".format(self.username,self.password,self.genre)

@app.route('/dashboard', methods=['POST','GET'])
def dashboard():
	if request.method == 'POST':
		username = request.form['username']
		username = username.lower()
		password = request.form['password']
		print("username = ",username,"\t password = ",password)
		result = Users.query.filter_by(username=username).first()
		if result.password == password :
			return render_template('dashboard.html')
		else:
			return render_template('login.html',error=1)
	else:
		return render_template('login.html',error=2)

@app.route('/signin')
def signin():
	return render_template('login.html',error=0)

@app.route('/signup')
def signup():
	return render_template('register.html')

@app.route('/task1')
def t1():
	return render_template('t1.html')

@app.route('/task2', methods=['POST','GET'])
def t2():
	if request.method == 'POST':
		username = request.form['username']
		username = username.lower()
		password = request.form['password']
		genre = request.form['option']
		print("username = ",username,"\t password = ",password,"\t genre = ",genre)
		temp = Users.query.filter_by(username=username).first()
		try:
			temp.username
			flag = True
		except:
			flag = False
		if flag:
			return render_template('register.html',error=1)
		else:
			new_entry = Users(username=username, password=password, genre=genre)
			db.session.add(new_entry)
			db.session.commit()
			return render_template('t2.html',error=1)
	else:
		return render_template('t2.html')

@app.route('/')
@app.route('/home')
def index():
	return render_template('home.html')

if __name__ == '__main__':
	app.run(host='127.0.0.1', port=12345, debug = True)
	#app.run(host='0.0.0.0', port=80, debug = True)