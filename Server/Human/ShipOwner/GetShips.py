from Lib import Database

def get_ships(HumanId):
	if not HumanId:
		HumanId="-1"
	
	# Connect to the database
	cursor, connection = Database.ConnectToDatabase()

	# Construct the SQL query
	query = "SELECT * "
	query +=f" FROM ships  WHERE OwnerHumanId = '{HumanId}'"
	print(query)
	# Execute the query and get the results
	cursor.execute(query)
	result = cursor.fetchall()
	if not result:
		result=[]
		
	# Close the database connection
	connection.close()
	
	# Return the result as a dictionary
	return result
