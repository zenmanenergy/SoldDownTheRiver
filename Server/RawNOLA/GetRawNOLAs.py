from _Lib import Database

def get_RawNOLAs(NOLA_ID_list=None):
	# Connect to the database
	cursor, connection = Database.ConnectToDatabase()

	print(tuple(NOLA_ID_list))
	# Construct SQL query
	if NOLA_ID_list:
		query = f"""
			SELECT 
				NOLA_ID, 
				FirstParty, 
				LocationFirstParty, 
				SecondParty, 
				LocationSecondParty, 
				TypeOfTransaction, 
				DateOfTransaction, 
				Act, 
				Page, 
				NotaryPublic, 
				Volume, 
				Notes,
				NameOfTranscriber, 
				ReferenceURL
			FROM raw_nola
			WHERE NOLA_ID IN ({', '.join(['%s'] * len(NOLA_ID_list))})
		"""
		cursor.execute(query, tuple(NOLA_ID_list))
	else:
		query = """
			SELECT 
				NOLA_ID, 
				FirstParty, 
				LocationFirstParty, 
				SecondParty, 
				LocationSecondParty, 
				TypeOfTransaction, 
				DateOfTransaction, 
				Act, 
				Page, 
				NotaryPublic, 
				Volume, 
				NameOfTranscriber, 
				ReferenceURL
			FROM raw_nola
		"""
		cursor.execute(query)

	results = cursor.fetchall()

	# Close connection
	connection.close()

	return results
