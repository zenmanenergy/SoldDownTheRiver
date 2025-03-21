from _Lib import Database

def get_families():
	# Connect to the database
	cursor, connection = Database.ConnectToDatabase()

	# Construct the SQL query
	sql = """
		SELECT FamilyId, FamilyName
		FROM families
		ORDER BY FamilyName;
	"""

	# Print the full SQL query for debugging
	print(f"Executing SQL: {sql}")

	# Execute the query
	cursor.execute(sql)
	result = cursor.fetchall()  # Fetch all rows as a list of dictionaries

	# Close the database connection
	connection.close()

	# Return the result
	return result if result else []
