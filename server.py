import os
import json
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
	genre = db.Column(db.String(30), nullable=False, default=0)
	
	def __repr__(self):
		return "Users('{}','{}','{}')".format(self.username,self.password,self.genre)

@app.route('/output', methods=['POST','GET'])
def output():
	body = {}
	if request.method == 'POST':
		body['type'] = request.form['type']
		if body['type'] == 'create':
			body['index'] = 'my-index'
			exe = {}
			exe['userId'] = request.form['userId']
			exe['movieId'] = request.form['movieId']
			exe['rating'] = request.form['rating']
			exe['timestamp'] = request.form['timestamp']
			body['exec'] = exe
		elif body['type'] == 'search':
			exe = {}
			exe['size'] = request.form['size']
			#query = {}
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
			boo['bool'] = must
			exe['query'] = boo
			body['exec'] = exe
		elif body['type'] == 'update':
			index = request.form.get("index")
			user = request.form.get("user")
			movie = request.form.get("movie")
			rating = request.form.get("rating")
			now = datetime.now()
			current_time = now.strftime("%H:%M:%S")
			data = {
				'type': 'update',
				'index': index,
				'exec':{
					'userId':user,
					'movieId':movie,
					'rating':rating,
					'timestamp':current_time
			   		}
				}
			body = data
		elif body['type'] == 'delete':
			index = request.form.get("index")
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
	return render_template('output.html')
	
# body={'type':'delete',
# 	  'index': 'my-index',
# 	  'exec': {
# 	  'query': {
# 	  	'match': {
# 	  	'userId': '890'
# 	  	}
# 	  	# 'movieId': '300',
# 	  	# 'rating' :'1.5'	,
# 	  	# 'timestamp' : '1093143913'
# 	  }
# 	  }
# 	  }

# body= {'type': 'update',
# 	   'index': 'my-index',
# 	   'exec': {
# 	     "script": {
# 	     	"inline": "ctx._source.rating='9.5'; ctx._source.timestamp='1113188335'"
# 	        # "rating": "5.5'",
# 	        # "timestamp": "1113188330"
# 	     },
# 	     "query": {
# 	        "match": {
# 	            "userId": "890"
# 	        }
# 	     }
#      }
# }

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