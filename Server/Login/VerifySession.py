from _Lib import Database
import uuid
import datetime

def verify_session(SessionId):
	if not SessionId:
		SessionId="-1"
	
	# Connect to the database
	cursor, connection = Database.ConnectToDatabase()

	# Construct the SQL query
	query = "SELECT * FROM UserSessions WHERE SessionId = %s"
	values = (SessionId,)


	print(query % tuple(map(repr, values)))


	# Execute the query and get the results
	cursor.execute(query, values)
	result = cursor.fetchone()
	# Close the database connection
	connection.close()
	
	
	if not result:
		return '""'
	else:
		return '"'+result["SessionId"]+'"'
	
	