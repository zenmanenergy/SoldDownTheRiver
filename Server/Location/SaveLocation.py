import uuid
from Lib import Database

def save_location(LocationId, City, State, Country, Latitude, Longitude):
	# Connect to the database
	cursor, connection = Database.ConnectToDatabase()

	sql=""
	# Check if the LocationId is present
	if LocationId:
		# If the LocationId is present, update the existing location
		sql = f"UPDATE Locations SET City = '{City}', State = '{State}', Country = '{Country}', Latitude = '{float(Latitude or 0.0)}', Longitude = '{float(Longitude or 0.0)}' WHERE LocationId = '{LocationId}'"
		
	else:
		# If the LocationId is not present, create a new location
		LocationId = "LOC"+str(uuid.uuid4())
		sql =f"INSERT INTO Locations (LocationId, City, State, Country, Latitude, Longitude) VALUES ('{LocationId}', '{City}', '{State}', '{Country}', '{float(Latitude or 0.0)}', '{float(Longitude or 0.0)}')"
		
		sql +=" ON DUPLICATE KEY UPDATE City=values(City),State=values(State),Country=values(Country),Latitude=values(Latitude),Longitude=values(Longitude) "


	# Execute the sql and commit the changes
	cursor.execute(sql)
	connection.commit()
	connection.close()
	response = {'success': True, 'LocationId': LocationId}

	print(response)
	# Return the response
	return response