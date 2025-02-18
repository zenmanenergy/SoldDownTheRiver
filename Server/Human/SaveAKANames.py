import uuid
from _Lib import Database

def save_aka(AKAHumanId, HumanId, AKAFirstName, AKAMiddleName, AKALastName):
	# Connect to the database
	cursor, connection = Database.ConnectToDatabase()

	# Check if the HumanId is present
	if AKAHumanId:
		# If the HumanId is present, update the existing AKA record
		query = "UPDATE HumansAKA SET AKAHumanId=%s, AKAFirstName=%s, AKAMiddleName=%s, AKALastName=%s WHERE AKAHumanId=%s"
		values = (HumanId, AKAFirstName, AKAMiddleName, AKALastName, AKAHumanId)
	else:
		# If the HumanId is not present, create a new AKA record
		AKAHumanId = "AKA"+str(uuid.uuid4())
		query = "INSERT INTO HumansAKA (AKAHumanId, HumanId, AKAFirstName, AKAMiddleName, AKALastName) VALUES (%s, %s, %s, %s, %s)"
		values = (AKAHumanId, HumanId, AKAFirstName, AKAMiddleName, AKALastName)

	# Execute the query and commit the changes
	cursor.execute(query, values)
	connection.commit()

	# Close the database connection
	connection.close()

	# Return the AKAHumanId
	return {'success': True, 'AKAHumanId': AKAHumanId}
