from _Lib import Database
import uuid
import datetime

def verify_session(SessionId):
	if not SessionId:
		SessionId = "-1"
	
	# Connect to the database
	cursor, connection = Database.ConnectToDatabase()

	# Construct the SQL query
	query = """
		SELECT usersessions.SessionId, users.UserType 
		FROM usersessions 
		INNER JOIN users ON usersessions.UserId = users.UserId 
		WHERE usersessions.SessionId = %s
	"""
	values = (SessionId,)


	# Execute the query and get the results
	cursor.execute(query, values)
	result = cursor.fetchone()
	# Close the database connection
	connection.close()
	
	if not result:
		return '""'
	else:
		return '{"SessionId": "' + result["SessionId"] + '", "UserType": "' + result["UserType"] + '"}'

