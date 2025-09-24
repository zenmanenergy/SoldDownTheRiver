from _Lib import Database

def get_transactions_by_location_id(location_id):
	
	# Connect to the database
	cursor, connection = Database.ConnectToDatabase()

	# Construct the SQL query with left joins for Seller and Buyer role aggregation
	query = f"""
		SELECT 
			t.TransactionId,
			t.date_circa,
			t.date_accuracy,
			t.TransactionType,
			t.URL,
			t.TotalPrice,
			t.LocationId,

			l.Address AS LocationAddress,
			l.City AS LocationCity,
			l.County AS LocationCounty,
			l.State_abbr AS LocationStateAbbr,
			n.Notary,
			s.Sellers,
			b.Buyers

		FROM transactions t

		LEFT JOIN locations l ON t.LocationId = l.LocationId
		LEFT JOIN (
			SELECT th1.TransactionId, GROUP_CONCAT(CONCAT_WS(' ', h1.FirstName, h1.LastName) SEPARATOR ', ') AS Notary
			FROM transactionhumans th1
			LEFT JOIN humans h1 ON th1.HumanId = h1.HumanId
			WHERE th1.RoleId = 'Notary'
			GROUP BY th1.TransactionId
		) n ON t.TransactionId = n.TransactionId
		LEFT JOIN (
			SELECT th2.TransactionId, GROUP_CONCAT(CONCAT_WS(' ', h2.FirstName, h2.LastName) SEPARATOR ', ') AS Sellers
			FROM transactionhumans th2
			LEFT JOIN humans h2 ON th2.HumanId = h2.HumanId
			WHERE th2.RoleId = 'Seller'
			GROUP BY th2.TransactionId
		) s ON t.TransactionId = s.TransactionId
		LEFT JOIN (
			SELECT th3.TransactionId, GROUP_CONCAT(CONCAT_WS(' ', h3.FirstName, h3.LastName) SEPARATOR ', ') AS Buyers
			FROM transactionhumans th3
			LEFT JOIN humans h3 ON th3.HumanId = h3.HumanId
			WHERE th3.RoleId = 'Buyer'
			GROUP BY th3.TransactionId
		) b ON t.TransactionId = b.TransactionId

		WHERE t.LocationId = '{location_id}'

		ORDER BY t.date_circa DESC
	"""

	# print(query)  # Debugging SQL query before execution
	# Execute the query and get the results
	cursor.execute(query)
	result = cursor.fetchall()
	if not result:
		result = []

	# Close the database connection
	connection.close()

	# Return the result as a list of dictionaries
	return result
