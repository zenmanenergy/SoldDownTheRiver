import uuid
from Lib import Database

def save_ship(ShipId, ShipName,BuildDate, Notes, ShipType, Size, OwnerHumanId):
	# Connect to the database
	cursor, connection = Database.ConnectToDatabase()

	if len(BuildDate) == 0:
		BuildDate = None
	# Check if the ShipId is present
	if ShipId:
		# If the ShipId is present, update the existing ship
		query = "UPDATE Ships SET ShipName=%s, BuildDate = %s, Notes = %s, ShipType = %s, Size = %s, OwnerHumanId=%s WHERE ShipId = %s"
		values = (ShipName, BuildDate, Notes, ShipType, Size, OwnerHumanId, ShipId)
	else:
		# If the ShipId is not present, create a new ship
		ShipId = "SHP" + str(uuid.uuid4())
		query = "INSERT INTO Ships (ShipId, ShipName,BuildDate, Notes, ShipType, Size, OwnerHumanId) VALUES (%s, %s,  %s, %s, %s, %s, %s)"
		values = (ShipId, ShipName, BuildDate, Notes, ShipType, Size, OwnerHumanId)

	# Execute the query and commit the changes
	print(query, values)
	cursor.execute(query, values)
	connection.commit()

	# Close the database connection
	connection.close()

	# Return the ShipId as a JSON response
	return {'success': True, 'ShipId': ShipId}
