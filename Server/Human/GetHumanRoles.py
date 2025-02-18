from _Lib import Database

def get_humanRoles(HumanId):
	# Connect to the database
	cursor, connection = Database.ConnectToDatabase()

	# Construct the SQL query
	query = "SELECT roles.RoleId,roles.Role"
	query += f" FROM HumanRoles join roles on roles.RoleId=HumanRoles.RoleId"
	query += f" where HumanRoles.HumanId = '{HumanId}'"
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
