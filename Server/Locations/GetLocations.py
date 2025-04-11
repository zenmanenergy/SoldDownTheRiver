from _Lib import Database

def get_locations():
	
	# Connect to the database
	cursor, connection = Database.ConnectToDatabase()

	# Construct the SQL query
	query = "SELECT distinct *"
	query +="   from locations where Address is not null order by Address"
	# query +=" limit 50"
	values = ()


	# Execute the query and get the results
	cursor.execute(query, values)
	result = cursor.fetchall()
	if not result:
		result=[]
		
	# Close the database connection
	connection.close()
	
	
	return result
