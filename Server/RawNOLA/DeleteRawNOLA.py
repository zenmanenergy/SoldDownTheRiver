from _Lib import Database

def delete_RawNOLA(SessionId, NOLA_ID):
	# Connect to the database
	cursor, connection = Database.ConnectToDatabase()

	# Delete query
	query = "DELETE FROM raw_nola WHERE NOLA_ID = %s"
	cursor.execute(query, (NOLA_ID,))
	connection.commit()
	connection.close()

	return {"status": "success"}
