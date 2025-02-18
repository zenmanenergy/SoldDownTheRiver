from _Lib import Database

def get_human(HumanId):
	if not HumanId:
		HumanId = "-1"
	
	# Connect to the database
	cursor, connection = Database.ConnectToDatabase()

	# Construct the SQL query
	sql = f"SELECT * FROM Humans WHERE HumanId = '{HumanId}'"

	# Print the full SQL query for debugging
	print(f"Executing SQL: {sql}")

	# Execute the query
	cursor.execute(sql)
	result = cursor.fetchone()  # Already returns a dictionary due to DictCursor

	# Close the database connection
	connection.close()

	# If no result, return an empty dictionary (optional, but keeps consistency)
	return result if result else {}
