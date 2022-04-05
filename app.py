from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    redirect,
    flash,
    make_response,
    url_for,
)
from flask_bootstrap import Bootstrap
import db_query
from flask_cors import CORS
import json
import emails
import razorpay
import datetime
import base64
import cloudinary
import cloudinary.uploader
import cloudinary.api

app = Flask(__name__)
Bootstrap(app)
CORS(app)
app.secret_key = "super secret key"
client = razorpay.Client(auth=("rzp_test_UGcdp8a9kJX5GE", "gGX2vt9HpHbC7IbAmIKPsyIX"))

cloudinary.config(
    cloud_name="emandi",
    api_key="973971686227723",
    api_secret="jfZ522s3tUO58HAthloblmxvC-U",
)


@app.route("/hello")
def hello():
    return "Hello World"


@app.route("/")
@app.route("/index.html")
def index():
    username = request.cookies.get("username")
    usertype = request.cookies.get("usertype")
    crop_status, crop_list = db_query.searchCrop("%")
    if crop_status == 200:
        print(datetime.date(22, 3, 2))
        return render_template(
            "index.html",
            crops=crop_list,
            username=username,
            usertype=usertype,
            today=datetime.date.today(),
        )
    else:
        flash(crop_list)
        return render_template(
            "index.html",
            crops=[],
            username=username,
            usertype=usertype,
            today=datetime.date.today(),
        )


@app.route("/search", methods=["GET"])
def search():
    username = request.cookies.get("username")
    usertype = bool(request.cookies.get("usertype"))
    if not request.args.get("search"):
        flash("Please provide a correct vlaue")
        return redirect("/")
    game_status, game_list = db_query.searchGame(request.args.get("search"))
    if game_status == 500:
        return redirect("/")
    elif game_status == 404:
        flash(game_list)
        return redirect("index.html")
    elif game_list == None:
        return redirect("/")
    return render_template("index.html", games=game_list, username=username, usertype=usertype)


@app.route("/login.html")
def login():
    return render_template("login.html")


@app.route("/signup.html")
def signup():
    return render_template("signup.html")


@app.route("/about.html")
def about():
    username = request.cookies.get("username")
    usertype = bool(request.cookies.get("usertype"))
    return render_template("about.html", username=username, usertype=usertype)


@app.route("/contact.html")
def contact():
    username = request.cookies.get("username")
    usertype = bool(request.cookies.get("usertype"))
    return render_template("contact.html", username=username, usertype=usertype)


@app.route("/contact", methods=["POST"])
def contactDetails():
    name = request.form.get("name")
    email = request.form.get("email")
    subject = request.form.get("subject")
    message = request.form.get("message")
    contactDetails = {
        "name": name,
        "email": email,
        "subject": subject,
        "message": message,
    }
    print("contactdetails", contactDetails)
    emails.complaintMail("emandi0786@gmail.com", contactDetails)
    flash("Your query has been registered. We will contact you soon")
    return redirect("/contact.html")


@app.route("/register", methods=["POST"])
def register():
    # method to register user into database
    username = request.form.get("username")
    fname = request.form.get("fname")
    # lname = request.form.get('lname') #deleted
    phno = request.form.get("phno")
    emailid = request.form.get("emailid")
    password = request.form.get("password")
    usertype = request.form.get("usertype")
    location = request.form.get("location")
    city = request.form.get("city")
    state = request.form.get("state")
    if (
        username == None
        or fname == None
        or location == None
        or phno == None
        or emailid == None
        or password == None
    ):
        flash("incorrect input")
        return render_template("signup.html")
    else:
        user = {
            "username": username,
            "fname": fname,
            "phno": phno,
            "emailid": emailid,
            "password": password,
            "usertype": usertype,
            "location": location,
            "city": city,
            "state": state,
        }
        registeration, error = db_query.registerUser(user)
        if registeration == 500:
            flash("User not registered")
            return render_template("signup.html")
        elif registeration == 200:
            emails.registerMail(user["emailid"], user)
            resp = make_response(redirect("/"))
            resp.set_cookie("username", username)
            resp.set_cookie("usertype", usertype)
            return resp


