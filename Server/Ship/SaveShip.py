import uuid
from Lib import Database
from datetime import datetime

def save_ship(ShipId, ShipName,BuildDate, Notes, ShipType, Size, HomePortLocationId):
	# Connect to the database
	cursor, connection = Database.ConnectToDatabase()

	if not BuildDate or len(BuildDate)==0:
		BuildDate = "NULL"
	else:
		# Assuming the date string format is "YYYY-MM-DD"
		BuildDate = datetime.strptime(BuildDate, "%Y-%m-%d")
		BuildDate=f"'{BuildDate.isoformat()}'"
	
	sql=""
	if ShipId:
		# If the ShipId is present, update the existing ship
		sql = f"UPDATE Ships SET ShipName='{ShipName}', BuildDate = {BuildDate}, Notes = '{Notes}', ShipType = '{ShipType}', Size = '{Size}', HomePortLocationId='{HomePortLocationId}' WHERE ShipId = '{ShipId}'"
		
	else:
		# If the ShipId is not present, create a new ship
		ShipId = "SHP" + str(uuid.uuid4())
		sql = f"INSERT INTO Ships (ShipId, ShipName,BuildDate, Notes, ShipType, Size, HomePortLocationId) VALUES ('{ShipId}', '{ShipName}',  {BuildDate}, '{Notes}', '{ShipType}', '{Size}', '{HomePortLocationId}')"

	# Execute the sql and commit the changes
	print(sql)
	cursor.execute(sql)
	connection.commit()

	# Close the database connection
	connection.close()

	# Return the ShipId as a JSON response
	return {'success': True, 'ShipId': ShipId}
