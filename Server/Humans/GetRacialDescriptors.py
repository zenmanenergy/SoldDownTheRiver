from _Lib.Database import ConnectToDatabase

def get_racial_descriptors():
	# Connect to the database
	cursor, connection = ConnectToDatabase()

	# Execute the query to fetch racial descriptors
	query = "SELECT DISTINCT RacialDescriptor FROM humans WHERE RacialDescriptor IS NOT NULL and RacialDescriptor <>'' ORDER BY RacialDescriptor"
	cursor.execute(query)
	result = [row['RacialDescriptor'] for row in cursor.fetchall()]  # Access by column name

	# Close the database connection
	connection.close()

	# Return the result
	return result
