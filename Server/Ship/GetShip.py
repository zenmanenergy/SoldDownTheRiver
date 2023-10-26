from Lib import Database

def get_ship(ShipId):
	if not ShipId:
		ShipId = "-1"

	# Connect to the database
	cursor, connection = Database.ConnectToDatabase()

	# Construct the SQL query
	query = "SELECT *, (select max(dateAdded) from History where History.KeyValue=Ships.ShipId and History.TableName='Ships' and History.KeyName='ShipId') LastModified"
	query += f" FROM ships left join humans on ships.OwnerHumanId=humans.humanId WHERE ShipId = '{ShipId}'"
	
	# Execute the query and get the results
	cursor.execute(query)
	result = cursor.fetchone()
	ic(result)
	if not result:
		result = {}

	# Close the database connection
	connection.close()

	# Return the result as a dictionary
	return result
