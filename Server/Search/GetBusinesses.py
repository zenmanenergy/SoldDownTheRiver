from _Lib import Database

def get_businesses(BusinessName):
	if not BusinessName:
		BusinessName="-1"
	
	# Connect to the database
	cursor, connection = Database.ConnectToDatabase()

	# Construct the SQL query
	query = "SELECT * from businesses WHERE BusinessName like %s"
	values = (BusinessName + '%',)


	# Execute the query and get the results
	cursor.execute(query, values)
	result = cursor.fetchall()
	if not result:
		result=[]
		
	# Close the database connection
	connection.close()
	
	# Return the result as a dictionary
	return result
