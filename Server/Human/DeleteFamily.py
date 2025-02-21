from _Lib import Database

def delete_Family(HumanId, FamilyHumanId):
	# Delete the specified row from the Humans table
	query = "DELETE from families WHERE HumanId = %s and FamilyHumanId = %s"
	values = (HumanId, FamilyHumanId)
	cursor, connection = Database.ConnectToDatabase()
	cursor.execute(query, values)
	connection.commit()
	query = "DELETE from families WHERE HumanId = %s and FamilyHumanId = %s"
	values = (FamilyHumanId,HumanId)
	cursor, connection = Database.ConnectToDatabase()
	cursor.execute(query, values)
	connection.commit()

	connection.close()

	return {'success': True,'message': f'Human with ID {HumanId} deleted successfully.'}
