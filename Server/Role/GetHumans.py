from Lib import Database

def get_Humans(RoleId,Query):

	# Connect to the database
	cursor, connection = Database.ConnectToDatabase()

	# Construct the SQL sql
	sql = f"SELECT humans.HumanId , humans.FirstName, humans.LastName "
	# , (select max(dateAdded) from History where History.KeyValue=Businesses.BusinessId and History.TableName='Businesses' and History.KeyName='BusinessId') LastModified"
	sql +=f" FROM  humans where humanId not in( "
	sql +=f" select HumanId from humanroles where roleId='{RoleId}'"
	sql +=" )"
	if len(Query):
		sql +=f" and 1=1 and ("
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