import uuid
from _Lib import Database

def save_Voyage(VoyageId, ShipId, CaptainHumanId,StartLocationId, EndLocationId, StartDate, EndDate, Notes):
	# Connect to the database
	cursor, connection = Database.ConnectToDatabase()

	if len(StartDate) == 0:
		StartDate = None
	if len(EndDate) == 0:
		EndDate = None
	# Check if the VoyageId is present
	if VoyageId:
		# If the VoyageId is present, update the existing Voyage
		query = "update voyages SET ShipId = %s, CaptainHumanId=%s, StartLocationId = %s, EndLocationId = %s, StartDate = %s, EndDate = %s, Notes = %s, DateUpdated = NOW() WHERE VoyageId = %s"
		values = (ShipId,CaptainHumanId, StartLocationId, EndLocationId, StartDate, EndDate, Notes, VoyageId)
	else:
		# If the VoyageId is not present, create a new Voyage
		VoyageId = "VYG" + str(uuid.uuid4())
		query = "INSERT into voyages (VoyageId, ShipId,CaptainHumanId, StartLocationId, EndLocationId, StartDate, EndDate, Notes, DateUpdated) VALUES (%s,%s, %s, %s, %s, %s, %s, %s, NOW())"
		values = (VoyageId, ShipId,CaptainHumanId, StartLocationId, EndLocationId, StartDate, EndDate, Notes)

	# Execute the query and commit the changes
	print(query, values)
	cursor.execute(query, values)
	connection.commit()

	# Close the database connection
	connection.close()

	# Return the VoyageId as a JSON response
	return {'success': True, 'VoyageId': VoyageId}
