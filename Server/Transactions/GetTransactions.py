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
		t.NotaryHumanId,
		t.Volume,
		t.URL,
		t.TotalPrice,
		t.LocationId,

		h1.FirstName AS FirstPartyFirstName,
		h1.MiddleName AS FirstPartyMiddleName,
		h1.LastName AS FirstPartyLastName,

		h2.FirstName AS SecondPartyFirstName,
		h2.MiddleName AS SecondPartyMiddleName,
		h2.LastName AS SecondPartyLastName,

		h3.FirstName AS NotaryFirstName,
		h3.MiddleName AS NotaryMiddleName,
		h3.LastName AS NotaryLastName,

		l.Address AS LocationAddress,
		l.City AS LocationCity,
		l.County AS LocationCounty,
		l.State_abbr AS LocationStateAbbr

	from transactions t
	LEFT JOIN parties p1 ON t.FirstPartyId = p1.PartyId
	LEFT JOIN partyhumans ph1 ON p1.PartyId = ph1.PartyId
	LEFT JOIN humans h1 ON ph1.HumanId = h1.HumanId

	LEFT JOIN parties p2 ON t.SecondPartyId = p2.PartyId
	LEFT JOIN partyhumans ph2 ON p2.PartyId = ph2.PartyId
	LEFT JOIN humans h2 ON ph2.HumanId = h2.HumanId

	LEFT JOIN humans h3 ON t.NotaryHumanId = h3.HumanId

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
