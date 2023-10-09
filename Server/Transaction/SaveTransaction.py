import uuid
from Lib import Database
import datetime

def save_transaction(TransactionId, TransactionDate, FromBusinessId, ToBusinessId, TransactionType, Notes, Act, Page, NotaryBusinessId, Volume, URL):
	
	print("TransactionDate", TransactionDate)
	print("TransactionDate1", datetime.datetime.strptime(str(TransactionDate), '%Y-%m-%d %H:%M:%S'))
	# Convert the TransactionDate string into a datetime object
	TransactionDate = str(TransactionDate)
	TransactionDate = datetime.datetime.strptime(TransactionDate, '%Y-%m-%d %H:%M:%S')
	TransactionDateTime = TransactionDate.strftime('%Y-%m-%d %H:%M:%S')
	
	# Connect to the database
	cursor, connection = Database.ConnectToDatabase()
	


	# Check if the TransactionId is present
	if TransactionId:
		# If the TransactionId is present, update the existing transaction
		query = "UPDATE Transactions SET TransactionDate = %s, FromBusinessId = %s, ToBusinessId = %s, TransactionType = %s, Notes = %s, Act = %s, Page = %s, NotaryBusinessId = %s, Volume = %s, URL = %s WHERE TransactionId = %s"
		values = (TransactionDateTime, FromBusinessId, ToBusinessId, TransactionType, Notes, Act, Page, NotaryBusinessId, Volume, URL, TransactionId)
	else:
		# If the TransactionId is not present, create a new transaction
		TransactionId = "TRN"+str(uuid.uuid4())
		query = "INSERT INTO Transactions (TransactionId, TransactionDate, FromBusinessId, ToBusinessId, TransactionType, Notes, Act, Page, NotaryBusinessId, Volume, URL) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
		values = (TransactionId, TransactionDateTime, FromBusinessId, ToBusinessId, TransactionType, Notes, Act, Page, NotaryBusinessId, Volume, URL)

	print(query.format(*values))

	# Execute the query and commit the changes
	cursor.execute(query, values)
	connection.commit()

	# Close the database connection 
	connection.close()

	# Return the TransactionId as a JSON response
	return {'success': True, 'TransactionId': TransactionId}
