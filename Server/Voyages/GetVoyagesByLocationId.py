from _Lib import Database

def get_voyages_by_location_id(location_id):
	
	# Connect to the database
	cursor, connection = Database.ConnectToDatabase()

	# Construct the SQL query with left joins for voyage details
	query = f"""
		SELECT 
			v.VoyageId,
			v.StartDate,
			v.EndDate,
			v.StartLocationId,
			v.EndLocationId,
			v.ShipId,
			s.ShipName,
			
			startloc.City AS StartCity,
			startloc.State AS StartState,
			startloc.County AS StartCounty,
			startloc.Address AS StartAddress,
			
			endloc.City AS EndCity,
			endloc.State AS EndState,
			endloc.County AS EndCounty,
			endloc.Address AS EndAddress,
			
			captains.Captains,
			agents.Agents,
			traders.Traders,
			
			(SELECT MAX(dateAdded) 
			 FROM history 
			 WHERE history.KeyValue = v.VoyageId 
			   AND history.TableName = 'voyages' 
			   AND history.KeyName = 'VoyageId') AS LastModified

		FROM voyages v

		LEFT JOIN ships s ON v.ShipId = s.ShipId
		LEFT JOIN locations startloc ON v.StartLocationId = startloc.LocationId
		LEFT JOIN locations endloc ON v.EndLocationId = endloc.LocationId
		
		LEFT JOIN (
			SELECT vh1.VoyageId, GROUP_CONCAT(CONCAT_WS(' ', h1.FirstName, h1.LastName) SEPARATOR ', ') AS Captains
			FROM voyagehumans vh1
			LEFT JOIN humans h1 ON vh1.HumanId = h1.HumanId
			WHERE vh1.RoleId = 'Captain'
			GROUP BY vh1.VoyageId
		) captains ON v.VoyageId = captains.VoyageId
		
		LEFT JOIN (
			SELECT vh2.VoyageId, GROUP_CONCAT(CONCAT_WS(' ', h2.FirstName, h2.LastName) SEPARATOR ', ') AS Agents
			FROM voyagehumans vh2
			LEFT JOIN humans h2 ON vh2.HumanId = h2.HumanId
			WHERE vh2.RoleId LIKE '%Agent%'
			GROUP BY vh2.VoyageId
		) agents ON v.VoyageId = agents.VoyageId
		
		LEFT JOIN (
			SELECT vh3.VoyageId, GROUP_CONCAT(CONCAT_WS(' ', h3.FirstName, h3.LastName) SEPARATOR ', ') AS Traders
			FROM voyagehumans vh3
			LEFT JOIN humans h3 ON vh3.HumanId = h3.HumanId
			WHERE vh3.RoleId LIKE '%Trader%'
			GROUP BY vh3.VoyageId
		) traders ON v.VoyageId = traders.VoyageId

		WHERE v.StartLocationId = '{location_id}' OR v.EndLocationId = '{location_id}'

		ORDER BY v.StartDate DESC
	"""

	print(query)  # Debugging SQL query before execution
	# Execute the query and get the results
	cursor.execute(query)
	result = cursor.fetchall()
	if not result:
		result = []

	# Close the database connection
	connection.close()

	# Return the result as a list of dictionaries
	return result
