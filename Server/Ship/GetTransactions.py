from _Lib import Database

def get_Transactions(ShipId):
	
	# Connect to the database
	cursor, connection = Database.ConnectToDatabase()

	# Construct the SQL query
	query = f"SELECT *, (select max(dateAdded) from History where History.KeyValue=Transactions.TransactionId  and History.TableName='Transactions' and History.KeyName='TransactionId') LastModified"
	query +=f" FROM Transactions "
	

	print(query)
	cursor.execute(query)
	result = cursor.fetchall()
	if not result:
		result=[]
		
	# Close the database connection
	connection.close()
	
	
	return result
