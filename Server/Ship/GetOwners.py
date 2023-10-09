from Lib import Database

def get_owners(ShipId):

	# Connect to the database
	cursor, connection = Database.ConnectToDatabase()

	# Construct the SQL query
	query = f"SELECT *"
	# , (select max(dateAdded) from History where History.KeyValue=Businesses.BusinessId and History.TableName='Businesses' and History.KeyName='BusinessId') LastModified"
	query +=f" FROM  humans join humanroles on humans.HumanId=humanroles.HumanId join roles on humanroles.RoleId=humanroles.RoleId"
	query += f" where roles.Role='Ship Owner'"
	print(query)

	# Execute the query and get the results
	cursor.execute(query)
	result = cursor.fetchall()
	if not result:
		result=[]
		
	# Close the database connection
	connection.close()

	# Return the result as a dictionary
	return result