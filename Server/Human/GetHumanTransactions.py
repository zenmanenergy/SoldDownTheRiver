from _Lib import Database

def get_human_transactions(HumanId):
	if not HumanId:
		HumanId = "-1"
	
	# Connect to the database
	cursor, connection = Database.ConnectToDatabase()

	# Construct the SQL query
	query = """
		SELECT distinct
			transactions.TransactionId,
			transactions.date_circa,
			transactions.date_accuracy,
			transactions.TransactionType,
			transactions.Notes,
			transactions.Act,
			transactions.Page,
			transactions.Volume,
			transactions.URL,
			transactions.NeedsReview,
			transactions.Transcriber,
			transactions.NOLA_ID,
			transactions.Parsed_Notes,
			transactions.QuantityOfSlaves,
			transactions.TotalPrice,
			transactions.dataIssue,
			transactions.Issues,
			transactions.LocationId,
			transactions.processedNotes,
			transactions.isApproved,
			transactions.DataQuestions,
			transactionhumans.Notes AS TransactionHumanNotes,
			transactionhumans.ParsedNotes AS TransactionHumanParsedNotes,
			transactionhumans.Price AS TransactionHumanPrice,
			transactionhumans.originLocationId,
			transactionhumans.destinationLocationId
		FROM transactions
		
		LEFT JOIN transactionhumans ON transactions.TransactionId = transactionhumans.TransactionId
		WHERE fp.HumanId = '{}' OR sp.HumanId = '{}' OR transactionhumans.HumanId = '{}'
		order by date_circa asc
	""".format(HumanId, HumanId, HumanId, HumanId)
	
	# Print the SQL query with the actual HumanId value
	print(query)
	
	# Execute the query and get the results
	cursor.execute(query)
	result = cursor.fetchall()
	if not result:
		result = []
		
	# Close the database connection
	connection.close()
	
	# Return the result as a dictionary
	return result
