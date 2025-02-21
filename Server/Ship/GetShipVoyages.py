from _Lib import Database

def get_ShipVoyages(ShipId):
	if not ShipId:
		ShipId = "-1"

	# Connect to the database
	cursor, connection = Database.ConnectToDatabase()

	# Construct the SQL sql
	sql = f"SELECT voyages.VoyageId, voyages.StartDate, voyages.EndDate, ships.ShipName,"
	sql += f" startlocation.City StartCity, startlocation.State StartState, endlocation.City EndCity, endlocation.State EndState,"
	sql += f" (select max(dateAdded) from history where history.KeyValue=voyages.VoyageId and history.TableName='voyages' and history.KeyName='VoyageId') LastModified "
	sql += f" from voyages join ships on voyages.shipId=ships.ShipId "
	sql += f" left join locations startlocation on startlocation.LocationId=voyages.StartlocationId"
	sql += f" left join locations endlocation on endlocation.LocationId=voyages.EndlocationId"
	sql += f" WHERE ships.ShipId = '{ShipId}'"




 




	print(sql)
	cursor.execute(sql)
	result = cursor.fetchall()
	if not result:
		result = []

	# Close the database connection
	connection.close()

	# Return the result as a dictionary
	return result
