from _Lib import Database

def get_family(HumanId):
	if not HumanId:
		HumanId = "-1"
	
	# Connect to the database
	cursor, connection = Database.ConnectToDatabase()

	# Construct the SQL query
	sql = f"""
		SELECT h2.*, fm2.left_value, fm2.right_value, h3.FirstName AS SpouseFirstName, h3.LastName AS SpouseLastName
		FROM familymembers AS fm1
		JOIN familymembers AS fm2
			ON fm1.FamilyId = fm2.FamilyId
		JOIN humans AS h2
			ON fm2.HumanId = h2.HumanId
		LEFT JOIN humans AS h3
			ON h2.spouseHumanId = h3.HumanId
		WHERE fm1.HumanId = '{HumanId}'
		ORDER BY fm2.left_value;
	"""

	# Print the full SQL query for debugging
	print(f"Executing SQL: {sql}")

	# Execute the query
	cursor.execute(sql)
	result = cursor.fetchall()  # Fetch all rows as a list of dictionaries

	# Close the database connection
	connection.close()

	# If no result, return an empty list (optional, but keeps consistency)
	return result if result else []
