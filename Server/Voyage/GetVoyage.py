from _Lib import Database

def get_Voyage(VoyageId):
	if not VoyageId:
		VoyageId = "-1"
	
	# Connect to the database
	cursor, connection = Database.ConnectToDatabase()

	# Construct the SQL query with LEFT JOINs for StartLocation, EndLocation, and CustomsLocation
	query = """
	SELECT v.*,
		sl.Name AS StartLocationName,
		sl.Address AS StartLocationAddress,
		sl.City AS StartLocationCity,
		sl.State AS StartLocationState,
		sl.Latitude AS StartLocationLatitude,
		sl.Longitude AS StartLocationLongitude,
		el.Name AS EndLocationName,
		el.Address AS EndLocationAddress,
		el.City AS EndLocationCity,
		el.State AS EndLocationState,
		el.Latitude AS EndLocationLatitude,
		el.Longitude AS EndLocationLongitude,
		cl.Name AS CustomsLocationName,
		cl.Address AS CustomsLocationAddress,
		cl.City AS CustomsLocationCity,
		cl.State AS CustomsLocationState,
		cl.Latitude AS CustomsLocationLatitude,
		cl.Longitude AS CustomsLocationLongitude
	FROM voyages v
	LEFT JOIN locations sl ON v.StartLocationId = sl.LocationId
	LEFT JOIN locations el ON v.EndLocationId = el.LocationId
	LEFT JOIN locations cl ON v.CustomsLocationId = cl.LocationId
	WHERE v.VoyageId = %s
	"""
	values = (VoyageId,)

	# Execute the query and get the results
	cursor.execute(query, values)
	result = cursor.fetchone()
	if not result:
		result = {}

	# Close the database connection
	connection.close()

	# Return the result as a dictionary
	return result
