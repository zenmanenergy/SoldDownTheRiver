from _Lib import Database

def get_humanlocations(HumanId):
	if not HumanId:
		HumanId="-1"
	
	# Connect to the database
	cursor, connection = Database.ConnectToDatabase()

	# Construct the SQL query
	query = "SELECT * "
	query +=f" FROM humanlocations join locations on locations.LocationId=humanlocations.LocationId WHERE humanlocations.HumanId = '{HumanId}' order by DateCirca"
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