@app.route("/signin", methods=["POST"])
def signin():
    emailid = request.form.get("emailid")
    password = request.form.get("password")
    usertype = request.form.get("usertype")
    if emailid == None or password == None or usertype == "role":
        flash("invalid login credentials")
        return render_template("login.html")
    else:
        user = {"emailid": emailid, "password": password, "usertype": usertype}
        check_status, error = db_query.checkUser(user)
        print(user)
        if check_status == 500:
            flash(error)
            return render_template("login.html")
        elif check_status == 404:
            flash("invalid login credentials")
            return render_template("login.html")
        elif check_status == 200:
            print(error[3], type(error))
            resp = make_response(redirect("/"))
            resp.set_cookie("username", error[0])
            resp.set_cookie("usertype", usertype)
            return resp


@app.route("/logout")
def logout():
    resp = make_response(redirect("/"))
    resp.delete_cookie("username")
    return resp


@app.route("/forget")
def ResetPasswordPage():
    return render_template("reset.html")


@app.route("/reset", methods=["POST"])
def resetPassword():
    username = request.form.get("username")
    password = request.form.get("password")
    if username == None or password == None:
        flash("invalid details")
        return redirect("/forget")
    else:
        user = {"username": username, "password": password}
        resetStatus, resetMessage = db_query.resetPassword(user)
        if resetStatus == 200:
            flash("Password Updated. Please Login Again")
            return render_template("reset.html")
        else:
            flash(resetMessage)
            return render_template("reset.html")


#################### AUDITOR LOGIN ####################
@app.route("/auditor/login")
def auditor_login():
    return render_template("auditor_login.html")


@app.route("/auditor/signin", methods=["Post"])
def auditor_login_signin():
    emailid = request.form.get("emailid")
    password = request.form.get("password")
    status, error = db_query.AuditorLogin({"emailid": emailid, "password": password})
    if status == 500:
        flash(error)
        return render_template("auditor_login.html")
    elif status == 404:
        flash("invalid login credentials")
        return render_template("auditor_login.html")
    elif status == 200:
        crop_status, crop_list = db_query.searchCrop("%")
        resp = make_response(
            render_template("auditor_index.html", username=error[0], crops=crop_list)
        )
        resp.set_cookie("username", error[0])
        return resp


################## CROP GRADING AUDITOR ##################
@app.route("/grade/crops", methods=["POST"])
def grade_crops():
    username = request.cookies.get("username")
    usertype = request.cookies.get("usertype")
    crop = {
        "crop_id": request.form.get("crop_id"),
        "crop_grade": request.form.get("grade"),
        "min_bid_price": 0.9 * float(request.form.get("min_bid_price")),
        "a_username": username,
        "crop_certificate": request.files.get("crop_certificate").read(),
    }
    grade_status, error = db_query.updateCropGrade(crop)
    if grade_status == 200:
        emails.gradeCropFarmerMail("emandi0786@gmail.com", {})
        crop_status, crop_list = db_query.searchCrop("%")
        return render_template("auditor_index.html", username=username, crops=crop_list)
    else:
        flash(error)
        return render_template("auditor_index.html", username=username, crops=[])


#################### AUDITOR CROPS PAGE ####################
@app.route("/crop/audited", methods=["GET", "POST"])
def crop_audited():
    username = request.cookies.get("username")
    usertype = request.cookies.get("usertype")
    cropID = request.args.get("type")
    crop_desc_status, crop_desc = db_query.searchCrop(cropID)
    if crop_desc_status == 200:
        return render_template(
            "auditor_crop_details_page.html", crop_desc=crop_desc, username=username
        )
    else:
        return redirect("/")


#################### CROPS MAIN PAGE ####################
@app.route("/crop", methods=["GET", "POST"])
def crop():
    username = request.cookies.get("username")
    usertype = request.cookies.get("usertype")
    cropID = request.args.get("type")

    crop_desc_status, crop_desc = db_query.searchCrop(cropID)
    query_status, bidder_name = db_query.finalBidderName(cropID)
    status_code, isPaid = db_query.is_Paid(username, cropID)  # return True or False

    order_id = None
    if not isPaid and bidder_name[0] == username:
        order_amount = int(crop_desc[0][5]) * 100
        order_currency = "INR"
        order_id = client.order.create({"amount": order_amount, "currency": order_currency})

    if status_code == 200:
        return render_template(
            "photo-detail.html",
            crop_desc=crop_desc,
            username=username,
            usertype=usertype,
            isPaid=isPaid,
            order_id=order_id,
            today=datetime.date.today(),
        )
    else:
        return redirect("/")


