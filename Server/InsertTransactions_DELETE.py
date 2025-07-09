import uuid
from _Lib import Database

def InsertTransaction(connection, cursor, txn):
	# Check if a transaction with the given NOLA_ID exists
	query_select = "SELECT TransactionId FROM transactions WHERE NOLA_ID = %s LIMIT 1"
	cursor.execute(query_select, (txn.get("NOLA_ID"),))
	row = cursor.fetchone()
	if row:
		# Use the existing transaction's TransactionId and update the record
		txn["TransactionId"] = row["TransactionId"]
	else:
		# Create a new transaction
		txn["TransactionId"] = "TXN" + str(uuid.uuid4()).replace("-", "")
	query_insert = (
		"INSERT INTO transactions (TransactionId, date_circa, date_accuracy, TransactionType, Notes, Act, Page, Volume, URL, NeedsReview, Transcriber, NOLA_ID, Parsed_Notes, QuantityOfSlaves, TotalPrice, dataIssue, Issues, LocationId, processedNotes, isApproved, DataQuestions, DateUpdated) "
		"VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW()) "
		"ON DUPLICATE KEY UPDATE "
		"date_circa = VALUES(date_circa), "
		"date_accuracy = VALUES(date_accuracy), "
		"TransactionType = VALUES(TransactionType), "
		"Notes = VALUES(Notes), "
		"Act = VALUES(Act), "
		"Page = VALUES(Page), "
		"Volume = VALUES(Volume), "
		"URL = VALUES(URL), "
		"NeedsReview = VALUES(NeedsReview), "
		"Transcriber = VALUES(Transcriber), "
		"Parsed_Notes = VALUES(Parsed_Notes), "
		"QuantityOfSlaves = VALUES(QuantityOfSlaves), "
		"TotalPrice = VALUES(TotalPrice), "
		"dataIssue = VALUES(dataIssue), "
		"Issues = VALUES(Issues), "
		"LocationId = VALUES(LocationId), "
		"processedNotes = VALUES(processedNotes), "
		"isApproved = VALUES(isApproved), "
		"DataQuestions = VALUES(DataQuestions), "
		"DateUpdated = NOW()"
	)
	values = (
		txn.get("TransactionId"),
		txn.get("date_circa"),
		txn.get("date_accuracy"),
		txn.get("TransactionType"),
		txn.get("Notes"),
		txn.get("Act"),
		txn.get("Page"),
		txn.get("Volume"),
		txn.get("URL"),
		txn.get("NeedsReview"),
		txn.get("Transcriber"),
		txn.get("NOLA_ID"),
		txn.get("Parsed_Notes"),
		txn.get("QuantityOfSlaves"),
		txn.get("TotalPrice"),
		txn.get("dataIssue"),
		txn.get("Issues"),
		txn.get("LocationId"),
		txn.get("processedNotes"),
		txn.get("isApproved"),
		txn.get("DataQuestions")
	)
	cursor.execute(query_insert, values)
	connection.commit()
	return txn["TransactionId"]
