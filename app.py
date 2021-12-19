from flask import Flask, render_template, request, jsonify, redirect,flash, make_response
from flask_bootstrap import Bootstrap
import db_query
from flask_cors import CORS
import json
from emails import sendMail
import razorpay
import datetime


app = Flask(__name__)
Bootstrap(app)
CORS(app)
app.secret_key = "super secret key"
client = razorpay.Client(auth=("rzp_test_Y8qqx6ykwxSLLJ", "CR89f0GyAecvqO4DSNgLCmYC"))

@app.route('/hello')
def hello():
	return "Hello World"

@app.route('/')
@app.route('/index.html')
def index():
	username = request.cookies.get("username")
	usertype = bool(request.cookies.get("usertype"))
	print("in index usertype", usertype)
	games_status, games_list = db_query.searchGame("%")
	if games_status == 200:
		return render_template('index.html', games=games_list,username=username,usertype=usertype)
	else:
		flash(games_list)
		return render_template('index.html',games=0,username=username,usertype=usertype)


@app.route('/search',  methods=['GET'])
def search():
	username = request.cookies.get("username")
	usertype = bool(request.cookies.get("usertype"))
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
	return render_template('index.html', games=game_list,username=username,usertype=usertype)


@app.route('/login.html')
def login():
	return render_template('login.html')

@app.route('/signup.html')
def signup():
	return render_template('signup.html')

@app.route('/about.html')
def about():
	username = request.cookies.get("username")
	usertype = bool(request.cookies.get("usertype"))
	return render_template("about.html",username=username,usertype=usertype)

@app.route('/contact.html')
def contact():
	username = request.cookies.get("username")
	usertype = bool(request.cookies.get("usertype"))
	return render_template('contact.html',username=username,usertype=usertype)

@app.route('/contact', methods=["POST"])
def contactDetails():
	name = request.form.get("name")
	email = request.form.get("email")
	subject = request.form.get("subject")
	message = request.form.get("message")
	contactDetails = {"name":name, "email":email, "subject":subject, "message":message}
	print("contactdetails", contactDetails)
	sendMail('famegamecorp2020@gmail.com', contactDetails)
	flash("Your query has been registered. We will contact you soon")
	return redirect("/contact.html")


@app.route('/register', methods=['POST'])
def register():
	#method to register user into database
	username = request.form.get('username')
	fname = request.form.get('fname')
	# lname = request.form.get('lname') #deleted
	phno = request.form.get('phno')
	emailid = request.form.get('emailid')
	password = request.form.get('password')
	usertype = request.form.get('usertype')
	location = request.form.get('location')
	city = request.form.get('city')
	state = request.form.get('state')

	print("usertype", usertype)
	if usertype=="Farmer":
		usertype = True

	else:
		usertype = False
	if username==None or fname==None or location == None or phno ==None or emailid==None or password==None:
		flash("incorrect input")
		return render_template('signup.html')
	else:
		user = {"username":username,"fname":fname, "phno":phno, "emailid":emailid, "password":password, "usertype":usertype, "location":location, "city":city,"state":state}
		print(user)
		registeration,error = db_query.registerUser(user)
		if registeration==500:
			flash("User not registered")
			return render_template('signup.html')
		elif registeration==200:
			resp = make_response(redirect('/'))
			resp.set_cookie("username",username)
			resp.set_cookie("usertype", bytes(usertype))
			return resp

@app.route('/signin', methods=['POST'])
def signin():
	emailid = request.form.get('emailid')
	password = request.form.get('password')
	usertype = request.form.get('usertype')
	if emailid==None or password==None or usertype=='role':
		flash('invalid login credentials')
		return render_template('login.html')
	else:
		user = {'emailid':emailid, "password":password , 'usertype' : usertype}
		check_status, error = db_query.checkUser(user)
		print(user)
		if check_status==500:
			flash(error)
			return render_template('login.html')
		elif check_status==404:
			flash("invalid login credentials")
			return render_template('login.html')
		elif check_status==200:
			print(error[3], type(error))
			resp = make_response(redirect("/"))
			resp.set_cookie("username", error[0])
			resp.set_cookie("usertype", bytes(True if usertype=='Farmer' else False))
			return resp


@app.route('/game', methods=["GET","POST"])
def game():
	username = request.cookies.get("username")
	usertype = bool(request.cookies.get("usertype"))
	gameName = request.args.get("type")
	toShowUpdate = False

	game_desc_status, game_desc = db_query.searchGame(gameName)
	category_status , category = db_query.findGameCategory(gameName)
	isPurchasedStatus, isPurchased = db_query.purchase(username,gameName)

	print(game_desc)
	order_id=None
	if username == game_desc[0][10]:
		toShowUpdate = True
		
	else:
		if not isPurchased:
			order_amount = int(game_desc[0][4])*100
			order_currency = 'INR'
			
			order_id = client.order.create({'amount':order_amount, 'currency':order_currency})
			

	if game_desc_status==200:
		return render_template("photo-detail.html",game_desc = game_desc,username=username, category=category, purchase=isPurchased,usertype=usertype, order_id=order_id, update=toShowUpdate)
	else:
		return redirect("/")

