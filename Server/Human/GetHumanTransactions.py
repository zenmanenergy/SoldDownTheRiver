from _Lib import Database

def get_human_transactions(HumanId):
	if not HumanId:
		HumanId = "-1"
	
	# Connect to the database
	cursor, connection = Database.ConnectToDatabase()

	# Construct the SQL query
	query = """
		SELECT distinct
			t.TransactionId,
			t.date_circa,
			t.date_accuracy,
			t.TransactionType,
			n.Notary,
			s.Sellers,
			b.Buyers
		FROM transactions t
			JOIN transactionhumans ON t.TransactionId = transactionhumans.TransactionId AND transactionhumans.HumanId = '{}'
			LEFT JOIN (
				SELECT th1.TransactionId, GROUP_CONCAT(CONCAT_WS(COALESCE(h1.FirstName, th1.HumanId), ' ', COALESCE(h1.LastName, '')) SEPARATOR ', ') AS Notary
				FROM transactionhumans th1
				LEFT JOIN humans h1 ON th1.HumanId = h1.HumanId
				WHERE th1.RoleId = 'Notary'
				GROUP BY th1.TransactionId
			) n ON t.TransactionId = n.TransactionId
			LEFT JOIN (
				SELECT th2.TransactionId, GROUP_CONCAT(CONCAT_WS(COALESCE(h2.FirstName, th2.HumanId), ' ', COALESCE(h2.LastName, '')) SEPARATOR ', ') AS Sellers
				FROM transactionhumans th2
				LEFT JOIN humans h2 ON th2.HumanId = h2.HumanId
				WHERE th2.RoleId = 'Seller'
				GROUP BY th2.TransactionId
			) s ON t.TransactionId = s.TransactionId
			LEFT JOIN (
				SELECT th3.TransactionId, GROUP_CONCAT(CONCAT_WS(COALESCE(h3.FirstName, th3.HumanId), ' ', COALESCE(h3.LastName, '')) SEPARATOR ', ') AS Buyers
				FROM transactionhumans th3
				LEFT JOIN humans h3 ON th3.HumanId = h3.HumanId
				WHERE th3.RoleId = 'Buyer'
				GROUP BY th3.TransactionId
			) b ON t.TransactionId = b.TransactionId
		order by t.date_circa asc
	""".format( HumanId)
	
	# Print the SQL query with the actual HumanId value
	# print(query)
	
	# Execute the query and get the results
	cursor.execute(query)
	result = cursor.fetchall()
	if not result:
		result = []
		
	# Close the database connection
	connection.close()
	
	# Return the result as a dictionary
	return result
