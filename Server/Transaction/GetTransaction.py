from _Lib import Database

def get_transaction(transaction_id):
	if not transaction_id:
		transaction_id = "-1"

	# Connect to the database
	cursor, connection = Database.ConnectToDatabase()

	# Construct the SQL query
	query = f"""
		SELECT 
	t.TransactionId,
	t.date_circa,
	t.date_accuracy,
	t.TransactionType,
	t.TotalPrice,
	t.URL,
	t.LocationId,
	t.Notes,
	t.Transcriber,
	t.Act,
	t.Volume,
	t.Page,
	t.Act,
	t.isApproved,
	t.DataQuestions,


	COALESCE(
		JSON_ARRAYAGG(
			JSON_OBJECT(
				'FirstPartyId', h1.HumanId,
				'FirstPartyFirstName', h1.FirstName,
				'FirstPartyMiddleName', h1.MiddleName,
				'FirstPartyLastName', h1.LastName
			)
		), '[]'
	) AS FirstParties,

	h3.HumanId AS NotaryHumanId,
	h3.FirstName AS NotaryFirstName,
	h3.MiddleName AS NotaryMiddleName,
	h3.LastName AS NotaryLastName,

	l.Address AS LocationAddress,
	l.City AS LocationCity,
	l.County AS LocationCounty,
	l.State_abbr AS LocationStateAbbr,

	COALESCE(
		JSON_ARRAYAGG(
			JSON_OBJECT(
				'SecondPartyId', h2.HumanId,
				'SecondPartyFirstName', h2.FirstName,
				'SecondPartyMiddleName', h2.MiddleName,
				'SecondPartyLastName', h2.LastName
			)
		), '[]'
	) AS SecondParties

from transactions t
LEFT JOIN parties p1 ON t.FirstPartyId = p1.PartyId
LEFT JOIN partyhumans ph1 ON p1.PartyId = ph1.PartyId
LEFT JOIN humans h1 ON ph1.HumanId = h1.HumanId

LEFT JOIN parties p2 ON t.SecondPartyId = p2.PartyId
LEFT JOIN partyhumans ph2 ON p2.PartyId = ph2.PartyId
LEFT JOIN humans h2 ON ph2.HumanId = h2.HumanId

LEFT JOIN humans h3 ON t.NotaryHumanId = h3.HumanId

LEFT JOIN locations l ON t.LocationId = l.LocationId

WHERE t.TransactionId = '{transaction_id}'
GROUP BY t.TransactionId;

		"""


	# Execute the query and get the results
	cursor.execute(query)
	result = cursor.fetchone()
	if not result:
		result = []

	# Close the database connection
	connection.close()

	# Return the result as a dictionary
	return result
