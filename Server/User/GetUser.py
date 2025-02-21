from _Lib import Database

def get_user(UserId):
	if not UserId:
		UserId = "-1"
	
	# Connect to the database
	cursor, connection = Database.ConnectToDatabase()

	# Construct the SQL query
	query = "SELECT *, (select max(dateAdded) from history where history.KeyValue=users.UserId  and history.TableName='users' and history.KeyName='UserId') LastModified"
	query +=" from users WHERE UserId = %s"
	values = (UserId,)

	# Execute the query and get the results
	cursor.execute(query, values)
	result = cursor.fetchone()
	if not result:
		result = {}

	# Close the database connection
	connection.close()

	# Return the result as a dictionary
	return result
