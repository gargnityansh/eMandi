import psycopg2
import json
from datetime import datetime
import random
import string


def connection():
	connection = psycopg2.connect(user = "postgres",
	                 password = "admin123",
	                 host = "127.0.0.1",
	                 port = "5432",
	                 dbname = "mandi")
	return connection


#################### REGISTER USER #################### 
def registerUser(user):
	try:
		connect = connection()
		cursor = connect.cursor()
		if user['usertype']=='Farmer':
			cursor.execute("INSERT INTO \"Farmer\" (f_username,farmer_name,f_phone,f_email,f_password,farmer_loc,farmer_city,farmer_state) Values (%s,%s,%s,%s,crypt(%s,gen_salt('bf')),%s,%s,%s)", (user['username'],user['fname'],str(user['phno']),user['emailid'],user['password'],user['location'],user['city'],user['state']))
		else:
			cursor.execute("INSERT INTO \"Buyer\" (b_username,buyer_name,b_phone,b_email,b_password,buyer_loc,buyer_city,buyer_state) Values (%s,%s,%s,%s,crypt(%s,gen_salt('bf')),%s,%s,%s)", (user['username'],user['fname'],str(user['phno']),user['emailid'],user['password'],user['location'],user['city'],user['state']))
		print("is in final")
		#closing database connection.
		if(connect):
			connect.commit()
			cursor.close()
			connect.close()
			print("PostgreSQL connection is closed")
		
		return 200, "OK"
	except (Exception, psycopg2.Error) as error :
		print ("Error while connecting to PostgreSQL", error)
		return 500, error


#################### CHECK USER LOGIN #################### 
def checkUser(user):
	try:
		connect = connection()
		cursor = connect.cursor()
		if user['usertype']=='Farmer':
			cursor.execute("SELECT * FROM \"Farmer\" WHERE f_email=%s AND f_password = crypt(%s, f_password)", (user['emailid'],user['password']))
		else:
			cursor.execute("SELECT * FROM \"Buyer\" WHERE b_email=%s AND b_password = crypt(%s, b_password)", (user['emailid'],user['password']))
		record = cursor.fetchall()
		#closing database connection.
		if(connect):
			cursor.close()
			connect.close()
		if len(record) == 0:
			return 404, "empty"
		return 200, record[0]
	except (Exception, psycopg2.Error) as error :
		print ("Error while connecting to PostgreSQL", error)
		return 500,error


#################### RESET PASS #################### 
def resetPassword(resetdetails):
	try:
		connection = connection()
		cursor = connection.cursor()
		if resetdetails['password']==None:
			return 404, "password not found"
		cursor.execute("""UPDATE user_details SET password = crypt(%s,gen_salt('bf')) WHERE username=%s""",(resetdetails['password'],resetdetails['username']))
		number_of_rows_changed = cursor.rowcount
		if number_of_rows_changed==0:
			return 404,"user not found"
		if(connection):
			connection.commit()
			cursor.close()
			connection.close()
		return 200, "updated"
	except (Exception, psycopg2.Error) as error :
		print ("Error while connecting to PostgreSQL", error)
		return 500,error


#################### AUDITOR LOGIN #################### 
def AuditorLogin(user):
	try:
		connect = connection()
		cursor = connect.cursor()
		cursor.execute("SELECT * From public.\"Auditor\" WHERE a_email=%s and a_password=crypt(%s,a_password)", (user['emailid'],user['password']))
		record = cursor.fetchall()
		#closing database connection.
		if(connect):
			cursor.close()
			connect.close()
		if len(record) == 0:
			return 404, "empty"
		return 200, record[0]
	except (Exception, psycopg2.Error) as error :
		print ("Error while connecting to PostgreSQL", error)
		return 500,error


