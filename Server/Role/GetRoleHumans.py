from Lib import Database

def get_roleHumans(RoleId):
	# Connect to the database
	cursor, connection = Database.ConnectToDatabase()

	# Construct the SQL query
	query = "SELECT Humans.HumanId, Humans.FirstName, Humans.LastName , HumanRoles.RoleId,  (select max(dateAdded) from History where History.KeyValue=Humans.HumanId  and History.TableName='Humans' and History.KeyName='HumanId') LastModified"
	query += f" FROM Humans join HumanRoles on Humans.HumanId=HumanRoles.HumanId "
	query += f" where HumanRoles.RoleId = '{RoleId}'"
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
