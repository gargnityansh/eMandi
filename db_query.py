import psycopg2
import json

def searchGame(game_name):
	try:
		connection = psycopg2.connect(user = "postgres",
	                                  password = "Garg@9406608047",
	                                  host = "127.0.0.1",
	                                  port = "5432",
	                                  database = "game_selling_marketplace")
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
		print ("Error while connecting to PostgreSQL", error)
		return 500,error
	
		
#print(searchGame("%"))

def registerUser(user):
	try:
		connection = psycopg2.connect(user = "postgres",
	                                  password = "Garg@9406608047",
	                                  host = "127.0.0.1",
	                                  port = "5432",
	                                  database = "game_selling_marketplace")
		cursor = connection.cursor()
		cursor.execute("INSERT INTO user_details (username,fname,lname,phno,emailid,password,usertype) Values (%s,%s,%s,%s,%s,crypt(%s,gen_salt('bf')),%s)", (user['username'],user['fname'],user['lname'],str(user['phno']),user['emailid'],user['password'],user['usertype']))
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
	                                  password = "Garg@9406608047",
	                                  host = "127.0.0.1",
	                                  port = "5432",
	                                  database = "game_selling_marketplace")
		cursor = connection.cursor()
		cursor.execute("SELECT username,emailid,password FROM user_details WHERE emailid=%s AND password = crypt(%s, password)", (user['emailid'],user['password']))
		record = cursor.fetchall()
		#closing database connection.
		if(connection):
			cursor.close()
			connection.close()
		if len(record) == 0:
			return 404, "empty"
		return 200, record[0][0]
	except (Exception, psycopg2.Error) as error :
		print ("Error while connecting to PostgreSQL", error)
		return 500,error

def findGameCategory(gameName):
	try:
		connection = psycopg2.connect(user = "postgres",
	                                  password = "Garg@9406608047",
	                                  host = "127.0.0.1",
	                                  port = "5432",
	                                  database = "game_selling_marketplace")
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
		print ("Error while connecting to PostgreSQL", error)
		return 500,error