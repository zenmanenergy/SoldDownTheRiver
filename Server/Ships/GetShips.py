from _Lib import Database

def get_ships():
	# Connect to the database
	cursor, connection = Database.ConnectToDatabase()

	# Construct the SQL query
	query = """
		SELECT ships.*,
			(select max(dateAdded) from history where history.KeyValue=ships.ShipId and history.TableName='ships' and history.KeyName='ShipId') LastModified,
			GROUP_CONCAT(DISTINCT CONCAT(h.FirstName, ' ', h.LastName) ORDER BY h.FirstName, h.LastName SEPARATOR ', ') AS Captains
		FROM ships
		LEFT JOIN voyages v ON ships.ShipId = v.ShipId
		LEFT JOIN voyagehumans vh ON v.VoyageId = vh.VoyageId AND vh.RoleId = 'Captain'
		LEFT JOIN humans h ON vh.HumanId = h.HumanId
		GROUP BY ships.ShipId
		ORDER BY ships.ShipType, ships.Size
	"""
	values = ()

	# Execute the query and get the results
	cursor.execute(query, values)
	result = cursor.fetchall()
	if not result:
		result = []

	# Close the database connection
	connection.close()

	# Return the result
	return result

def search_ships():
	# Connect to the database
	cursor, connection = Database.ConnectToDatabase()

	# Construct the SQL query
	query = """
		SELECT ships.*,
			(select max(dateAdded) from history where history.KeyValue=ships.ShipId and history.TableName='ships' and history.KeyName='ShipId') LastModified,
			GROUP_CONCAT(DISTINCT CONCAT(h.FirstName, ' ', h.LastName) ORDER BY h.FirstName, h.LastName SEPARATOR ', ') AS Captains
		FROM ships
		LEFT JOIN voyages v ON ships.ShipId = v.ShipId
		LEFT JOIN voyagehumans vh ON v.VoyageId = vh.VoyageId AND vh.RoleId = 'Captain'
		LEFT JOIN humans h ON vh.HumanId = h.HumanId
		GROUP BY ships.ShipId
		ORDER BY ships.ShipType, ships.Size
	"""
	values = ()

	# Execute the query and get the results
	cursor.execute(query, values)
	result = cursor.fetchall()
	if not result:
		result = []

	# Close the database connection
	connection.close()

	# Return the result
	return result
