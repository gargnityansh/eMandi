import psycopg2
import json

def searchGame(game_name):
	try:
		connection = psycopg2.connect(user = "postgres",
	                                  password = "***",
	                                  host = "127.0.0.1",
	                                  port = "5432",
	                                  database = "*****")
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
	                                  password = "***",
	                                  host = "127.0.0.1",
	                                  port = "5432",
	                                  database = "*****")
		cursor = connection.cursor()
		cursor.execute("INSERT INTO user_details (username,fname,lname,phno,emailid,password,\"isClient\") Values (%s,%s,%s,%s,%s,crypt(%s,gen_salt('bf')),%s)", (user['username'],user['fname'],user['lname'],str(user['phno']),user['emailid'],user['password'],user['usertype']))
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
		connection = psycopg2.connect(user = "postgres",
	                                  password = "***",
	                                  host = "127.0.0.1",
	                                  port = "5432",
	                                  database = "*****")
		cursor = connection.cursor()
		cursor.execute("SELECT username,emailid,password,\"isClient\" FROM user_details WHERE emailid=%s AND password = crypt(%s, password)", (user['emailid'],user['password']))
		record = cursor.fetchall()
		#closing database connection.
		if(connection):
			cursor.close()
			connection.close()
		if len(record) == 0:
			return 404, "empty"
		return 200, record[0]
	except (Exception, psycopg2.Error) as error :
		print ("Error while connecting to PostgreSQL", error)
		return 500,error

def findGameCategory(gameName):
	try:
		connection = psycopg2.connect(user = "postgres",
	                                  password = "***",
	                                  host = "127.0.0.1",
	                                  port = "5432",
	                                  database = "*****")
		cursor = connection.cursor()
		cursor.execute("SELECT cat_name FROM category WHERE gameid = (SELECT gameid FROM identty WHERE game_name=%s)",(gameName,))
		record = cursor.fetchall()
		#closing database connection.
		print(record)
		if(connection):
			cursor.close()
			connection.close()
		if len(record) == 0:
			return 404, "empty"
		return 200, record
	except (Exception, psycopg2.Error) as error :
		print ("Error in category", error)
		return 500,error

def resetPassword(resetdetails):
	try:
		connection = psycopg2.connect(user = "postgres",
	                                  password = "***",
	                                  host = "127.0.0.1",
	                                  port = "5432",
	                                  database = "*****")
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
		connection = psycopg2.connect(user = "postgres",
	                                  password = "***",
	                                  host = "127.0.0.1",
	                                  port = "5432",
	                                  database = "*****")
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
		connection = psycopg2.connect(user = "postgres",
	                                  password = "***",
	                                  host = "127.0.0.1",
	                                  port = "5432",
	                                  database = "*****")
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
		connection = psycopg2.connect(user = "postgres",
	                                  password = "***",
	                                  host = "127.0.0.1",
	                                  port = "5432",
	                                  database = "*****")
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
		connection = psycopg2.connect(user = "postgres",
	                                  password = "***",
	                                  host = "127.0.0.1",
	                                  port = "5432",
	                                  database = "*****")
		cursor = connection.cursor()

		cursor.execute("""INSERT INTO game(game_name, date_of_release, game_size, prod_studio, mrp, game_link, image, description, curr_version, username)
		VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",(game['game_name'],game['date_of_release'],game['game_size'],game['prod_studio'],game['mrp'],game['game_link'],game['image'],game['description'],game['curr_version'],game['username']))
		record = cursor.rowcount
		if(connection):
			connection.commit()
			cursor.close()
			connection.close()

		if record!=0:
			return 200,True
		return 404, False

	except (Exception, psycopg2.Error) as error :
		print ("Error in adding game", error)
		return 500,False

def insertCategory(category, gameName):
	try:
		connection = psycopg2.connect(user = "postgres",
	                                  password = "***",
	                                  host = "127.0.0.1",
	                                  port = "5432",
	                                  database = "*****")
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
		connection = psycopg2.connect(user = "postgres",
	                                  password = "***",
	                                  host = "127.0.0.1",
	                                  port = "5432",
	                                  database = "*****")
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
		connection = psycopg2.connect(user = "postgres",
	                                  password = "***",
	                                  host = "127.0.0.1",
	                                  port = "5432",
	                                  database = "*****")
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

if __name__ == "__main__":
	insertCategory(['Open World',"Action"],"Among Us")