#################### MY CROPS ####################
@app.route("/mycrops")
def my_crops():
    username = request.cookies.get("username")
    usertype = request.cookies.get("usertype")
    crop_status, crop_list = db_query.myCrops(username, usertype)
    if crop_status == 200:
        return render_template(
            "mycrops.html", crops=crop_list, username=username, usertype=usertype
        )
    else:
        flash("No Crops to display")
        return render_template("mycrops.html", crops=[], username=username, usertype=usertype)


#################### ADD CROPS ####################
@app.route("/addcrop")
def addCrop():
    username = request.cookies.get("username")
    usertype = request.cookies.get("usertype")
    return render_template("addcrop.html", username=username, usertype=usertype)


@app.route("/addcrop/success", methods=["POST"])
def addCropSuccess():
    username = request.cookies.get("username")
    usertype = bool(request.cookies.get("usertype"))
    start = request.form.get("datepicker").split(" - ")[0]
    end = request.form.get("datepicker").split(" - ")[1]
    end_time = datetime.datetime.strptime(end, "%B %d, %Y") + datetime.timedelta(hours=22)

    crop = {
        "crop_name": request.form.get("crop_name"),
        "crop_type": request.form.get("crop_type"),
        "crop_region": request.form.get("crop_region"),
        "f_username": username,
        "crop_weight": request.form.get("crop_weight"),
        "crop_img": "https://sc04.alicdn.com/kf/Uadb37e80f09f439e9af7951a0659eae2a.jpg",
        "start_date": start,
        "end_date": end,
    }

    crop_img = request.files.get("crop_img")
    cloudinaryResult = cloudinary.uploader.upload(crop_img, public_id=crop["crop_name"])
    if "error" not in cloudinaryResult:
        crop["crop_img"] = cloudinaryResult["secure_url"]
    crop_insert_status, crop_id = db_query.insert_crop(crop)
    if crop_insert_status == 200:
        emails.farmerCropRegister("emandi0786@gmail.com", {})
        emails.auditorCropGrade("emandi0786@gmail.com", {})
        flash("Your Crop is added successfully")
        return redirect("/mycrops")
    else:
        flash("Crop Not Added. Please Try Again")
        return render_template("addcrop.html", username=username, usertype=usertype)


#################### BIDDING ####################
@app.route("/makebid", methods=["post"])
def make_bid():
    username = request.cookies.get("username")
    usertype = request.cookies.get("usertype")
    bid_price = request.form.get("bid_price")
    crop_id = request.form.get("crop_id")
    min_bid = request.form.get("min_bid")

    if float(bid_price) > float(min_bid):
        bid = {"username": username, "bid_price": bid_price, "crop_id": crop_id}
        bid_status, bid_error = db_query.insertBid(bid)
        if bid_status == 200:
            return redirect(url_for("crop", type=crop_id))
        else:
            flash(bid_error)
            return redirect(url_for("crop", type=crop_id))
    else:
        flash("Error! Please bid amount greater than Minimum Bidding Price")
        return redirect(url_for("crop", type=crop_id))


#################### PAYMENT ####################
@app.route("/payment/success/<crop_id>/<order_id>/<price>", methods=["GET"])
def paymentSuccess(crop_id, order_id, price):
    username = request.cookies.get("username")
    transaction = {
        "order_id": order_id,
        "price": price,
        "username": username,
        "selling_date": datetime.date.today(),
        "crop_id": crop_id,
    }
    transactionStatus, insertTransaction = db_query.insertTransaction(transaction)
    if transactionStatus == 200:
        emails.buyerWinBid("emandi0786@gmail.com", {})
        return redirect("/mycrops")
    else:
        return redirect("/")


#################### TEMP CLOSE ####################
@app.route("/closeauction", methods=["GET"])
def close_auction():
    crop_ids, err = db_query.get_active_auctions(datetime.date.today())
    closed = db_query.close(crop_ids)
    return render_template("/closed.html", closed=closed)


##################### MAIN #####################
if __name__ == "__main__":
    app.run(debug=True)