@app.route('/logout')
def logout():
	resp = make_response(redirect('/'))
	resp.delete_cookie('username')
	return resp

@app.route("/forget")
def ResetPasswordPage():
	return render_template("reset.html")

@app.route('/reset',methods=['POST'])
def resetPassword():
	username = request.form.get("username")
	password = request.form.get("password")
	if (username==None or password==None):
		flash("invalid details")
		return redirect("/forget")
	else:
		user = {"username":username, "password":password}
		resetStatus, resetMessage = db_query.resetPassword(user)
		if resetStatus == 200:
			flash("Password Updated. Please Login Again")
			return render_template("reset.html")
		else:
			flash(resetMessage)
			return render_template("reset.html")

#needs to complete
@app.route("/payment/success/<game_name>/<order_id>/<price>/<curr_version>", methods=['GET'])
def paymentSuccess(game_name,order_id,price,curr_version):
	username = request.cookies.get("username")
	transaction = {'order_id':order_id,'price':price,'curr_version':curr_version,'username':username,
					'selling_date':datetime.date.today(),'game_name':game_name}
	transactionStatus, insertTransaction = db_query.insertTransaction(transaction)
	if transactionStatus==200:
		return redirect("/mygames")
	else:
		return redirect("/")

@app.route("/mygames")
def myGames():
	username = request.cookies.get("username")
	usertype = bool(request.cookies.get("usertype"))
	games_status, games_list = db_query.myGames(username)
	print(games_list)
	if games_status == 200:
		return render_template('mygames.html', games=games_list,username=username,usertype=usertype)
	else:
		flash("No Games purchased")
		return render_template('mygames.html',games=[],username=username,usertype=usertype)



@app.route("/addgame")
def addGame():
	username = request.cookies.get("username")
	usertype = bool(request.cookies.get("usertype"))
	return render_template("addgame.html",username=username,usertype=usertype)

@app.route("/addcrop/success", methods=['POST'])
def addCropSuccess():
	username = request.cookies.get("username")
	usertype = bool(request.cookies.get("usertype"))
	game = {'crop_name':request.form.get('crop_name'),
			'crop_type':request.form.get('crop_type'),
			'crop_region':request.form.get('crop_region'),
			'f_username':username,
			'crop_weight':request.form.get('crop_weight'),
			'crop_img': 'https://sc04.alicdn.com/kf/Uadb37e80f09f439e9af7951a0659eae2a.jpg'
			}
	gameInsertStatus, gameInsert = db_query.insertGame(game)
	if gameInsertStatus==200:
		flash("Your Game is added successfully")
		return render_template("addgame.html",username=username,usertype=usertype)
	else:
		flash("Game Not Added. Please Try Again")
		return render_template("addgame.html",username=username,usertype=usertype)


@app.route("/update/<game_name>", methods=['GET', 'POST'])
def updatePage(game_name):
	if request.method == 'POST':
		username = request.cookies.get("username")
		usertype = bool(request.cookies.get("usertype"))
		game = {'game_name':game_name, 'game_link':request.form.get('update_link'),
				'curr_version':request.form.get('update_version')}
		print(game)
		updateGameStatus, updateGame = db_query.updateGame(game)
		if updateGameStatus==200:
			for mail in updateGame:
				sendMail(mail[0])
			flash("Game is updated successfully")
			return render_template("update.html",username=username,usertype=usertype)
		else:
			flash("Game is not updated")
			return render_template("update.html",username=username,usertype=usertype)
	else:
		username = request.cookies.get("username")
		usertype = bool(request.cookies.get("usertype"))
		gameName = game_name
		print(gameName)
		return render_template("update.html",username=username,usertype=usertype, gameName=gameName)


#auditor login page rendering
@app.route("/auditor/login")
def auditor_login():
	return render_template('auditor_login.html')

#auditor login methods
@app.route("/auditor/signin", methods=['Post'])
def auditor_login_signin():
	emailid = request.form.get("emailid")
	password = request.form.get("password")
	status, error = db_query.AuditorLogin({'emailid':emailid,'password':password})
	if status==500:
		flash(error)
		return render_template('auditor_login.html')
	elif status==404:
		flash("invalid login credentials")
		return render_template('auditor_login.html')
	elif status==200:
		print(error[3], type(error))
		resp = make_response(redirect("/"))
		resp.set_cookie("username", error[0])
		# resp.set_cookie("usertype", bytes(True if usertype=='Farmer' else False))
		return resp



if __name__ == "__main__":
	app.run(debug=True)