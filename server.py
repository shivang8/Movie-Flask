import os
import json
import requests
from datetime import datetime
from flask import Flask, request, redirect, url_for, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Users(db.Model):
	username = db.Column(db.String(20), primary_key=True)
	password = db.Column(db.String(20), nullable=False)
	genre1 = db.Column(db.String(30), nullable=False)
	genre2 = db.Column(db.String(30), nullable=False)
	genre3 = db.Column(db.String(30), nullable=False)
	genre4 = db.Column(db.String(30), nullable=False)
	genre5 = db.Column(db.String(30), nullable=False)
	
	def __repr__(self):
		return "Users('{}','{}','{}','{}','{}','{}','{}')".format(self.username,self.password,self.genre1,self.genre2,self.genre3,self.genre4,self.genre5)

@app.route('/output', methods=['POST','GET'])
def output():
	body = {}
	if request.method == 'POST':
		body['type'] = request.form['type']
		flag = 0
		if body['type'] == 'create':
			flag = 3
			body['index'] = 'my-index'
			exe = {}
			exe['userId'] = request.form['userId']
			exe['movieId'] = request.form['movieId']
			exe['rating'] = request.form['rating']
			exe['timestamp'] = request.form['timestamp']
			body['exec'] = exe
		elif body['type'] == 'search':
			flag = 1
			exe = {}
			boo = {}
			must = []
			v1 = request.form['userId']
			v2 = request.form['movieId']
			v3 = request.form['rating']
			v4 = request.form['timestamp']
			if v1 != '':
				temp = {}
				t = {}
				t['userId'] = v1
				temp['match'] = t
				must.append(temp)
			if v2 != '':
				temp = {}
				t = {}
				t['movieId'] = v2
				temp['match'] = t
				must.append(temp)
			if v3 != '':
				temp = {}
				t = {}
				t['rating'] = v3
				temp['match'] = t
				must.append(temp)
			if v4 != '':
				temp = {}
				t = {}
				t['timestamp'] = v4
				temp['match'] = t
				must.append(temp)
			#boo['bool'] = must
			#exe['query'] = boo
			#body['exec'] = exe
			body['exec'] = must
		elif body['type'] == 'update':
			flag = 2
			user = request.form.get("user")
			movie = request.form.get("movie")
			rating = request.form.get("rating")
			now = datetime.now()
			current_time = now.strftime("%H:%M:%S")
			data = {
				'type': 'update',
				'index': 'my-index',
				'exec':{
					'match':
						[
							{'match': {'userId': user}},
							{'match': {'movieId': movie}}
						],
					'change':
						{
							'rating':rating,
							'timestamp':current_time
						}
					}
				}
			body = data
		elif body['type'] == 'delete':
			flag = 4
			user = request.form.get("user")
			movie = request.form.get("movie")
			rating = request.form.get("rating")
			now = datetime.now()
			current_time = now.strftime("%H:%M:%S")
			data = {
				'type': 'update',
				'index': index,
				'exec': {
					'userId': user,
					'movieId': movie,
					'rating': rating,
					'timestamp': current_time
					}
				}
			body = data
	json_data = json.dumps(body)
	print("\n\n",json_data,"\n\n")
	r=requests.get("http://localhost:8080",json=body)
	if flag == 1:
		json_data=r.json()
		data = []
		for line in json_data:
			data.append(line['_source'])
		return render_template('output.html',flag=1, data=data)
	elif flag == 2:
		return render_template('output.html',flag=2, data=data)
	return render_template('output.html')

@app.route('/c')
def crud_c():
	return render_template('C.html')

@app.route('/r')
def crud_r():
	return render_template('R.html')

@app.route('/u')
def crud_u():
	return render_template('U.html')

@app.route('/d')
def crud_d():
	return render_template('D.html')

@app.route('/dashboard', methods=['POST','GET'])
def dashboard():
	if request.method == 'POST':
		username = request.form['username']
		username = username.lower()
		password = request.form['password']
		print("username = ",username,"\t password = ",password)
		result = Users.query.filter_by(username=username).first()
		try:
			result.username
			flag = True
		except:
			flag = False
		if flag:
			if result.password == password :
				genre = []
				genre.append(result.genre1)
				genre.append(result.genre2)
				genre.append(result.genre3)
				genre.append(result.genre4)
				genre.append(result.genre5)
				return render_template('dashboard.html')
			else:
				return render_template('login.html',error=1)
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
		genre1 = request.form['option1']
		genre2 = request.form['option2']
		genre3 = request.form['option3']
		genre4 = request.form['option4']
		genre5 = request.form['option5']
		
		print("username = ",username,"\t password = ",password,"\t genre1 = ",genre1,"\t genre2 = ",genre2,"\t genre3 = ",genre3,"\t genre4 = ",genre4,"\t genre5 = ",genre5)
		temp = Users.query.filter_by(username=username).first()
		try:
			temp.username
			flag = True
		except:
			flag = False
		if flag:
			return render_template('register.html',error=1)
		else:
			new_entry = Users(username=username, password=password, genre1=genre1, genre2=genre2, genre3=genre3, genre4=genre4, genre5=genre5)
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