from _Lib import Database

def get_transactionHumans(TransactionId):
  

	# Connect to the database
	cursor, connection = Database.ConnectToDatabase()

	# Construct the SQL query
	query = "SELECT humans.*, transactionhumans.TransactionId,transactionhumans.RoleId,roles.Role,transactionhumans.notes as TransactionNotes from humans join transactionhumans on humans.HumanId=transactionhumans.HumanId join roles on roles.roleId=transactionhumans.roleId where transactionhumans.TransactionId=%s order by transactionhumans.roleId,Firstname, Lastname"
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
