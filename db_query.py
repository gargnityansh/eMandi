import psycopg2
import json
from datetime import datetime
import random
import string


def connection():
	connection = psycopg2.connect(user = "postgres",
	                 password = "Garg@9406608047",
	                 host = "127.0.0.1",
	                 port = "5432",
	                 dbname = "eMandi")
	return connection


def searchGame(game_name):
	try:
		connection = psycopg2.connect(user = "nkhtxgbfglczah",
	                                  password = "6136a94cd1f1c0faae5fb3380df7f70dc064f6ad7efaabc4e667b7055db847c3",
	                                  host = "ec2-34-239-33-57.compute-1.amazonaws.com",
	                                  port = "5432",
	                                  database = "deob53en4bmk8d")
		cursor = connection.cursor()
		# Print PostgreSQL Connection properties
		#print ( connection.get_dsn_parameters(),"\n")
		# Print PostgreSQL version
		cursor.execute("SELECT * FROM game where game_name like '%"+ game_name + "%'")
		record = cursor.fetchall()
		#print (record,"\n")
		#closing database connection.
		if(connection):
			cursor.close()
			connection.close()

		if len(record)!=0:
			return 200,record
		return 404, "No Such Games"

	except (Exception, psycopg2.Error) as error :
		print ("Error in game searching", error)
		return 500,error
	
		
#print(searchGame("%"))

def registerUser(user):
	try:
		connection = psycopg2.connect(user = "postgres",
	                                  password = "Garg@9406608047",
	                                  host = "127.0.0.1",
	                                  port = "5432",
	                                  dbname = "eMandi")
		cursor = connection.cursor()
		if user['usertype']=='Farmer':
			cursor.execute("INSERT INTO \"Farmer\" (f_username,farmer_name,f_phone,f_email,f_password,farmer_loc,farmer_city,farmer_state) Values (%s,%s,%s,%s,crypt(%s,gen_salt('bf')),%s,%s,%s)", (user['username'],user['fname'],str(user['phno']),user['emailid'],user['password'],user['location'],user['city'],user['state']))
		else:
			cursor.execute("INSERT INTO \"Buyer\" (b_username,buyer_name,b_phone,b_email,b_password,buyer_loc,buyer_city,buyer_state) Values (%s,%s,%s,%s,crypt(%s,gen_salt('bf')),%s,%s,%s)", (user['username'],user['fname'],str(user['phno']),user['emailid'],user['password'],user['location'],user['city'],user['state']))
		print("is in final")
		#closing database connection.
		if(connection):
			connection.commit()
			cursor.close()
			connection.close()
			print("PostgreSQL connection is closed")
		
		return 200, "OK"
	except (Exception, psycopg2.Error) as error :
		print ("Error while connecting to PostgreSQL", error)
		return 500,error

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


def myGames(userdetails):
	try:
		connection = connection()
		cursor = connection.cursor()

		cursor.execute("""SELECT * from game where game_name in 
						(SELECT game_name from identty where gameid in (
				Select gameid from transactions where username = %s ))""",(userdetails,))
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

def purchase(username, gameName):
	try:
		connection = connection()
		cursor = connection.cursor()

		cursor.execute("""SELECT gameid, username FROM transactions 
			where gameid in (SELECT gameid FROM identty where game_name=%s)
			AND username = %s""",(gameName,username))
		record = cursor.fetchall()
		if(connection):
			cursor.close()
			connection.close()

		if len(record)!=0:
			return 200,True
		return 404, False

	except (Exception, psycopg2.Error) as error :
		print ("Error in purchase", error)
		return 500,False

def insertGame(game):
	try:
		connect = connection()
		cursor = connect.cursor()
		crop_id = ''.join(random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase, k = 6))
		cursor.execute("""INSERT INTO "Crop"("crop_ID", crop_type, crop_region, crop_name, "upload_Date", f_username, crop_weight_kg, crop_img)
		VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",(crop_id,game['crop_type'],game['crop_region'],game['crop_name'],datetime.today().strftime('%Y-%m-%d'),game['f_username'],game['crop_weight'],game['crop_img']))
		record = cursor.rowcount
		if(connect):
			connect.commit()
			cursor.close()
			connect.close()
		if record!=0:
			return 200,True
		return 404, False

	except (Exception, psycopg2.Error) as error :
		print ("Error in adding game", error)
		return 500,False

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

def insertTransaction(transaction):
	try:
		connection = connection()
		cursor = connection.cursor()
		cursor.execute("""SELECT gameid FROM identty WHERE game_name = %s""",(transaction['game_name'],))
		gameid = cursor.fetchall()
		
		cursor.execute("""INSERT INTO transactions(gameid, username, selling_date, price, curr_version, order_id)
				VALUES (%s, %s, %s, %s, %s, %s);""",(gameid[0][0],transaction['username'],transaction['selling_date'],transaction['price'],transaction['curr_version'],transaction['order_id']))
		record = cursor.rowcount			
		if record!=0:
			if(connection):
				connection.commit()
				cursor.close()
				connection.close()
				return 200,record

	except (Exception, psycopg2.Error) as error :
		print ("Error in transaction table", error)
		return 500,False


#auditor login method
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








if __name__ == "__main__":
	insertCategory(['Open World',"Action"],"Among Us")