import uuid

def InsertTransaction(connection, cursor, txn):
	# Check if a transaction with the given NOLA_ID already exists
	query = f"SELECT TransactionId FROM transactions WHERE NOLA_ID='{txn['NOLA_ID']}'"
	cursor.execute(query)
	row = cursor.fetchone()
	
	if row:
		# Existing transaction: update row
		transactionId = row['TransactionId']
		update_query = f"""
			UPDATE transactions SET
				date_circa='{txn['date_circa']}',
				date_accuracy='{txn['date_accuracy']}',
				TransactionType='{txn['TransactionType']}',
				Notes='{txn['Notes'].replace("'", "''")}',
				Act='{txn['Act']}',
				Page='{txn['Page']}',
				Volume='{txn['Volume']}',
				URL='{txn['URL']}',
				NeedsReview={txn['NeedsReview']},
				Transcriber='{txn['Transcriber']}',
				Parsed_Notes='{txn['Parsed_Notes'].replace("'", "''")}',
				QuantityOfSlaves={txn['QuantityOfSlaves']},
				TotalPrice={txn['TotalPrice']},
				dataIssue='{txn['dataIssue']}',
				Issues='{txn['Issues']}',
				LocationId={ 'NULL' if txn['LocationId'] is None else f"'{txn['LocationId']}'" },
				processedNotes={txn['processedNotes']},
				isApproved={txn['isApproved']},
				DataQuestions='{txn['DataQuestions'].replace("'", "''")}',
				DateUpdated=NOW()
			WHERE TransactionId='{transactionId}'
		"""
		cursor.execute(update_query)
	else:
		# New transaction: generate TransactionId if not provided and insert new record
		transactionId = txn.get('TransactionId') or "TXN" + str(uuid.uuid4()).replace("-", "")
		txn['TransactionId'] = transactionId
		insert_query = f"""
			INSERT INTO transactions
			(TransactionId, date_circa, date_accuracy, TransactionType, Notes, Act, Page, Volume, URL, NeedsReview, Transcriber, NOLA_ID, Parsed_Notes, QuantityOfSlaves, TotalPrice, dataIssue, Issues, LocationId, processedNotes, isApproved, DataQuestions, DateUpdated)
			VALUES (
				'{transactionId}',
				'{txn['date_circa']}',
				'{txn['date_accuracy']}',
				'{txn['TransactionType']}',
				'{txn['Notes'].replace("'", "''")}',
				'{txn['Act']}',
				'{txn['Page']}',
				'{txn['Volume']}',
				'{txn['URL']}',
				{txn['NeedsReview']},
				'{txn['Transcriber']}',
				'{txn['NOLA_ID']}',
				'{txn['Parsed_Notes'].replace("'", "''")}',
				{txn['QuantityOfSlaves']},
				{txn['TotalPrice']},
				'{txn['dataIssue']}',
				'{txn['Issues']}',
				{ 'NULL' if txn['LocationId'] is None else f"'{txn['LocationId']}'" },
				{txn['processedNotes']},
				{txn['isApproved']},
				'{txn['DataQuestions'].replace("'", "''")}',
				NOW()
			)
		"""
		cursor.execute(insert_query)
	
	return transactionId
