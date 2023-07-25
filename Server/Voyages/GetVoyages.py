from Lib import Database

def get_voyages():
	# Connect to the database
	cursor, connection = Database.ConnectToDatabase()

	# Construct the SQL query for voyages
	query = "SELECT *, (SELECT MAX(dateAdded) FROM History WHERE History.KeyValue=Voyages.VoyageId AND History.TableName='Voyages' AND History.KeyName='VoyageId') AS LastModified"
	query += " FROM Voyages ORDER BY StartDate"

	# Execute the query and get the results
	cursor.execute(query)
	result = cursor.fetchall()
	if not result:
		result = []

	# Close the database connection
	connection.close()

	# Return the result
	return result
