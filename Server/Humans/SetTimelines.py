from _Lib import Database

def set_timelines():
	
	cursor, connection = Database.ConnectToDatabase()

	# First insert statement: NotaryHumanId
	query1 = """
		INSERT IGNORE INTO humantimeline(HumanId, LocationId, date_circa, date_accuracy)
		SELECT DISTINCT
			NotaryHumanId AS HumanId,
			LocationId,
			date_circa,
			date_accuracy
		FROM transactions
		JOIN humans ON humans.HumanId = transactions.NotaryHumanId
		WHERE LocationId IS NOT NULL
			AND NotaryHumanId IS NOT NULL
			AND date_circa IS NOT NULL
			AND date_accuracy IS NOT NULL
		ORDER BY NotaryHumanId, LocationId, date_circa
	"""
	print(query1)
	cursor.execute(query1)
	connection.commit()

	# Second insert statement: Join partyhumans with transactions on FirstPartyId
	query2 = """
		INSERT IGNORE INTO humantimeline(HumanId, LocationId, date_circa, date_accuracy)
		SELECT DISTINCT
			partyhumans.HumanId,
			transactions.LocationId,
			transactions.date_circa,
			transactions.date_accuracy
		FROM transactions
		JOIN partyhumans ON transactions.FirstPartyId = partyhumans.PartyId
		WHERE transactions.LocationId IS NOT NULL
			AND transactions.FirstPartyId IS NOT NULL
			AND transactions.date_circa IS NOT NULL
			AND transactions.date_accuracy IS NOT NULL
		ORDER BY partyhumans.HumanId, transactions.LocationId, transactions.date_circa
	"""
	print(query2)
	cursor.execute(query2)
	connection.commit()

	# Third insert statement: Join partyhumans with transactions on SecondPartyId
	query3 = """
		INSERT IGNORE INTO humantimeline(HumanId, LocationId, date_circa, date_accuracy)
		SELECT DISTINCT
			partyhumans.HumanId,
			transactions.LocationId,
			transactions.date_circa,
			transactions.date_accuracy
		FROM transactions
		JOIN partyhumans ON transactions.SecondPartyId = partyhumans.PartyId
		WHERE transactions.LocationId IS NOT NULL
			AND transactions.SecondPartyId IS NOT NULL
			AND transactions.date_circa IS NOT NULL
			AND transactions.date_accuracy IS NOT NULL
		ORDER BY partyhumans.HumanId, transactions.LocationId, transactions.date_circa
	"""
	print(query3)
	cursor.execute(query3)
	connection.commit()

	# Fourth insert statement: Join transactionhumans with transactions
	query4 = """
		INSERT IGNORE INTO humantimeline(HumanId, LocationId, date_circa, date_accuracy)
		SELECT DISTINCT
			transactionhumans.HumanId,
			transactions.LocationId,
			transactions.date_circa,
			transactions.date_accuracy
		FROM transactions
		JOIN transactionhumans ON transactions.TransactionId = transactionhumans.TransactionId
		WHERE transactions.LocationId IS NOT NULL
			AND transactionhumans.HumanId IS NOT NULL
			AND transactions.date_circa IS NOT NULL
			AND transactions.date_accuracy IS NOT NULL
		ORDER BY transactionhumans.HumanId, transactions.LocationId, transactions.date_circa
	"""
	print(query4)
	cursor.execute(query4)
	connection.commit()

	# Fifth insert statement: HumanId from voyagehumans with StartLocationId and StartDate
	query5 = """
		INSERT IGNORE INTO humantimeline(HumanId, LocationId, date_circa, date_accuracy)
		SELECT DISTINCT
			voyagehumans.HumanId,
			voyages.StartLocationId AS LocationId,
			voyages.StartDate AS date_circa,
			'D' AS date_accuracy
		FROM voyages
		JOIN voyagehumans ON voyages.VoyageId = voyagehumans.VoyageId
		WHERE voyagehumans.HumanId IS NOT NULL
			AND voyages.StartLocationId IS NOT NULL
			AND voyages.StartDate IS NOT NULL
		ORDER BY voyagehumans.HumanId, voyages.StartLocationId, voyages.StartDate
	"""
	print(query5)
	cursor.execute(query5)
	connection.commit()

	# Sixth insert statement: HumanId from voyagehumans with EndLocationId and EndDate
	query6 = """
		INSERT IGNORE INTO humantimeline(HumanId, LocationId, date_circa, date_accuracy)
		SELECT DISTINCT
			voyagehumans.HumanId,
			voyages.EndLocationId AS LocationId,
			voyages.EndDate AS date_circa,
			'D' AS date_accuracy
		FROM voyages
		JOIN voyagehumans ON voyages.VoyageId = voyagehumans.VoyageId
		WHERE voyagehumans.HumanId IS NOT NULL
			AND voyages.EndLocationId IS NOT NULL
			AND voyages.EndDate IS NOT NULL
		ORDER BY voyagehumans.HumanId, voyages.EndLocationId, voyages.EndDate
	"""
	print(query6)
	cursor.execute(query6)
	connection.commit()

	connection.close()

	return {"status": "success", "message": "Timelines set successfully"}

