from _Lib import Database

def get_transactions():
	
	# Connect to the database
	cursor, connection = Database.ConnectToDatabase()

	# Construct the SQL query
	query = """
		SELECT 
		t.TransactionId,
		t.date_circa,
		t.date_accuracy,
		t.TransactionType,
		t.Act,
		t.Page,
		t.Volume,
		t.URL,
		t.TotalPrice,
		t.LocationId,

		

		l.Address AS LocationAddress,
		l.City AS LocationCity,
		l.County AS LocationCounty,
		l.State_abbr AS LocationStateAbbr

	from transactions t
	

	LEFT JOIN locations l ON t.LocationId = l.LocationId

	ORDER BY t.date_circa DESC

	"""

	values = ()

	print(query % values)  # Debugging SQL query before execution
	# Execute the query and get the results
	cursor.execute(query, values)
	result = cursor.fetchall()
	if not result:
		result = []

	# Close the database connection
	connection.close()

	# Return the result as a list of dictionaries
	return result
