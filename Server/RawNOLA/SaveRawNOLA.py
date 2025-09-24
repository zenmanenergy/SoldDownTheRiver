import uuid
from _Lib import Database

def save_RawNOLA(SessionId, NOLA):
	# Connect to the database
	cursor, connection = Database.ConnectToDatabase()

	# Generate a new NOLA_ID if empty
	NOLA_ID = NOLA.get("NOLA_ID", "").strip()
	if not NOLA_ID:
		NOLA_ID = f"NOL{uuid.uuid4().hex}"  # Generate a unique ID

	# Check if NOLA_ID exists using an alias for COUNT(*)
	existing_query = "SELECT COUNT(*) as thecount FROM raw_nola WHERE NOLA_ID = %s"
	cursor.execute(existing_query, (NOLA_ID,))
	existing_count = cursor.fetchone()
	print(f"DEBUG: existing_count = {existing_count}")  # Debugging output

	# Extract count safely
	if isinstance(existing_count, dict):
		existing_count = existing_count.get("thecount", 0)  # Extract from dict
	else:
		existing_count = existing_count[0] if existing_count else 0  # Extract from tuple

	if existing_count > 0:
		# Update existing record
		query = """
			UPDATE raw_nola
			SET FirstParty = %s, LocationFirstParty = %s, SecondParty = %s, LocationSecondParty = %s,
				TypeOfTransaction = %s, DateOfTransaction = %s, Act = %s, Page = %s,
				Notary = %s, Volume = %s, NameOfTranscriber = %s, ReferenceURL = %s
			WHERE NOLA_ID = %s
		"""
		values = (
			NOLA["FirstParty"], NOLA["LocationFirstParty"], NOLA["SecondParty"], NOLA["LocationSecondParty"],
			NOLA["TypeOfTransaction"], NOLA["DateOfTransaction"], NOLA["Act"], NOLA["Page"],
			NOLA["Notary"], NOLA["Volume"], NOLA["NameOfTranscriber"], NOLA["ReferenceURL"],
			NOLA_ID
		)
	else:
		# Insert new record
		query = """
			INSERT INTO raw_nola (NOLA_ID, FirstParty, LocationFirstParty, SecondParty, LocationSecondParty,
				TypeOfTransaction, DateOfTransaction, Act, Page, Notary, Volume,
				NameOfTranscriber, ReferenceURL)
			VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
		"""
		values = (
			NOLA_ID, NOLA["FirstParty"], NOLA["LocationFirstParty"], NOLA["SecondParty"], NOLA["LocationSecondParty"],
			NOLA["TypeOfTransaction"], NOLA["DateOfTransaction"], NOLA["Act"], NOLA["Page"],
			NOLA["Notary"], NOLA["Volume"], NOLA["NameOfTranscriber"], NOLA["ReferenceURL"]
		)

	cursor.execute(query, values)
	connection.commit()
	connection.close()
	
	return {"status": "success", "NOLA_ID": NOLA_ID}  # Return new NOLA_ID
