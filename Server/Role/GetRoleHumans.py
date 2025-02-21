from _Lib import Database

def get_roleHumans(RoleId):
	# Connect to the database
	cursor, connection = Database.ConnectToDatabase()

	# Construct the SQL query
	query = "SELECT humans.HumanId, humans.FirstName, humans.LastName , humanroles.RoleId,  (select max(dateAdded) from history where history.KeyValue=humans.HumanId  and history.TableName='humans' and history.KeyName='HumanId') LastModified"
	query += f" from humans join humanroles on humans.HumanId=humanroles.HumanId "
	query += f" where humanroles.RoleId = '{RoleId}'"
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
