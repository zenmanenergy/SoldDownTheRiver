import uuid
from _Lib import Database

def save_location(LocationId, City, State, Country, Latitude, Longitude):
	# Connect to the database
	cursor, connection = Database.ConnectToDatabase()

	sql = ""
	# Convert Latitude & Longitude to float safely
	Latitude = float(Latitude) if Latitude else 0.0
	Longitude = float(Longitude) if Longitude else 0.0

	if LocationId:
		# Update existing location
		sql = f"""
		UPDATE locations 
		SET City = '{City}', 
			State = '{State}', 
			Country = '{Country}', 
			Latitude = {Latitude}, 
			Longitude = {Longitude}, 
			DateUpdated = NOW() 
		WHERE LocationId = '{LocationId}'
		"""
	else:
		# Create new LocationId
		LocationId = "LOC" + str(uuid.uuid4())

		# Insert new location
		sql = f"""
		INSERT INTO locations (LocationId, City, State, Country, Latitude, Longitude, DateUpdated)
		VALUES ('{LocationId}', '{City}', '{State}', '{Country}', {Latitude}, {Longitude}, NOW())
		ON DUPLICATE KEY UPDATE 
			City = VALUES(City), 
			State = VALUES(State), 
			Country = VALUES(Country), 
			Latitude = VALUES(Latitude), 
			Longitude = VALUES(Longitude), 
			DateUpdated = NOW()
		"""

	# Execute the query
	print("Executing SQL:", sql)  # Debugging output
	cursor.execute(sql)
	connection.commit()
	connection.close()

	response = {'success': True, 'LocationId': LocationId}
	print(response)
	return response
