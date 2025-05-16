from _Lib import Database

def get_CollectorAgents():
	
	# Connect to the database
	cursor, connection = Database.ConnectToDatabase()

	# Construct the SQL query
	query = "SELECT distinct h.HumanId, h.FirstName, h.LastName"
	query +=" from humans h join voyagehumans vh on h.humanid=vh.collectoragent_humanid order by firstname,lastname"
	values = ()

	print(query)
	# Execute the query and get the results
	cursor.execute(query, values)
	result = cursor.fetchall()
	if not result:
		result = []
		
	# Close the database connection
	connection.close()
	
	# Return the result as a dictionary
	return result
