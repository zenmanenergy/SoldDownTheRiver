from Lib import Database

def get_Humans(TransactionId):
	
	# Connect to the database
	cursor, connection = Database.ConnectToDatabase()

	# Construct the SQL query
	query = "SELECT *, (select max(dateAdded) from History where History.KeyValue=Humans.HumanId and History.TableName='Humans' and History.KeyName='HumanId') LastModified"
	query +=" FROM Humans order by FirstName, LastName"
	values = ()


	# Execute the query and get the results
	cursor.execute(query, values)
	result = cursor.fetchall()
	if not result:
		result=[]
		
	# Close the database connection
	connection.close()
	
	# Return the result as a dictionary
	return result
