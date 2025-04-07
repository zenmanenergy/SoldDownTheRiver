import uuid
from _Lib import Database

def save_HumanRole(HumanId,RoleId):
	# Connect to the database
	cursor, connection = Database.ConnectToDatabase()

	# Updated SQL to include DateUpdated and ON DUPLICATE KEY UPDATE
	sql = f"INSERT into humanroles (HumanId, RoleId, DateUpdated) VALUES ('{HumanId}','{RoleId}', NOW()) ON DUPLICATE KEY UPDATE RoleId=VALUES(RoleId), DateUpdated=NOW()"
	print(sql)
	# Execute the sql and commit the changes
	cursor.execute(sql)
	connection.commit()

	# Close the database connection
	connection.close()

	# Return the role as a JSON response
	return {'success': True, 'RoleId': RoleId}
