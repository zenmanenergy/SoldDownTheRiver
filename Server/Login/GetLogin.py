from _Lib import Database
import uuid
import datetime

def get_login(Email, Password):
	if not Email or not Password:
		Email="-1"
	
	# Connect to the database
	cursor, connection = Database.ConnectToDatabase()

	# Construct the SQL query
	query = "SELECT * from users WHERE Email = %s and Password = %s"
	values = (Email, Password,)


	print(query % tuple(map(repr, values)))


	# Execute the query and get the results
	cursor.execute(query, values)
	result = cursor.fetchone()


	if not result:
		result=""
	else:
		print(result)
		query = "delete from usersessions where userId= %s "
		values = (result['UserId'],)
		cursor.execute(query, values)
		connection.commit()

		SessionId = "SES" + str(uuid.uuid4())
		query = "INSERT into usersessions(sessionId,userId,dateAdded) VALUES (%s, %s, %s)"
		values = (SessionId, result['UserId'], datetime.datetime.now(),)
		cursor.execute(query, values)
		
		connection.commit()
		result=SessionId
		
	# Close the database connection
	connection.close()
	
	# Return the result as a dictionary
	return '"' + result+'"'
