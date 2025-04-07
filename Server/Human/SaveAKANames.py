import uuid
from _Lib import Database

def save_aka(AKAHumanId, HumanId, AKAFirstName, AKAMiddleName, AKALastName):
	# Connect to the database
	cursor, connection = Database.ConnectToDatabase()

	# Check if the HumanId is present
	if AKAHumanId:
		# If the HumanId is present, update the existing AKA record and set DateUpdated to NOW()
		query = "update humansaka SET AKAHumanId=%s, AKAFirstName=%s, AKAMiddleName=%s, AKALastName=%s, DateUpdated=NOW() WHERE AKAHumanId=%s"
		values = (HumanId, AKAFirstName, AKAMiddleName, AKALastName, AKAHumanId)
	else:
		# If the HumanId is not present, create a new AKA record and set DateUpdated to NOW()
		AKAHumanId = "AKA"+str(uuid.uuid4())
		query = "INSERT into humansaka (AKAHumanId, HumanId, AKAFirstName, AKAMiddleName, AKALastName, DateUpdated) VALUES (%s, %s, %s, %s, %s, NOW())"
		values = (AKAHumanId, HumanId, AKAFirstName, AKAMiddleName, AKALastName)

	# Execute the query and commit the changes
	cursor.execute(query, values)
	connection.commit()

	# Close the database connection
	connection.close()

	# Return the AKAHumanId
	return {'success': True, 'AKAHumanId': AKAHumanId}
