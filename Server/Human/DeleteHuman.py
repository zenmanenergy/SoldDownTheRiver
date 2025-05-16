from _Lib import Database

def delete_human(HumanId):
	
	cursor, connection = Database.ConnectToDatabase()

	
	query = f"DELETE from humanclosure WHERE AncestorHumanId = '{HumanId}' or DescendantHumanId = '{HumanId}'"
	cursor.execute(query)
	connection.commit()


	query = f"DELETE from humanrelationships WHERE ParentHumanId = '{HumanId}' or ChildHumanId = '{HumanId}'"
	cursor.execute(query)
	connection.commit()

	query = f"DELETE from humansaka WHERE HumanId = '{HumanId}'"
	print(query)
	cursor.execute(query)

	query = f"DELETE from humantimeline WHERE HumanId = '{HumanId}'"
	cursor.execute(query)
	connection.commit()

	query = f"DELETE FROM voyagehumans WHERE HumanId = '{HumanId}'"
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
