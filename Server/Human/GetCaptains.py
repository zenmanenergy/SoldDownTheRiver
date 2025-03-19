from _Lib import Database

def get_captains(HumanId):
	if not HumanId:
		HumanId = "-1"
	
	# Connect to the database
	cursor, connection = Database.ConnectToDatabase()

	# Construct the SQL query
	query = """
		SELECT distinct
			voyages.VoyageId,
			voyages.ShipId,
			voyages.StartLocationId,
			voyages.EndLocationId,
			voyages.StartDate,
			voyages.EndDate,
			voyages.Notes,
			start_locations.Address AS StartAddress,
			end_locations.Address AS EndAddress
		FROM voyages
		LEFT JOIN locations AS start_locations ON voyages.StartLocationId = start_locations.LocationId
		LEFT JOIN locations AS end_locations ON voyages.EndLocationId = end_locations.LocationId
		WHERE voyages.CaptainHumanId = '{}'
		ORDER BY voyages.StartDate ASC
	""".format(HumanId)
	
	# Print the SQL query with the actual HumanId value
	print(query)
	
	# Execute the query and get the results
	cursor.execute(query)
	result = cursor.fetchall()
	if not result:
		result = []
		
	# Close the database connection
	connection.close()
	
	# Return the result as a dictionary
	return result