#################### INSERT CROP ####################
def insert_crop(crop):
	try:
		connect = connection()
		cursor = connect.cursor()
		crop_id = ''.join(random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase, k = 6))
		cursor.execute("""INSERT INTO "Crop"("crop_ID", crop_type, crop_region, crop_name, "upload_Date", f_username, crop_weight_kg, crop_img, start_date, end_date)
		VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",(crop_id, crop['crop_type'], crop['crop_region'], crop['crop_name'],datetime.today().strftime('%Y-%m-%d'), crop['f_username'], crop['crop_weight'], crop['crop_img'], crop['start_date'], crop['end_date']))
		record = cursor.rowcount
		if(connect):
			connect.commit()
			cursor.close()
			connect.close()
		if record!=0:
			return 200, crop_id
		return 404, 0

	except (Exception, psycopg2.Error) as error :
		print ("Error in adding crop", error)
		return 500, 0


############## Update Crop Quality in Crops table ##################
def updateCropGrade(crop):
	try:
		connect = connection()
		cursor = connect.cursor()
		cursor.execute("""UPDATE "Crop" SET crop_grade=%s, "grading_Date"=%s, final_bid_price=%s,min_bid_price=%s, auditor_un=%s,crop_certificate=%s	WHERE "crop_ID"=%s""",(crop['crop_grade'],datetime.now(),crop['min_bid_price'],crop['min_bid_price'],crop['a_username'],crop['crop_certificate'],crop['crop_id']))
		if(connect):
			connect.commit()
			cursor.close()
			connect.close()
		return 200, None
	except (Exception, psycopg2.Error) as error :
		print ("Error in update crop", error)
		return 500,error


##################### CLOSE AUCTION [MANUAL] ####################
def close(crop_id):
	try:
		connect = connection()
		cursor = connect.cursor()
		cursor.execute("SELECT b_username, \"bidAmount\" from \"Auction\" WHERE \"crop_ID\"=%s ORDER BY \"bidAmount\" desc limit 1", (crop_id,))
		record = cursor.fetchall()
		if len(record)==0:
			return None, "No Bidders Found"
		else:
			winner = record[0][0]
			cursor.execute("UPDATE \"Crop\" SET b_username=%s WHERE \"crop_ID\"=%s", (winner, crop_id))
		if(connect):
			cursor.close()
			connect.commit()
			connect.close()
		return winner, 'no error'
	except (Exception, psycopg2.Error) as error :
		print ("Error while connecting to PostgreSQL", error)
		return None, error


#################### CROP SEARCH FOR DISPLAY #################### 
def searchCrop(cropID='%'):
	try:
		connect = connection()
		cursor = connect.cursor()
		cursor.execute("SELECT \"crop_ID\", crop_type, crop_region, crop_name, \"upload_Date\", final_bid_price, crop_grade, \"grading_Date\", min_bid_price, f_username, auditor_un, b_username, crop_img, crop_weight_kg, start_date, end_date, encode(crop_certificate,'base64') FROM \"Crop\" WHERE \"crop_ID\" like %s",(cropID,))
		record = cursor.fetchall()

		#closing database connection.
		if(connect):
			cursor.close()
			connect.close()

		if len(record)!=0:
			return 200,record
		return 404, "No Such Crops"

	except (Exception, psycopg2.Error) as error :
		print ("Error in crop searching", error)
		return 500,error


#################### MY CROPS #################### 
def myCrops(uname, utype):
	try:
		connect = connection()
		cursor = connect.cursor()
		if utype=='Farmer':
			cursor.execute("SELECT * From \"Crop\" WHERE f_username=%s",(uname,))
		else:
			cursor.execute("SELECT * FROM \"Crop\" WHERE \"Crop\".\"crop_ID\" in (SELECT \"crop_ID\" from \"Auction\" where b_username=%s);",(uname,))
		
		record = cursor.fetchall()
		if(connect):
			cursor.close()
			connect.close()

		if len(record)!=0:
			return 200,record
		return 404, "No Such Crops"

	except (Exception, psycopg2.Error) as error :
		print ("Error while connecting to PostgreSQL", error)
		return 500,error


#################### INSERT BID #################### 
def insertBid(bid):
	try:
		connect = connection()
		cursor = connect.cursor()
		cursor.execute("INSERT INTO \"Auction\"( \"bidAmount\", b_username, bid_time, \"crop_ID\") VALUES (%s, %s, %s, %s)", (bid['bid_price'],bid['username'],datetime.now(), bid['crop_id']))
		cursor.execute("UPDATE \"Crop\" SET final_bid_price=%s WHERE \"crop_ID\"=%s", (bid['bid_price'], bid['crop_id']))
		if(connect):
			cursor.close()
			connect.commit()
			connect.close()
		return 200, 'no error'
	except (Exception, psycopg2.Error) as error :
		print ("Error while connecting to PostgreSQL", error)
		return 500,error


#################### FINAL BIDDER #################### 
def finalBidderName(crop_id):
	try:
		connect = connection()
		cursor = connect.cursor()

		cursor.execute("SELECT b_username FROM \"Crop\" WHERE \"crop_ID\"=%s",(crop_id,))
		record = cursor.fetchall()
		if(connect):
			cursor.close()
			connect.close()

		if len(record)!=0:
			return 200,record[0]
		return 404, "no user found"

	except (Exception, psycopg2.Error) as error :
		print ("Error in purchase", error)
		return 500,error


#################### TRANSACTION #################### 
def insertTransaction(transaction):
	try:
		connect = connection()
		cursor = connect.cursor()
		cursor.execute("""INSERT INTO "Transaction"("crop_ID", b_username, order_id, pay_date) VALUES (%s, %s, %s, %s);""",(transaction['crop_id'],transaction['username'],transaction['order_id'],transaction['selling_date']))
		record = cursor.rowcount			
		if record!=0:
			if(connect):
				connect.commit()
				cursor.close()
				connect.close()
				return 200,record

	except (Exception, psycopg2.Error) as error :
		print ("Error in transaction table", error)
		return 500,False


#################### PAYMENT CHECK #################### 
def is_Paid(uname, crop_id):
	try:
		connect = connection()
		cursor = connect.cursor()
		cursor.execute("SELECT * FROM \"Transaction\" WHERE \"crop_ID\" = %s", (crop_id,))
		record = cursor.fetchall()
		if(connect):
			cursor.close()
			connect.close()
		if len(record) == 0:
			return 200, False
		return 200, True
	except (Exception, psycopg2.Error) as error :
		print ("Error while connecting to PostgreSQL", error)
		return 500,error


#########################################################

def insertCategory(category, gameName):
	try:
		connection = connection()
		cursor = connection.cursor()
		
		cursor.execute("""SELECT gameid FROM identty WHERE game_name = %s""",(gameName,))
		gameid = cursor.fetchall()
		for cat in category:
			cursor.execute("""INSERT INTO category(gameid, cat_name)
				Values (%s, %s)""",(gameid[0][0], cat))

		if(connection):
			connection.commit()
			cursor.close()
			connection.close()
			return 200,True

	except (Exception, psycopg2.Error) as error :
		print ("Error in inserting category", error)
		return 500,False

def updateGame(game):
	try:
		connection = connection()
		cursor = connection.cursor()
		
		cursor.execute("""UPDATE game SET update_link = %s, curr_version=%s
						WHERE game_name = %s """,(game['game_link'],game['curr_version'],game['game_name']))
		record = cursor.rowcount			
		if record!=0:
			cursor.execute("""SELECT gameid FROM identty WHERE game_name = %s""",(game['game_name'],))
			gameid = cursor.fetchall()
			cursor.execute("""SELECT emailid FROM user_details
				WHERE username in (SELECT username FROM transactions 
				WHERE gameid=%s)""",(gameid[0][0],))
			record = cursor.fetchall()
			if(connection):
				connection.commit()
				cursor.close()
				connection.close()
				return 200,record

	except (Exception, psycopg2.Error) as error :
		print ("Error in updating game", error)
		return 500,False

def gameDetails(gameName):
	try:
		connection = connection()
		cursor = connection.cursor()

		cursor.execute("""SELECT mrp FROM game where game_name=%s""",(gameName,))
		record = cursor.fetchall()
		if(connection):
			cursor.close()
			connection.close()

		if len(record)!=0:
			return 200,record
		return 404, "No Such Games"

	except (Exception, psycopg2.Error) as error :
		print ("Error while connecting to PostgreSQL", error)
		return 500,error

def findGameCategory(gameName):
	try:
		connect = connection()
		cursor = connect.cursor()
		cursor.execute("SELECT cat_name FROM category WHERE gameid = (SELECT gameid FROM identty WHERE game_name=%s)",(gameName,))
		record = cursor.fetchall()
		#closing database connection.
		print(record)
		if(connect):
			cursor.close()
			connect.close()
		if len(record) == 0:
			return 404, "empty"
		return 200, record
	except (Exception, psycopg2.Error) as error :
		print ("Error in category", error)
		return 500,error


'''
################### TEMP AUDIT ###################
def add_price_crop(crop_id):
	try:
		connect = connection()
		cursor = connect.cursor()
		cursor.execute("UPDATE \"Crop\" SET final_bid_price=%s, min_bid_price=%s WHERE \"crop_ID\"=%s", (100, 100, crop_id))
		if(connect):
			cursor.close()
			connect.commit()
			connect.close()
		return 200, 'no error'
	except (Exception, psycopg2.Error) as error :
		print ("Error while connecting to PostgreSQL", error)
		return 500,error

'''