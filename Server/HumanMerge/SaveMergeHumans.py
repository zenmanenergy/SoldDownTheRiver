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
		INSERT INTO humans (HumanId, FirstName, MiddleName, LastName, isCompany, Notes, age_string, BirthDate, BirthDateAccuracy, BirthPlace, RacialDescriptor, Sex, Height_cm, DateUpdated, originCity, physical_features, profession, mergedHumanId, spouseHumanId, swap_FirstName, swap_LastName) 
		SELECT '{NewHumanId}', 
			COALESCE(h1.FirstName, h2.FirstName), 
			COALESCE(h1.MiddleName, h2.MiddleName), 
			COALESCE(h1.LastName, h2.LastName), 
			COALESCE(h1.isCompany, h2.isCompany), 
			COALESCE(h1.Notes, h2.Notes), 
			COALESCE(h1.age_string, h2.age_string), 
			COALESCE(h1.BirthDate, h2.BirthDate), 
			COALESCE(h1.BirthDateAccuracy, h2.BirthDateAccuracy), 
			COALESCE(h1.BirthPlace, h2.BirthPlace), 
			COALESCE(h1.RacialDescriptor, h2.RacialDescriptor), 
			COALESCE(h1.Sex, h2.Sex), 
			COALESCE(h1.Height_cm, h2.Height_cm), 
			NOW(),
			COALESCE(h1.originCity, h2.originCity), 
			COALESCE(h1.physical_features, h2.physical_features), 
			COALESCE(h1.profession, h2.profession), 
			COALESCE(h1.mergedHumanId, h2.mergedHumanId), 
			COALESCE(h1.spouseHumanId, h2.spouseHumanId), 
			COALESCE(h1.swap_FirstName, h2.swap_FirstName), 
			COALESCE(h1.swap_LastName, h2.swap_LastName)
		FROM humans h1
		LEFT JOIN humans h2 ON h2.HumanId = '{MergeHumanId}'
		WHERE h1.HumanId = '{HumanId}'
		"""
		cursor.execute(insert_query)
		
		# Move the original records to humansarchive table before deleting them
		archive_query = f"""
		INSERT INTO humansarchive (HumanId, FirstName, MiddleName, LastName, isCompany, Notes, age_string, BirthDate, BirthDateAccuracy, BirthPlace, RacialDescriptor, Sex, Height_cm, DateUpdated, originCity, physical_features, profession, mergedHumanId, spouseHumanId, swap_FirstName, swap_LastName, DateArchived)
		SELECT HumanId, FirstName, MiddleName, LastName, isCompany, Notes, age_string, BirthDate, BirthDateAccuracy, BirthPlace, RacialDescriptor, Sex, Height_cm, DateUpdated, originCity, physical_features, profession, '{NewHumanId}' as mergedHumanId, spouseHumanId, swap_FirstName, swap_LastName, NOW() as DateArchived
		FROM humans 
		WHERE HumanId IN ('{HumanId}', '{MergeHumanId}')
		"""
		cursor.execute(archive_query)
		
		# Delete the original records from humans table
		delete_query = f"""
		DELETE FROM humans
		WHERE HumanId IN ('{HumanId}', '{MergeHumanId}')
		"""
		cursor.execute(delete_query)
		
		# List of tables to update - simply change HumanId references to point to the new merged human
		tables = [
			("transactionhumans", "HumanId"), 
			("voyagehumans", "HumanId"), 
			("humanroles", "HumanId"),
			("humantimeline", "HumanId"),
			("humansaka", "HumanId"),
			("humanrelationships", "ParentHumanId"),
			("humanrelationships", "ChildHumanId"),
			("humanclosure", "AncestorHumanId"),
			("humanclosure", "DescendantHumanId")
		]
		
		# Update all references to point to the new merged human
	
		for table, column in tables:
			update_query_1 = f"""
			UPDATE {table} SET {column} = '{NewHumanId}', DateUpdated = NOW()
			WHERE {column} = '{HumanId}'
			"""
			update_query_2 = f"""
			UPDATE {table} SET {column} = '{NewHumanId}', DateUpdated = NOW()
			WHERE {column} = '{MergeHumanId}'
			"""
			try:
				cursor.execute(update_query_1)
			except Exception as e:
				if hasattr(e, 'args') and e.args and '1062' in str(e.args[0]):
					pass  # Ignore duplicate entry error
				else:
					raise
			try:
				cursor.execute(update_query_2)
			except Exception as e:
				if hasattr(e, 'args') and e.args and '1062' in str(e.args[0]):
					pass  # Ignore duplicate entry error
				else:
					raise
		
		# Update voyages table where humans are captains
		update_query = f"""
		UPDATE voyages SET CaptainHumanId = '{NewHumanId}', DateUpdated = NOW()
		WHERE CaptainHumanId = '{HumanId}'
		"""
		cursor.execute(update_query)
		update_query = f"""
		UPDATE voyages SET CaptainHumanId = '{NewHumanId}', DateUpdated = NOW()
		WHERE CaptainHumanId = '{MergeHumanId}'
		"""
		cursor.execute(update_query)
		
		# Update voyagehumans table where humans are referenced in other columns
		voyagehumans_columns = [
			"owner_humanid", "shippingagent_humanid", 
			"owner2_humanid", "collectoragent_humanid"
		]
		for column in voyagehumans_columns:
			update_query = f"""
			UPDATE voyagehumans SET {column} = '{NewHumanId}', DateUpdated = NOW()
			WHERE {column} = '{HumanId}'
			"""
			cursor.execute(update_query)
			update_query = f"""
			UPDATE voyagehumans SET {column} = '{NewHumanId}', DateUpdated = NOW()
			WHERE {column} = '{MergeHumanId}'
			"""
			cursor.execute(update_query)
		
		# Special handling for raw_manifest table - copy records where humans are referenced
		raw_manifest_columns = [
			"Owner_humanId", "ShippingAgent_humanId", "Owner2_humanId", 
			"CollectorAgent_humanId", "Captain_humanId", "enslaved_humanid"
		]
		for column in raw_manifest_columns:
			copy_query = f"""
			UPDATE raw_manifest SET {column} = '{NewHumanId}', dateupdated = NOW()
			WHERE {column} = '{HumanId}'
			"""
			cursor.execute(copy_query)
			copy_query = f"""
			UPDATE raw_manifest SET {column} = '{NewHumanId}', dateupdated = NOW()
			WHERE {column} = '{MergeHumanId}'
			"""
			cursor.execute(copy_query)
		
		# Special handling for raw_nola table - copy records where humans are referenced
		raw_nola_columns = [
			"SellerHumanId", "BuyerHumanId", "NotaryHumanId"
		]
		for column in raw_nola_columns:
			copy_query = f"""
			UPDATE raw_nola SET {column} = '{NewHumanId}'
			WHERE {column} = '{HumanId}'
			"""
			cursor.execute(copy_query)
			copy_query = f"""
			UPDATE raw_nola SET {column} = '{NewHumanId}'
			WHERE {column} = '{MergeHumanId}'
			"""
			cursor.execute(copy_query)
		
		# Update referencelinks table where humans are the target
		copy_query = f"""
		UPDATE referencelinks SET LinkId = '{NewHumanId}', dateUpdated = NOW()
		WHERE LinkId = '{HumanId}' AND TargetType = 'human'
		"""
		cursor.execute(copy_query)
		copy_query = f"""
		UPDATE referencelinks SET LinkId = '{NewHumanId}', dateUpdated = NOW()
		WHERE LinkId = '{MergeHumanId}' AND TargetType = 'human'
		"""
		cursor.execute(copy_query)
		
		# Commit the changes
		connection.commit()

		# Return the NewHumanId as a JSON response
		return {'success': True, 'HumanId': NewHumanId}

	# Return an error response if HumanId or MergeHumanId is missing
	return {'success': False, 'message': 'HumanId or MergeHumanId is missing'}
