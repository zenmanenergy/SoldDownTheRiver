from Lib import Database

def get_voyages():
	# Connect to the database
	cursor, connection = Database.ConnectToDatabase()

	# Construct the SQL query for voyages
	
	sql = f"SELECT voyages.VoyageId, voyages.StartDate, voyages.EndDate, ships.ShipName,"
	sql += f" startLocation.City StartCity, startLocation.State StartState, EndLocation.City EndCity, EndLocation.State EndState,"
	sql += f" (select max(dateAdded) from History where History.KeyValue=voyages.VoyageId and History.TableName='Voyages' and History.KeyName='VoyageId') LastModified "
	sql += f" FROM voyages join ships on Voyages.shipId=ships.ShipId "
	sql += f" left join locations startLocation on startLocation.LocationId=voyages.StartLocationId"
	sql += f" left join locations endLocation on endLocation.LocationId=voyages.EndLocationId"

	# Execute the query and get the results
	cursor.execute(sql)
	result = cursor.fetchall()
	if not result:
		result = []

	# Close the database connection
	connection.close()

	# Return the result
	return result
