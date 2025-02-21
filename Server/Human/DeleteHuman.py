from _Lib import Database

def delete_human(HumanId):
	
	cursor, connection = Database.ConnectToDatabase()

	query = f"DELETE from businesshumans WHERE HumanId = '{HumanId}'"
	cursor.execute(query)
	connection.commit()
	
	query = f"DELETE from families WHERE HumanId = '{HumanId}' or FamilyHumanId = '{HumanId}'"
	cursor.execute(query)
	connection.commit()

	query = f"DELETE from humansaka WHERE HumanId = '{HumanId}'"
	cursor.execute(query)
	connection.commit()

	query = f"DELETE FROM transactionhumans WHERE HumanId = '{HumanId}'"
	cursor.execute(query)
	connection.commit()

	query = f"DELETE from humans WHERE HumanId = '{HumanId}'"
	cursor.execute(query)
	connection.commit()
	
	connection.close()

	return {'success': True,'message': f'Human with ID {HumanId} deleted successfully.'}
