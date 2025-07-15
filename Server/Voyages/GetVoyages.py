from _Lib import Database

def get_voyages():
	# Connect to the database
	cursor, connection = Database.ConnectToDatabase()

	# Construct the SQL query for voyages
	
	sql = f"SELECT voyages.VoyageId, voyages.Notes, voyages.StartDate, voyages.EndDate, ships.ShipName,"
	sql += f" startlocation.Address StartAddress, startlocation.City StartCity, startlocation.State StartState, endlocation.Address EndAddress, endlocation.City EndCity, endlocation.State EndState,"
	sql += f" (select max(dateAdded) from history where history.KeyValue=voyages.VoyageId and history.TableName='voyages' and history.KeyName='VoyageId') LastModified "
	sql += f" from voyages join ships on voyages.shipId=ships.ShipId "
	sql += f" left join locations startlocation on startlocation.LocationId=voyages.StartLocationId"
	sql += f" left join locations endlocation on endlocation.LocationId=voyages.EndLocationId"


	print(sql)	
	# Execute the query and get the results
	cursor.execute(sql)
	result = cursor.fetchall()
	if not result:
		result = []

	# Close the database connection
	connection.close()

	# Return the result
	return result
