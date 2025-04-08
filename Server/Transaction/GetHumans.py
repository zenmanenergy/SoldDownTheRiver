from _Lib import Database

def get_Humans(LastFetchTime=None):
	# Connect to the database
	cursor, connection = Database.ConnectToDatabase()

	# Construct the SQL query
	query = """
		SELECT *
		FROM humans
	"""
	values = []

	# Add filtering by LastFetchTime if provided
	if LastFetchTime:
		query += " WHERE DateUpdated > %s"
		values.append(LastFetchTime)

	query += " ORDER BY FirstName, LastName"

	# Execute the query and get the results
	cursor.execute(query, values)
	result = cursor.fetchall()
	if not result:
		result = []
		
	# Close the database connection
	connection.close()
	
	# Return the result as a dictionary
	return result
