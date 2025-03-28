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
				NotaryHumanId = {f"'{NotaryHumanId}'" if NotaryHumanId else 'NULL'}, 
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
		Notes = Notes.replace("'", "''") if Notes is not None else None
		Transcriber = Transcriber.replace("'", "''") if Transcriber is not None else None
		URL = URL.replace("'", "''") if URL is not None else None
		DataQuestions = DataQuestions.replace("'", "''") if DataQuestions is not None else None

		query = f"""
			INSERT INTO transactions 
			(TransactionId, date_circa, date_accuracy, TransactionType, Notes, NotaryHumanId, URL, 
			TotalPrice, LocationId, Act, Page, Volume, Transcriber, isApproved, DataQuestions)
			VALUES (
				'{TransactionId}', 
				{f"'{date_circa}'" if date_circa is not None else 'NULL'}, 
				{f"'{date_accuracy}'" if date_accuracy is not None else 'NULL'}, 
				{f"'{TransactionType}'" if TransactionType is not None else 'NULL'}, 
				{f"'{Notes}'" if Notes is not None else 'NULL'}, 
				{f"'{NotaryHumanId}'" if NotaryHumanId else 'NULL'}, 
				{f"'{URL}'" if URL is not None else 'NULL'}, 
				{TotalPrice if TotalPrice is not None else 'NULL'}, 
				{f"'{LocationId}'" if LocationId is not None else 'NULL'}, 
				{f"'{Act}'" if Act is not None else 'NULL'}, 
				{Page if Page is not None else 'NULL'}, 
				{Volume if Volume is not None else 'NULL'}, 
				{f"'{Transcriber}'" if Transcriber is not None else 'NULL'}, 
				{1 if isApproved else 0}, 
				{f"'{DataQuestions}'" if DataQuestions is not None else 'NULL'}
			)
		"""







	# Print and execute the query
	print(f"Executing SQL:\n{query}\n")
	cursor.execute(query)
	connection.commit()
	# Handle FirstParties and SecondParties insertion into `parties`
	def insert_parties(party_list, which_party):
		if not party_list:
			return

		# Generate a single PartyId for the entire party
		PartyId = "PTY" + str(uuid.uuid4())
		party_query = f"""
			INSERT INTO parties (PartyId, WhichParty) 
			VALUES ('{PartyId}', '{which_party}')
			ON DUPLICATE KEY UPDATE WhichParty = VALUES(WhichParty)
		"""
		print(f"Executing SQL:\n{party_query}\n")
		cursor.execute(party_query)

		# Link all humans in the party to the single PartyId
		for party in party_list:
			HumanId = party.get("FirstPartyId") or party.get("SecondPartyId")
			if HumanId:
				party_human_query = f"""
					INSERT INTO partyhumans (PartyId, HumanId) 
					VALUES ('{PartyId}', '{HumanId}')
					ON DUPLICATE KEY UPDATE HumanId = VALUES(HumanId)
				"""
				print(f"Executing SQL:\n{party_human_query}\n")
				cursor.execute(party_human_query)

		# Update the PartyId in the transactions table
		party_column = "FirstPartyId" if which_party == "FirstParty" else "SecondPartyId"
		update_transaction_query = f"""
			UPDATE transactions
			SET {party_column} = '{PartyId}'
			WHERE TransactionId = '{TransactionId}'
		"""
		print(f"Executing SQL:\n{update_transaction_query}\n")
		cursor.execute(update_transaction_query)

	# Insert FirstParties and SecondParties
	insert_parties(FirstParties, "FirstParty")
	insert_parties(SecondParties, "SecondParty")

	# Commit again if there are parties involved
	connection.commit()

	# Close the database connection
	connection.close()

	# Return the TransactionId as a JSON response
	return {'success': True, 'TransactionId': TransactionId}
