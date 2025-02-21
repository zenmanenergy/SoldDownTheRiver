from _Lib import Database

def get_role(RoleId):
	# Connect to the database
	cursor, connection = Database.ConnectToDatabase()

	# Construct the SQL query
	query = "SELECT *, (select max(dateAdded) from history where history.KeyValue=roles.RoleId  and history.TableName='roles' and history.KeyName='RoleId') LastModified"
	query +="   from roles WHERE RoleId = %s"
	values = (RoleId,)
	print(query%values)
	# Execute the query and get the results
	cursor.execute(query, values)
	result = cursor.fetchone()
	if not result:
		result = {}

	# Close the database connection
	connection.close()

	# Return the result as a dictionary
	return result
