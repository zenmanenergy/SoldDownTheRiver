import uuid
import datetime
import json
from _Lib import Database

def save_transaction(TransactionId, date_circa, date_accuracy, TransactionType, NotaryHumanId, FirstParties, SecondParties,  LocationId, TotalPrice, URL, Notes, Act, Page, Volume, Transcriber, isApproved, DataQuestions):


	

	# Convert JSON strings to lists (if needed)
	def parse_json_list(value):
		if isinstance(value, str):
			try:
				return json.loads(value) if value else []
			except json.JSONDecodeError:
				raise ValueError(f"Invalid JSON format in {value}")
		return value if isinstance(value, list) else []

	FirstParties = parse_json_list(FirstParties)
	SecondParties = parse_json_list(SecondParties)

	# Connect to the database
	cursor, connection = Database.ConnectToDatabase()

	# Check if the TransactionId is present
	if TransactionId:
		query = f"""
			UPDATE transactions 
			SET date_circa = '{date_circa}', 
				date_accuracy = '{date_accuracy}', 
				TransactionType = '{TransactionType}', 
				Notes = '{Notes.replace("'", "''")}', 
				NotaryHumanId = '{NotaryHumanId}', 
				URL = '{URL.replace("'", "''")}', 
				TotalPrice = {TotalPrice if TotalPrice is not None else 'NULL'}, 
				LocationId = '{LocationId}', 
				Act = '{Act}', 
				Page = {Page if Page is not None else 'NULL'}, 
				Volume = {Volume if Volume is not None else 'NULL'}, 
				Transcriber = '{Transcriber.replace("'", "''")}', 
				isApproved = {1 if isApproved else 0}, 
				DataQuestions = '{DataQuestions.replace("'", "''")}'
			WHERE TransactionId = '{TransactionId}'
		"""
	else:
		# If TransactionId is not present, create a new transaction
		TransactionId = "TRN" + str(uuid.uuid4())
		TotalPrice = 'NULL' if not TotalPrice or str(TotalPrice).lower() == 'null' else float(TotalPrice)
		query = f"""
			INSERT INTO transactions 
			(TransactionId, date_circa, date_accuracy, TransactionType, Notes, NotaryHumanId, URL, 
			TotalPrice, LocationId, Act, Page, Volume, Transcriber, isApproved, DataQuestions)
			VALUES (
				'{TransactionId}', 
				'{date_circa}', 
				'{date_accuracy}', 
				'{TransactionType}', 
				'{Notes.replace("'", "''")}', 
				'{NotaryHumanId}', 
				'{URL.replace("'", "''")}', 
				{TotalPrice}, 
				'{LocationId}', 
				'{Act}', 
				{Page if Page is not None else 'NULL'}, 
				{Volume if Volume is not None else 'NULL'}, 
				'{Transcriber.replace("'", "''")}', 
				{1 if isApproved else 0}, 
				'{DataQuestions.replace("'", "''")}'
			)
		"""





	# Print and execute the query
	print(f"Executing SQL:\n{query}\n")
	cursor.execute(query)
	connection.commit()

	# Handle FirstParties and SecondParties insertion into `parties`
	def insert_parties(party_list, which_party):
		for party in party_list:
			PartyId = "PTY" + str(uuid.uuid4())  # Generate a unique PartyId
			party_query = f"""
				INSERT INTO parties (PartyId, WhichParty) 
				VALUES ('{PartyId}', '{which_party}')
				ON DUPLICATE KEY UPDATE WhichParty = VALUES(WhichParty)
			"""
			print(f"Executing SQL:\n{party_query}\n")
			cursor.execute(party_query)

			# Link humans to this party
			if isinstance(party, dict) and "Humans" in party:
				for human in party["Humans"]:
					HumanId = human.get("HumanId")
					if HumanId:
						party_human_query = f"""
							INSERT INTO partyhumans (PartyId, HumanId) 
							VALUES ('{PartyId}', '{HumanId}')
							ON DUPLICATE KEY UPDATE HumanId = VALUES(HumanId)
						"""
						print(f"Executing SQL:\n{party_human_query}\n")
						cursor.execute(party_human_query)

	# Insert FirstParties and SecondParties
	insert_parties(FirstParties, "FirstParty")
	insert_parties(SecondParties, "SecondParty")

	# Commit again if there are parties involved
	connection.commit()

	# Close the database connection
	connection.close()

	# Return the TransactionId as a JSON response
	return {'success': True, 'TransactionId': TransactionId}
