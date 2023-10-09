from Lib import Database

def get_humans(Query):

	# Connect to the database
	cursor, connection = Database.ConnectToDatabase()

	# Construct the SQL query
	query = f"SELECT *, (select max(dateAdded) from History where History.KeyValue=Humans.HumanId and History.TableName='Humans' and History.KeyName='HumanId') LastModified"
	query +=f" FROM Humans "
	query +=f" where 1=1 "
	if Query:
		query +=f" and FirstName='{Query}'"
	
	query += f" order by LastName, FirstName"
	

	cursor.execute(query)
	result = cursor.fetchall()
	if not result:
		result=[]
		
	# Close the database connection
	connection.close()

	# Return the result as a dictionary
	return result