from _Lib import Database

def get_locations(City, State, Country):
	
	
	# Connect to the database
	cursor, connection = Database.ConnectToDatabase()

	# Construct the SQL query
	query = "SELECT *"
	query += " from locations WHERE City like %s and State like %s and Country like %s"
	values = (City + '%', State + '%', Country + '%')



	# Execute the query and get the results
	cursor.execute(query, values)
	result = cursor.fetchall()
	if not result:
		result=[]
		
	# Close the database connection
	connection.close()
	
	# Return the result as a dictionary
	return result
