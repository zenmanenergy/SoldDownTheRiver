import uuid
from _Lib import Database
from datetime import datetime

def save_ship(ShipId, ShipName, BuildDate, Notes, ShipType, Size, HomePortLocationId):
	# Connect to the database
	cursor, connection = Database.ConnectToDatabase()

	# Handle BuildDate safely
	if not BuildDate or BuildDate.lower() == "null":
		BuildDate = None
	else:
		try:
			# Convert BuildDate to datetime object
			BuildDate = datetime.strptime(BuildDate, "%Y-%m-%d").isoformat()
		except ValueError:
			raise ValueError(f"Invalid date format for BuildDate: {BuildDate}")

	# Prepare SQL query
	if ShipId:
		# Update existing ship
		sql = """
			UPDATE ships 
			SET ShipName = %s, BuildDate = %s, Notes = %s, 
				ShipType = %s, Size = %s, HomePortLocationId = %s
			WHERE ShipId = %s
		"""
		values = (ShipName, BuildDate, Notes, ShipType, Size, HomePortLocationId, ShipId)
	else:
		# Create new ShipId
		ShipId = "SHP" + str(uuid.uuid4())

		# Insert new ship
		sql = """
			INSERT INTO ships (ShipId, ShipName, BuildDate, Notes, ShipType, Size, HomePortLocationId) 
			VALUES (%s, %s, %s, %s, %s, %s, %s)
		"""
		values = (ShipId, ShipName, BuildDate, Notes, ShipType, Size, HomePortLocationId)

	# Execute the SQL and commit changes
	print("Executing SQL:", sql, "with values:", values)  # Debugging output
	cursor.execute(sql, values)
	connection.commit()
	connection.close()

	# Return JSON response
	return {'success': True, 'ShipId': ShipId}
