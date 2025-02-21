from _Lib import Database

def get_transactions(TransactionId, TransactionDate):
	
	
	# Connect to the database
	cursor, connection = Database.ConnectToDatabase()

	# Construct the SQL query
	query = "SELECT *"
	query += " from transactions WHERE TransactionId like %s and TransactionDate like %s"
	values = (TransactionId + '%', TransactionDate + '%')


	#Business isn't there??? So fix this later probably



	# Execute the query and get the results
	cursor.execute(query, values)
	result = cursor.fetchall()
	if not result:
		result=[]
		
	# Close the database connection
	connection.close()
	
	# Return the result as a dictionary
	return result
