from _Lib import Database

def get_notary_humans():
  

	# Connect to the database
	cursor, connection = Database.ConnectToDatabase()

	# Construct the SQL query
	query = "SELECT humans.* from humans join humanroles on humans.HumanId=humanroles.HumanId join Roles on humanroles.RoleId=Roles.RoleId where Roles.Role='Notary' order by Firstname, lastname"

	# Execute the query and get the results
	cursor.execute(query)
	result = cursor.fetchall()

	# Close the database connection
	connection.close()

	# Return the result as a dictionary
	return result
