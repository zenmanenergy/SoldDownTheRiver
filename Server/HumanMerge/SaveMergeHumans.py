import uuid
from _Lib import Database

def save_mergehumans(HumanId, MergeHumanId):
	# Connect to the database
	cursor, connection = Database.ConnectToDatabase()

	# Check if the HumanId is present
	if HumanId and MergeHumanId:
		
		# Create a new HumanId
		NewHumanId = "HUM"+str(uuid.uuid4())
		
		# Insert a new record into the humans table
		insert_query = f"""
		INSERT INTO humans (HumanId, FirstName, MiddleName, LastName, Notes, age_string, BirthDate, BirthDateAccuracy, BirthPlace, RacialDescriptor, Sex, Height_cm, DateUpdated, originCity, physical_features, profession) 
		SELECT '{NewHumanId}', 
			COALESCE(h1.FirstName, h2.FirstName), 
			COALESCE(h1.MiddleName, h2.MiddleName), 
			COALESCE(h1.LastName, h2.LastName), 
			COALESCE(h1.Notes, h2.Notes), 
			COALESCE(h1.age_string, h2.age_string), 
			COALESCE(h1.BirthDate, h2.BirthDate), 
			COALESCE(h1.BirthDateAccuracy, h2.BirthDateAccuracy), 
			COALESCE(h1.BirthPlace, h2.BirthPlace), 
			COALESCE(h1.RacialDescriptor, h2.RacialDescriptor), 
			COALESCE(h1.Sex, h2.Sex), 
			COALESCE(h1.Height_cm, h2.Height_cm), 
			COALESCE(h1.DateUpdated, h2.DateUpdated), 
			COALESCE(h1.originCity, h2.originCity), 
			COALESCE(h1.physical_features, h2.physical_features), 
			COALESCE(h1.profession, h2.profession)
		FROM humans h1
		LEFT JOIN humans h2 ON h2.HumanId = '{MergeHumanId}'
		WHERE h1.HumanId = '{HumanId}'
		"""
		cursor.execute(insert_query)
		
		# Update the original records to set mergedHumanId
		update_query = f"""
		UPDATE humans
		SET mergedHumanId = '{NewHumanId}'
		WHERE HumanId IN ('{HumanId}', '{MergeHumanId}')
		"""
		cursor.execute(update_query)
		
		# List of tables to copy records from
		tables = [
			("transactions", "NotaryHumanId"), 
			("transactionhumans", "HumanId"), 
			("partyhumans", "HumanId"), 
			("voyagehumans", "HumanId"), 
			("humantimeline", "HumanId"), 
			("humantimelines", "HumanId"),
			("voyages", "CaptainHumanId")
		]
		
		# Copy records from each table
		for table, column in tables:
			copy_query = f"""
			INSERT INTO {table} (SELECT * FROM {table} WHERE {column} = '{HumanId}')
			"""
			cursor.execute(copy_query)
			copy_query = f"""
			INSERT INTO {table} (SELECT * FROM {table} WHERE {column} = '{MergeHumanId}')
			"""
			cursor.execute(copy_query)
		
		# Special handling for voyagehumans table
		voyagehumans_columns = [
			"SellingSlaveTraderHumanId", "BuyingSlaveTraderHumanId", 
			"ShippingAgentHumanId", "CollectingAgentHumanId"
		]
		for column in voyagehumans_columns:
			copy_query = f"""
			INSERT INTO voyagehumans (SELECT * FROM voyagehumans WHERE {column} = '{HumanId}')
			"""
			cursor.execute(copy_query)
			copy_query = f"""
			INSERT INTO voyagehumans (SELECT * FROM voyagehumans WHERE {column} = '{MergeHumanId}')
			"""
			cursor.execute(copy_query)
		
		# Commit the changes
		connection.commit()

		# Return the NewHumanId as a JSON response
		return {'success': True, 'HumanId': NewHumanId}

	# Return an error response if HumanId or MergeHumanId is missing
	return {'success': False, 'message': 'HumanId or MergeHumanId is missing'}
