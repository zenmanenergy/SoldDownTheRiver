from _Lib import Database
import json  # Import json module to format arrays manually

def get_transaction(transaction_id):
	if not transaction_id:
		transaction_id = "-1"

	# Connect to the database
	cursor, connection = Database.ConnectToDatabase()

	# Construct the SQL query using GROUP_CONCAT
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
			t.isApproved,
			t.DataQuestions,
			t.NOLA_ID,

			-- Buyers as a comma-separated JSON-like string
			COALESCE(
				GROUP_CONCAT(
					DISTINCT JSON_OBJECT(
						'BuyerId', h1.HumanId,
						'BuyerFirstName', h1.FirstName,
						'BuyerMiddleName', h1.MiddleName,
						'BuyerLastName', h1.LastName
					)
				SEPARATOR ','
				), ''
			) AS Buyers,

			-- Sellers as a comma-separated JSON-like string
			COALESCE(
				GROUP_CONCAT(
					DISTINCT JSON_OBJECT(
						'SellerId', h2.HumanId,
						'SellerFirstName', h2.FirstName,
						'SellerMiddleName', h2.MiddleName,
						'SellerLastName', h2.LastName
					)
				SEPARATOR ','
				), ''
			) AS Sellers,

			h3.HumanId AS NotaryHumanId,
			h3.FirstName AS NotaryFirstName,
			h3.MiddleName AS NotaryMiddleName,
			h3.LastName AS NotaryLastName,

			l.Address AS LocationAddress,
			l.City AS LocationCity,
			l.County AS LocationCounty,
			l.State_abbr AS LocationStateAbbr

		FROM transactions t

		LEFT JOIN transactionhumans th_buyer ON t.TransactionId = th_buyer.TransactionId AND th_buyer.RoleId = 'Buyer'
		LEFT JOIN humans h1 ON th_buyer.HumanId = h1.HumanId

		LEFT JOIN transactionhumans th_seller ON t.TransactionId = th_seller.TransactionId AND th_seller.RoleId = 'Seller'
		LEFT JOIN humans h2 ON th_seller.HumanId = h2.HumanId

		LEFT JOIN humans h3 ON t.NotaryHumanId = h3.HumanId
		LEFT JOIN locations l ON t.LocationId = l.LocationId

		WHERE t.TransactionId = '{transaction_id}'
		GROUP BY t.TransactionId;
	"""

	print(query)
	# Execute the query and get the results
	cursor.execute(query)
	result = cursor.fetchone()
	if not result:
		result = {}

	# Convert Buyers and Sellers from string to JSON array
	result["Buyers"] = json.loads(f"[{result['Buyers']}]" if result["Buyers"] else "[]")
	result["Sellers"] = json.loads(f"[{result['Sellers']}]" if result["Sellers"] else "[]")

	# Close the database connection
	connection.close()

	# Return the result as a dictionary
	return result
