import uuid
from _Lib import Database
import datetime

def save_transactionhuman(TransactionId, HumanId, RoleId):
	# Connect to the database
	cursor, connection = Database.ConnectToDatabase()

	# Prepare the query and values for transactionhumans
	relationship_query = """
		INSERT INTO transactionhumans (TransactionId, HumanId, RoleId, DateUpdated)
		VALUES (%s, %s, %s, NOW())
		ON DUPLICATE KEY UPDATE
			RoleId = VALUES(RoleId),
			DateUpdated = NOW()
	"""
	relationship_values = (TransactionId, HumanId, RoleId)

	# Print out the query with values for debugging
	print("Executing query:")
	print(relationship_query)
	print("Values:", relationship_values)

	# Execute query for transactionhumans
	cursor.execute(relationship_query, relationship_values)

	# Query transactions table for date_circa, Date_Accuracy, and LocationId
	transaction_query = "SELECT Date_Circa, Date_Accuracy, LocationId FROM transactions WHERE TransactionId = %s and Date_Circa is not null and Date_Accuracy is not null and LocationId is not null"
	cursor.execute(transaction_query, (TransactionId,))
	row = cursor.fetchone()
	if row:
		 # Updated timeline query with ON DUPLICATE KEY UPDATE clause
		timeline_query = """
			INSERT INTO humantimeline (HumanId, LocationId, Date_Circa, Date_Accuracy, DateUpdated)
			VALUES (%s, %s, %s, %s, NOW())
			ON DUPLICATE KEY UPDATE
				Date_Circa = VALUES(Date_Circa),
				Date_Accuracy = VALUES(Date_Accuracy),
				DateUpdated = NOW()
		"""
		timeline_values = (HumanId, row['LocationId'], row['Date_Circa'], row['Date_Accuracy'])
		cursor.execute(timeline_query, timeline_values)

	# Commit both changes
	connection.commit()

	connection.close()
	return {"TransactionId": TransactionId, "HumanId": HumanId, "RoleId": RoleId}
