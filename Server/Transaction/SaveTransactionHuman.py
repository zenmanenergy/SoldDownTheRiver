import uuid
from _Lib import Database
import datetime

def save_transactionhuman(TransactionId, HumanId, Price, Notes):
	
	# Connect to the database
	cursor, connection = Database.ConnectToDatabase()
	


	
	query = "INSERT INTO TransactionHumans (TransactionId, HumanId, Price, Notes) VALUES (%s, %s, %s, %s)"
	query +=" ON DUPLICATE KEY UPDATE TransactionId=values(TransactionId),HumanId=values(HumanId),Price=values(Price),Notes=values(Notes)"
		
	values = (TransactionId, HumanId, Price, Notes)

	print(query % values)

	# Execute the query and commit the changes
	cursor.execute(query, values)
	connection.commit()

	# Close the database connection 
	connection.close()

	# Return the TransactionId as a JSON response
	return {'success': True, 'TransactionId:HumanId': TransactionId+":"+HumanId}
