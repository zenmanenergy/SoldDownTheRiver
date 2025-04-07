import uuid
import datetime
import json
from _Lib import Database

def save_transaction(TransactionId, date_circa, date_accuracy, TransactionType, LocationId, TotalPrice, URL, Notes, Act, Page, Volume, Transcriber, isApproved, DataQuestions):

	# Convert JSON strings to lists (if needed)
	def parse_json_list(value):
		if isinstance(value, str):
			try:
				return json.loads(value) if value else []
			except json.JSONDecodeError:
				raise ValueError("Invalid JSON format in " + value)
		return value if isinstance(value, list) else []

	# Connect to the database
	cursor, connection = Database.ConnectToDatabase()
	
	# Preprocess TotalPrice to avoid data truncation in the float column.
	if not TotalPrice or str(TotalPrice).strip() == "" or str(TotalPrice).lower() == "null":
		TotalPrice = None
	else:
		TotalPrice = float(TotalPrice)

	# Check if the TransactionId is present
	if TransactionId:
		# Build parameterized UPDATE query
		query = ("UPDATE transactions SET "
				"date_circa=%s, date_accuracy=%s, TransactionType=%s, Notes=%s, URL=%s, "
				"TotalPrice=%s, LocationId=%s, Act=%s, Page=%s, Volume=%s, Transcriber=%s, "
				"isApproved=%s, DataQuestions=%s, DateUpdated=NOW() "
				"WHERE TransactionId=%s")
		params = (
			date_circa, 
			date_accuracy, 
			TransactionType, 
			Notes, 
			URL, 
			TotalPrice, 
			LocationId, 
			Act, 
			Page, 
			Volume, 
			Transcriber, 
			1 if isApproved else 0, 
			DataQuestions,
			TransactionId
		)
	else:
		# Create a new TransactionId and build parameterized INSERT query
		TransactionId = "TRN" + str(uuid.uuid4())
		query = ("INSERT INTO transactions "
				"(TransactionId, date_circa, date_accuracy, TransactionType, Notes, URL, TotalPrice, "
				"LocationId, Act, Page, Volume, Transcriber, isApproved, DataQuestions, DateUpdated) "
				"VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())")
		params = (
			TransactionId,
			date_circa,
			date_accuracy,
			TransactionType,
			Notes,
			URL,
			TotalPrice,
			LocationId,
			Act,
			Page,
			Volume,
			Transcriber,
			1 if isApproved else 0,
			DataQuestions
		)

	# Print and execute the query
	print("Executing SQL:\n" + query + "\nWith params:\n" + str(params) + "\n")
	cursor.execute(query, params)
	connection.commit()
	
	connection.close()

	# Return the TransactionId as a JSON response
	return {'success': True, 'TransactionId': TransactionId}
