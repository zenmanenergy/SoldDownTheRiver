from _Lib import Database

def get_transactionHumans(TransactionId):
  

	# Connect to the database
	cursor, connection = Database.ConnectToDatabase()

	# Construct the SQL query
	query = "SELECT humans.*, transactionhumans.*,transactionhumans.notes as TransactionNotes from humans join transactionhumans on humans.HumanId=transactionhumans.HumanId where transactionhumans.TransactionId=%s order by Firstname, Lastname"
	values = (TransactionId,)
	# Execute the query and get the results

	# print(query % values)
	cursor.execute(query, values)
	result = cursor.fetchall()
	if not result:
		result = []

	# Close the database connection
	connection.close()
	# Return the result as a dictionary
	return result
