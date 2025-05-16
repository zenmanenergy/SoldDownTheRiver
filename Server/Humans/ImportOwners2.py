from _Lib.Database import ConnectToDatabase
import uuid

def import_owner2():
	# Connect to the database
	cursor, connection = ConnectToDatabase()

	# Execute the query to fetch Owner2
	query = "SELECT DISTINCT Owner2 FROM raw_manifest WHERE Owner2 <> '' AND Owner2 IS NOT NULL;"
	cursor.execute(query)
	result = cursor.fetchall()  # Access by column name

	# Process the result to split into FirstName, MiddleName, LastName
	processed_result = []
	for row in result:
		owner2_name = row['Owner2']
		parts = owner2_name.split(',', 1)  # Split into LastName and the rest
		last_name = parts[0].strip()
		first_and_middle = parts[1].strip() if len(parts) > 1 else ""
		first_name = first_and_middle.split(' ', 1)[0].strip() if first_and_middle else ""
		middle_name = first_and_middle.split(' ', 1)[1].strip() if ' ' in first_and_middle else ""

		# Search for an exact match in the humans table
		human_query = """
			SELECT HumanId 
			FROM humans 
			WHERE (FirstName = %s OR (FirstName IS NULL AND %s = '')) 
			  AND (MiddleName = %s OR (MiddleName IS NULL AND %s = ''))
			  AND (LastName = %s OR (LastName IS NULL AND %s = ''))
			LIMIT 1;
		"""
		cursor.execute(human_query, (first_name, first_name, middle_name, middle_name, last_name, last_name))
		human_match = cursor.fetchone()

		# If no match is found, insert a new row into the humans table
		if not human_match:
			human_id = "HUM" + str(uuid.uuid4())
			insert_query = """
				INSERT INTO humans (HumanId, FirstName, MiddleName, LastName, DateUpdated) 
				VALUES (%s, %s, %s, %s, NOW());
			"""
			cursor.execute(insert_query, (human_id, first_name, middle_name, last_name))
			connection.commit()
		else:
			human_id = human_match['HumanId']

		# Update the raw_manifest table to set Owner_humanId
		update_query = """
			UPDATE raw_manifest 
			SET Owner2_humanId = %s 
			WHERE Owner2 = %s;
		"""
		cursor.execute(update_query, (human_id, owner2_name))
		connection.commit()

		# Add the result with HumanId
		processed_result.append({
			"Owner2": owner2_name,
			"FirstName": first_name,
			"MiddleName": middle_name,
			"LastName": last_name,
			"HumanId": human_id
		})

	# Close the database connection
	connection.close()

	# Return the processed result
	return processed_result
