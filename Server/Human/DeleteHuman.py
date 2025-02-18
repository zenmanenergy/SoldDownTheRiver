from _Lib import Database

def delete_human(HumanId):
	
	cursor, connection = Database.ConnectToDatabase()

	query = f"DELETE FROM BusinessHumans WHERE HumanId = '{HumanId}'"
	cursor.execute(query)
	connection.commit()
	
	query = f"DELETE FROM Families WHERE HumanId = '{HumanId}' or FamilyHumanId = '{HumanId}'"
	cursor.execute(query)
	connection.commit()

	query = f"DELETE FROM HumansAKA WHERE HumanId = '{HumanId}'"
	cursor.execute(query)
	connection.commit()

	query = f"DELETE FROM TransactionHumans WHERE HumanId = '{HumanId}'"
	cursor.execute(query)
	connection.commit()

	query = f"DELETE FROM Humans WHERE HumanId = '{HumanId}'"
	cursor.execute(query)
	connection.commit()
	
	connection.close()

	return {'success': True,'message': f'Human with ID {HumanId} deleted successfully.'}
