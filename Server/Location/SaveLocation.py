import uuid
from Lib import Database

def save_location(LocationId, City, State, Country, Latitude, Longitude):
	# Connect to the database
	cursor, connection = Database.ConnectToDatabase()

	
	try:
		# Check if the LocationId is present
		if LocationId:
			# If the LocationId is present, update the existing location
			query = "UPDATE Locations SET City = %s, State = %s, Country = %s, Latitude = %s, Longitude = %s WHERE LocationId = %s"
			values = (City, State, Country, Latitude, Longitude, LocationId)
		else:
			# If the LocationId is not present, create a new location
			LocationId = "LOC"+str(uuid.uuid4())
			query = "INSERT INTO Locations (LocationId, City, State, Country, Latitude, Longitude) VALUES (%s, %s, %s, %s, %s, %s)"
			
			query +=" ON DUPLICATE KEY UPDATE City=values(City),State=values(State),Country=values(Country),Latitude=values(Latitude),Longitude=values(Longitude) "

			values = (LocationId, City, State, Country, float(Latitude or 0.0), float(Longitude or 0.0))

		response = {'success': True, 'LocationId': LocationId}
		# Execute the query and commit the changes
		cursor.execute(query, values)
		connection.commit()


	except pymysql.err.IntegrityError as e:
		# If a duplicate entry error occurred, modify the response
		response = {'success': False, 'error': str(e), 'LocationId': LocationId}

	finally:
		# Close the database connection
		connection.close()

	print(response)
	# Return the response
	return response