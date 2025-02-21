from _Lib import Database

def get_ships():
	# Connect to the database
	cursor, connection = Database.ConnectToDatabase()

	# Construct the SQL query
	query = "SELECT *, (select max(dateAdded) from history where history.KeyValue=ships.ShipId  and history.TableName='ships' and history.KeyName='ShipId') LastModified"
	query += "  from ships ORDER BY ShipType, Size"
	values = ()

	# Execute the query and get the results
	cursor.execute(query, values)
	result = cursor.fetchall()
	if not result:
		result = []

	# Close the database connection
	connection.close()

	# Return the result
	return result
