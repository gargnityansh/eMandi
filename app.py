from flask import Flask, render_template, request, jsonify, redirect,flash, make_response
from flask_bootstrap import Bootstrap
import db_query
from flask_cors import CORS
import json
from emails import sendMail

app = Flask(__name__)
Bootstrap(app)
CORS(app)
app.secret_key = "super secret key"

@app.route('/')
@app.route('/index.html')
def index():
	username = request.cookies.get("username")
	games_status, games_list = db_query.searchGame("%")
	if games_status == 200:
		return render_template('index.html', games=games_list,username=username)
	else:
		flash(games_list)
		return render_template('index.html',games=0,username=username)


@app.route('/search',  methods=['GET'])
def search():
	username = request.cookies.get("username")
	print("hello mr. how do you do",request.args.get('search'))
	if not request.args.get('search'):
		flash("Please provide a correct vlaue")
		return redirect("/")
	game_status, game_list = db_query.searchGame(request.args.get('search'))
	if game_status == 500:
		return redirect("/")
	elif game_status==404:
		flash(game_list)
		return redirect("index.html")
	elif game_list == None:
		return redirect("/")
	return render_template('index.html', games=game_list,username=username)


@app.route('/login.html')
def login():
	return render_template('login.html')

@app.route('/signup.html')
def signup():
	return render_template('signup.html')

"""@app.route('/photo-detail.html')
def photodetail():
	username = request.cookies.get("username")
	return render_template('photo-detail.html',username=username)
"""

@app.route('/about.html')
def about():
	username = request.cookies.get("username")
	return render_template("about.html",username=username)

@app.route('/contact.html')
def contact():
	username = request.cookies.get("username")
	return render_template('contact.html',username=username)

@app.route('/contact', methods=["POST"])
def contactDetails():
	name = request.form.get("name")
	email = request.form.get("email")
	subject = request.form.get("subject")
	message = request.form.get("message")
	contactDetails = {"name":name, "email":email, "subject":subject, "message":message}
	sendMail('famegamecorp2020@gmail.com', contactDetails)
	flash("Your query has been registered. We will contact you soon")
	return redirect("/contact.html")


@app.route('/register', methods=['POST'])
def register():
	#method to register user into database
	username = request.form.get('username')
	fname = request.form.get('fname')
	lname = request.form.get('lname')
	phno = request.form.get('phno')
	emailid = request.form.get('emailid')
	password = request.form.get('password')
	usertype = request.form.get('usertype')
	if usertype=="Gamer":
		usertype = False
	else:
		usertype = True
	if username==None or fname==None or lname == None or phno ==None or emailid==None or password==None:
		flash("incorrect input")
		return render_template('signup.html')
	else:
		user = {"username":username,"fname":fname, "lname":lname, "phno":phno, "emailid":emailid, "password":password, "usertype":usertype}
		print(user)
		registeration,error = db_query.registerUser(user)
		if registeration==500:
			flash(error)
			return render_template('signup.html')
		elif registeration==200:
			resp = make_response(redirect('/'))
			resp.set_cookie("username",username)
			return resp

@app.route('/signin', methods=['POST'])
def signin():
	emailid = request.form.get('emailid')
	password = request.form.get('password')
	if emailid==None or password==None:
		return render_template('login.html')
	else:
		user = {'emailid':emailid, "password":password}
		check_status, error = db_query.checkUser(user)
		print(user)
		if check_status==500:
			flash(error)
			return render_template('login.html')
		elif check_status==404:
			flash("invalid login credentials")
			return render_template('login.html')
		elif check_status==200:
			resp = make_response(redirect("/"))
			resp.set_cookie("username", error)
			return resp


@app.route('/game', methods=["GET","POST"])
def game():
	username = request.cookies.get("username")
	gameName = request.args.get("type")
	print(gameName)
	game_desc_status, game_desc = db_query.searchGame(gameName)
	category_status , category = db_query.findGameCategory(gameName)
	print(game_desc)
	if game_desc_status==200:
		return render_template("photo-detail.html",game_desc = game_desc,username=username, category=category)
	else:
		return redirect("/")

@app.route('/logout')
def logout():
	resp = make_response(redirect('/'))
	resp.delete_cookie('username')
	return resp

@app.route('/forgetpassword', methods=["POST"])
def forgetPassword():
	emailid = request.form.get("emailid")
	if emailid==None:
		flash("invalid emailid")
		return render_template("forgetpassword.html")
	else:
		mail_status, mail_error = sendMail(emailid)
		if mail_status == 200:
			flash("reset link has been sent to your mail id")
			return render_template("forgetpassword.html")
		else:
			flash("Error. Please try again after some time")
			return render_template("forgetpassword.html")

@app.route("/forgetpassword.html")
def forgetPasswordPage():
	return render_template("forgetpassword.html")


if __name__ == "__main__":
	app.run(debug=True)