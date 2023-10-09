import uuid
from Lib import Database

def save_BusinessHuman(BusinessId, HumanId, RoleId):
	# Connect to the database
	cursor, connection = Database.ConnectToDatabase()


	query = "INSERT INTO BusinessHumans (BusinessId, HumanId, RoleId) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE RoleId = VALUES(RoleId)"
	values = (BusinessId, HumanId, RoleId)

	# Execute the query and commit the changes
	cursor.execute(query, values)
	connection.commit()

	# Close the database connection
	connection.close()

	# Return the BusinessId as a JSON response
	return {'success': True, 'BusinessId': BusinessId}