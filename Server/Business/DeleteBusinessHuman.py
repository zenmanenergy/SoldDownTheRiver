from _Lib import Database

def Delete_BusinessHuman(BusinessId,HumanId):
	# Delete the specified row from the Businesses table
	query = f"DELETE from businesshumans WHERE BusinessId = '{BusinessId}' and HumanId = '{HumanId}'"
	cursor, connection = Database.ConnectToDatabase()
	cursor.execute(query)
	connection.commit()
	connection.close()

	return {'success': True,'message': f'businesshumans with BusinessId {BusinessId} and HumanId {HumanId} deleted successfully.'}
