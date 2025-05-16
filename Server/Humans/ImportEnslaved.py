from _Lib.Database import ConnectToDatabase
import uuid
from datetime import datetime

def import_enslaved():
	# Connect to the database
	cursor, connection = ConnectToDatabase()

	# Fetch rows from raw_manifest where enslaved_humanId is null
	query = """
		SELECT DISTINCT manifest_id, LastName, FirstNameMiddleName, shipvoyageid, norfolk_date, age, height_feet, height_inches, sex, color
		FROM raw_manifest 
		WHERE enslaved_humanid IS NULL
		LIMIT 5000
	"""
	unprocessed_result = []
	cursor.execute(query)
	result = cursor.fetchall()

	# Process each row
	for row in result:
		manifest_id = row["manifest_id"]
		last_name = row["LastName"]
		first_and_middle = row["FirstNameMiddleName"]
		norfolk_date = row["norfolk_date"]
		age = row["age"]
		height_feet = row["height_feet"]
		height_inches = row["height_inches"]
		sex = row["sex"]
		color = row["color"]

		# Parse FirstName and MiddleName
		if first_and_middle:
			parts = first_and_middle.split(' ', 1)
			first_name = parts[0].strip() if len(parts) > 0 else None
			middle_name = parts[1].strip() if len(parts) > 1 else None
		else:
			first_name = None
			middle_name = None

		# Search for a matching human in the humans table
		human_query = """
			SELECT HumanId 
			FROM humans 
			WHERE (FirstName = %s OR (FirstName IS NULL AND %s IS NULL)) 
			AND (MiddleName = %s OR (MiddleName IS NULL AND %s IS NULL)) 
			AND (LastName = %s OR (LastName IS NULL AND %s IS NULL))
			LIMIT 1
		"""
		cursor.execute(human_query, (first_name, first_name, middle_name, middle_name, last_name, last_name))
		human_match = cursor.fetchone()

		# # If no match is found, create a new human
		# if not human_match:
		human_id = "HUM" + str(uuid.uuid4())
		age_string = age
		birth_date = None
		height_cm = None

		# Calculate birthdate based on norfolk_date and age
		if norfolk_date and age:
			try:
				# Use norfolk_date directly as it is already a datetime.date object
				birth_year = norfolk_date.year - int(age)
				birth_date = norfolk_date.replace(year=birth_year)
			except (ValueError, AttributeError):
				birth_date = None

		# Calculate height in cm based on feet and inches
		if height_feet or height_inches:
			try:
				height_cm = (
					(float(height_feet) * 30.48 if height_feet else 0) +
					(float(height_inches) * 2.54 if height_inches else 0)
				)
				if height_cm ==0:
					
					height_cm = None
			except ValueError:
				height_cm = None


		# Insert the new human record
		insert_query = f"""
			INSERT INTO humans (HumanId, FirstName, MiddleName, LastName, age_string, BirthDate, BirthDateAccuracy, RacialDescriptor, Sex, Height_cm, DateUpdated) 
			VALUES (
				'{human_id}', 
				{f"'{first_name}'" if first_name else 'NULL'}, 
				{f"'{middle_name}'" if middle_name else 'NULL'}, 
				{f"'{last_name}'" if last_name else 'NULL'}, 
				{f"'{age_string}'" if age_string else 'NULL'}, 
				{f"'{birth_date}'" if birth_date else 'NULL'}, 
				'Y', 
				{f"'{color}'" if color else 'NULL'}, 
				{f"'{sex}'" if sex else 'NULL'}, 
				{height_cm if height_cm is not None else 'NULL'}, 
				NOW()
			)
		"""

		unprocessed_result.append({
			"insert_query": insert_query,
			"human_id": human_id,
			"FirstName": first_name,
			"MiddleName": middle_name,
			"LastName": last_name,
			"height_feet":height_feet,
			"height_inches":height_inches,
			"height_cm":height_cm,
			"norfolk_date":norfolk_date,
			"age":age,
			"birth_date":birth_date,

			"manifest_id": manifest_id
		})
		cursor.execute(insert_query)
		connection.commit()
		# else:
		# 	human_id = human_match["HumanId"]

		if human_id:
			# Update the raw_manifest table with the found or created human_id
			update_query = """
				UPDATE raw_manifest 
				SET enslaved_humanId = %s,
				dateupdated=NOW() 
				WHERE manifest_id = %s
			"""
			cursor.execute(update_query, (human_id, manifest_id))
			connection.commit()
			pass
		else:
			print("manifest_id", manifest_id)
			unprocessed_result.append({
				"human_id": human_id,
				"FirstName": first_name,
				"MiddleName": middle_name,
				"LastName": last_name,
				"manifest_id": manifest_id
			})

	# Close the database connection
	connection.close()

	return "done!"




def update_humans_firstname():
	# Connect to the database
	cursor, connection = ConnectToDatabase()

	# Fetch rows where FirstName contains a space
	query = """
		SELECT HumanId, FirstName 
		FROM humans 
		WHERE FirstName LIKE '% %'
	"""
	cursor.execute(query)
	rows = cursor.fetchall()

	# Process each row
	for row in rows:
		human_id = row["HumanId"]
		first_name = row["FirstName"]

		# Split the FirstName into first word and the rest
		parts = first_name.split(' ', 1)
		new_first_name = parts[0].strip()
		new_middle_name = parts[1].strip() if len(parts) > 1 else None

		# Print the update query with actual data
		update_query = f"""
			UPDATE humans 
			SET FirstName = '{new_first_name}', MiddleName = '{new_middle_name}' 
			WHERE HumanId = '{human_id}'
		"""
		# print(update_query)
		cursor.execute(update_query)
		connection.commit()

	# Close the database connection
	connection.close()

	return update_query

def resolve_duplicate_enslaved_humanid():
	# Connect to the database
	cursor, connection = ConnectToDatabase()

	# Use a temporary table to avoid the "target table" error
	temp_table_query = """
		CREATE TEMPORARY TABLE temp_human_ids AS
		SELECT humanid
		FROM humans 
		JOIN raw_manifest ON humans.humanid = raw_manifest.enslaved_humanid
		GROUP BY humanid
		HAVING COUNT(*) > 1
	"""
	cursor.execute(temp_table_query)

	# Update the raw_manifest table using the temporary table
	update_query = """
		UPDATE raw_manifest
		SET enslaved_humanid = NULL
		WHERE enslaved_humanid IN (SELECT humanid FROM temp_human_ids)
	"""
	cursor.execute(update_query)
	connection.commit()

	# Drop the temporary table
	drop_temp_table_query = "DROP TEMPORARY TABLE temp_human_ids"
	cursor.execute(drop_temp_table_query)

	# Close the database connection
	connection.close()
	

# Run the function
