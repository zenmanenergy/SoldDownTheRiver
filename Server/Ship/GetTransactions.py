from _Lib import Database

def get_Transactions(ShipId):
	
	# Connect to the database
	cursor, connection = Database.ConnectToDatabase()

	# Construct the SQL query
	query = f"SELECT *"
	query +=f" from transactions "
	

	print(query)
	cursor.execute(query)
	result = cursor.fetchall()
	if not result:
		result=[]
		
	# Close the database connection
	connection.close()
	
	
	return result
