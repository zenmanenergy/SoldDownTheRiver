from _Lib import Database

def get_human_second_party(HumanId):
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
			transactions.TransactionType
		FROM transactions
		JOIN partyhumans AS sp ON transactions.SecondPartyId = sp.PartyId
		LEFT JOIN partyhumans AS fp ON transactions.FirstPartyId = fp.PartyId
		LEFT JOIN humans AS fp_humans ON fp.HumanId = fp_humans.HumanId
		LEFT JOIN humans AS sp_humans ON sp.HumanId = sp_humans.HumanId
		
		WHERE sp.HumanId = '{}'
		order by date_circa asc
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
