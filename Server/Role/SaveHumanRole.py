import uuid
from Lib import Database

def save_HumanRole(HumanId,RoleId):
	# Connect to the database
	cursor, connection = Database.ConnectToDatabase()

	

	sql = f"INSERT INTO humanroles (HumanId,RoleId) VALUES ('{HumanId}','{RoleId}')"
	print(sql)
	# Execute the sql and commit the changes
	cursor.execute(sql)
	connection.commit()

	# Close the database connection
	connection.close()

	# Return the role as a JSON response
	return {'success': True, 'RoleId': RoleId}
