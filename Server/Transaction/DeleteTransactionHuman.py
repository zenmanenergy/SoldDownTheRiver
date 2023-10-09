from Lib import Database

def delete_transactionhuman(TransactionId, HumanId):
	# Delete the specified row from the Transactions table
	query = f"DELETE FROM TransactionHumans WHERE TransactionId = '{TransactionId}' and  HumanId = '{HumanId}'"
	cursor, connection = Database.ConnectToDatabase()
	cursor.execute(query)
	connection.commit()
	connection.close()

	return {'success': True,'message': f'Transaction with TransactionId {TransactionId} HumanId {HumanId} deleted successfully.'}
