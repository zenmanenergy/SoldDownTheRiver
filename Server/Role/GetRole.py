from Lib import Database

def get_role(RoleId):
	# Connect to the database
	cursor, connection = Database.ConnectToDatabase()

	# Construct the SQL query
	query = "SELECT *, (select max(dateAdded) from History where History.KeyValue=Roles.RoleId  and History.TableName='Roles' and History.KeyName='RoleId') LastModified"
	query +="   FROM Roles WHERE RoleId = %s"
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
