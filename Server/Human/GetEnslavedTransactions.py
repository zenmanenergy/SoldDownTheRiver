from _Lib import Database

def get_enslaved_transactions(HumanId):
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
			transactions.FirstPartyId,
			fp_humans.FirstName AS FirstPartyFirstName,
			fp_humans.LastName AS FirstPartyLastName,
			transactions.SecondPartyId,
			sp_humans.FirstName AS SecondPartyFirstName,
			sp_humans.LastName AS SecondPartyLastName,
			transactions.TransactionType,
			transactionhumans.Notes AS TransactionHumanNotes,
			transactionhumans.ParsedNotes AS TransactionHumanParsedNotes,
			transactionhumans.Price AS TransactionHumanPrice,
			transactionhumans.originLocationId,
			transactionhumans.destinationLocationId
		FROM transactions
		LEFT JOIN transactionhumans ON transactions.TransactionId = transactionhumans.TransactionId
		LEFT JOIN partyhumans AS fp_partyhumans ON transactions.FirstPartyId = fp_partyhumans.PartyId
		LEFT JOIN humans AS fp_humans ON fp_partyhumans.HumanId = fp_humans.HumanId
		LEFT JOIN partyhumans AS sp_partyhumans ON transactions.SecondPartyId = sp_partyhumans.PartyId
		LEFT JOIN humans AS sp_humans ON sp_partyhumans.HumanId = sp_humans.HumanId
		WHERE transactionhumans.HumanId = '{}'
		ORDER BY transactions.date_circa ASC
	""".format(HumanId)
	
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
