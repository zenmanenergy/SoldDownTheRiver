from _Lib import Database

def set_timelines():
	
	cursor, connection = Database.ConnectToDatabase()
	# Fourth insert statement: Join transactionhumans with transactions
	query2 = """
		insert into humantimeline(HumanId,LocationId, Date_circa, Date_Accuracy,LocationType)
		SELECT DISTINCT
			transactionhumans.HumanId,
			raw_nola.LocationIdSecondParty,
			transactions.date_circa,
			transactions.date_accuracy,
			'Residence'
		FROM transactions
		JOIN transactionhumans ON transactions.TransactionId = transactionhumans.TransactionId
		join raw_nola on raw_nola.NOLA_ID=transactions.NOLA_ID
		WHERE transactions.LocationId IS NOT NULL
			AND transactionhumans.HumanId IS NOT NULL
			AND transactions.date_circa IS NOT NULL
			AND transactions.date_accuracy IS NOT NULL
			and raw_nola.LocationIdSecondParty is not null
			and transactionhumans.RoleId='Seller'
		
		ON DUPLICATE KEY UPDATE LocationType = VALUES(LocationType)
	"""
	print(query2)
	cursor.execute(query2)
	connection.commit()

	query3 = """
		insert into humantimeline(HumanId,LocationId, Date_circa, Date_Accuracy,LocationType)
		SELECT DISTINCT
			transactionhumans.HumanId,
			raw_nola.LocationIdFirstParty,
			transactions.date_circa,
			transactions.date_accuracy,
			'Residence'
		FROM transactions
		JOIN transactionhumans ON transactions.TransactionId = transactionhumans.TransactionId
		join raw_nola on raw_nola.NOLA_ID=transactions.NOLA_ID
		WHERE transactions.LocationId IS NOT NULL
			AND transactionhumans.HumanId IS NOT NULL
			AND transactions.date_circa IS NOT NULL
			AND transactions.date_accuracy IS NOT NULL
			and raw_nola.LocationIdFirstParty is not null
			and transactionhumans.RoleId='Buyer'
		
		ON DUPLICATE KEY UPDATE LocationType = VALUES(LocationType)
	"""
	print(query3)
	cursor.execute(query3)
	connection.commit()
	
	# Fourth insert statement: Join transactionhumans with transactions
	query4 = """
		INSERT INTO humantimeline(HumanId, LocationId, date_circa, date_accuracy, LocationType)
		SELECT DISTINCT
			transactionhumans.HumanId,
			transactions.LocationId,
			transactions.date_circa,
			transactions.date_accuracy,
			'Transaction'
		FROM transactions
		JOIN transactionhumans ON transactions.TransactionId = transactionhumans.TransactionId
		WHERE transactions.LocationId IS NOT NULL
			AND transactionhumans.HumanId IS NOT NULL
			AND transactions.date_circa IS NOT NULL
			AND transactions.date_accuracy IS NOT NULL
		ORDER BY transactionhumans.HumanId, transactions.LocationId, transactions.date_circa
		ON DUPLICATE KEY UPDATE LocationType = VALUES(LocationType)
	"""
	print(query4)
	cursor.execute(query4)
	connection.commit()

	# Fifth insert statement: HumanId from voyagehumans with StartLocationId and StartDate
	query5 = """
		INSERT INTO humantimeline(HumanId, LocationId, date_circa, date_accuracy, LocationType)
		SELECT DISTINCT
			voyagehumans.HumanId,
			voyages.StartLocationId AS LocationId,
			voyages.StartDate AS date_circa,
			'D' AS date_accuracy,
			'Voyage Start'
		FROM voyages
		JOIN voyagehumans ON voyages.VoyageId = voyagehumans.VoyageId
		WHERE voyagehumans.HumanId IS NOT NULL
			AND voyages.StartLocationId IS NOT NULL
			AND voyages.StartDate IS NOT NULL
		ORDER BY voyagehumans.HumanId, voyages.StartLocationId, voyages.StartDate
		ON DUPLICATE KEY UPDATE LocationType = VALUES(LocationType)
	"""
	print(query5)
	cursor.execute(query5)
	connection.commit()

	# Sixth insert statement: HumanId from voyagehumans with EndLocationId and EndDate
	query6 = """
		INSERT INTO humantimeline(HumanId, LocationId, date_circa, date_accuracy, LocationType)
		SELECT DISTINCT
			voyagehumans.HumanId,
			voyages.EndLocationId AS LocationId,
			voyages.EndDate AS date_circa,
			'D' AS date_accuracy,
			'Voyage End'
		FROM voyages
		JOIN voyagehumans ON voyages.VoyageId = voyagehumans.VoyageId
		WHERE voyagehumans.HumanId IS NOT NULL
			AND voyages.EndLocationId IS NOT NULL
			AND voyages.EndDate IS NOT NULL
		ORDER BY voyagehumans.HumanId, voyages.EndLocationId, voyages.EndDate
		ON DUPLICATE KEY UPDATE LocationType = VALUES(LocationType)
	"""
	print(query6)
	cursor.execute(query6)
	connection.commit()

	connection.close()

	return {"status": "success", "message": "Timelines set successfully"}

