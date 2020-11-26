import psycopg2

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
		cursor.execute("SELECT game_name FROM identty where game_name like '%"+ game_name + "%'")
		record = cursor.fetchall()
		print (record,"\n")

	except (Exception, psycopg2.Error) as error :
		print ("Error while connecting to PostgreSQL", error)
	finally:
		print("is in final")
		#closing database connection.
		if(connection):
			cursor.close()
			connection.close()
			print("PostgreSQL connection is closed")
		return record

#searchGame("l")
