from Lib import Database

def get_owners(Query):

	# Connect to the database
	cursor, connection = Database.ConnectToDatabase()

	# Construct the SQL sql
	sql = f"SELECT humans.HumanId , humans.FirstName, humans.LastName "
	# , (select max(dateAdded) from History where History.KeyValue=Businesses.BusinessId and History.TableName='Businesses' and History.KeyName='BusinessId') LastModified"
	sql +=f" FROM  humans join humanroles on humans.HumanId=humanroles.HumanId and humanroles.RoleId='ShipOwner'"
	if len(Query):
		sql +=f" where 1=1 and ("
		sql +=f" humans.FirstName like '%{Query}%'"
		sql +=f" or humans.LastName like '%{Query}%'"
		sql +=f" )"
	print(sql)

	# Execute the sql and get the results
	cursor.execute(sql)
	result = cursor.fetchall()
	if not result:
		result=[]
		
	# Close the database connection
	connection.close()

	# Return the result as a dictionary
	return result