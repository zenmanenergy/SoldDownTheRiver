from _Lib import Database

def get_humanlocations(HumanId):
	if not HumanId:
		HumanId = "-1"
	
	# Connect to the database
	cursor, connection = Database.ConnectToDatabase()

	# Construct the SQL query
	query = """
	SELECT humanlocations.LocationId, humanlocations.date_circa, humanlocations.date_accuracy, humanlocations.locationType,
	       locations.Address, locations.City, locations.State_abbr, locations.Country, locations.Latitude, locations.Longitude
	FROM humanlocations
	JOIN locations ON locations.LocationId = humanlocations.LocationId
	WHERE humanlocations.HumanId = '{}'
	ORDER BY humanlocations.date_circa asc
	""".format(HumanId)
	
	# Print the SQL query with the actual HumanId value
	print(query)
	
	# Execute the query and get the results
	cursor.execute(query)
	result = cursor.fetchall()
	if not result:
		result = []
		
	# Close the database connection
	connection.close()
	
	# Return the result as a dictionary
	return result
