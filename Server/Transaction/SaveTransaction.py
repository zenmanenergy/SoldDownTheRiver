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
	
	# Update the isApproved status for the associated location
	if LocationId:
		location_query = "UPDATE locations SET isApproved=%s WHERE LocationId=%s"
		location_params = (1 if isApproved else 0, LocationId)
		print("Executing Location SQL:\n" + location_query + "\nWith params:\n" + str(location_params) + "\n")
		cursor.execute(location_query, location_params)
	
	# Update the isApproved status for humans associated with this transaction
	human_query = """UPDATE humans SET isApproved=%s 
					WHERE HumanId IN (
						SELECT HumanId FROM transactionhumans 
						WHERE TransactionId=%s
					)"""
	human_params = (1 if isApproved else 0, TransactionId)
	print("Executing Human SQL:\n" + human_query + "\nWith params:\n" + str(human_params) + "\n")
	cursor.execute(human_query, human_params)
	
	# Update locations based on humantimeline table for humans associated with this transaction
	timeline_location_query = """UPDATE locations 
								SET isApproved=%s 
								WHERE LocationId IN (
									SELECT t.LocationId FROM humantimeline t 
									JOIN humans h ON h.HumanId = t.HumanId 
									JOIN transactionhumans th ON th.HumanId = h.HumanId
									WHERE th.TransactionId=%s
								)"""
	timeline_location_params = (1 if isApproved else 0, TransactionId)
	print("Executing Timeline Location SQL:\n" + timeline_location_query + "\nWith params:\n" + str(timeline_location_params) + "\n")
	cursor.execute(timeline_location_query, timeline_location_params)
	
	connection.commit()
	
	connection.close()

	# Return the TransactionId as a JSON response
	return {'success': True, 'TransactionId': TransactionId}
