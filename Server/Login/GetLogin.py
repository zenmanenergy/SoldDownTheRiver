from _Lib import Database
import uuid
import datetime

def get_login(Email, Password):
	if not Email or not Password:
		Email = "-1"
	
	# Connect to the database
	cursor, connection = Database.ConnectToDatabase()

	# Construct the SQL query
	query = "SELECT * FROM users WHERE Email = %s AND Password = %s"
	values = (Email, Password,)

	print(query % tuple(map(repr, values)))

	# Execute the query and get the results
	cursor.execute(query, values)
	result = cursor.fetchone()

	if not result:
		result = ""
	else:
		print(result)
		# Delete existing sessions for the user
		query = "DELETE FROM usersessions WHERE UserId = %s"
		values = (result['UserId'],)
		cursor.execute(query, values)
		connection.commit()

		# Create a new session
		SessionId = "SES" + str(uuid.uuid4())
		query = "INSERT INTO usersessions(SessionId, UserId, DateAdded) VALUES (%s, %s, %s)"
		values = (SessionId, result['UserId'], datetime.datetime.now(),)
		cursor.execute(query, values)
		connection.commit()

		# Return both SessionId and UserType
		result = {
			"SessionId": SessionId,
			"UserType": result['UserType']
		}
	
	# Close the database connection
	connection.close()
	
	# Return the result as a JSON string
	return '{"SessionId": "' + result["SessionId"] + '", "UserType": "' + result["UserType"] + '"}' if result else '""'
