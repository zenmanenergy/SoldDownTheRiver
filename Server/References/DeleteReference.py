from _Lib.Database import ConnectToDatabase

def delete_reference(SessionId, ReferenceId):
	cursor, connection = ConnectToDatabase()
	query = "DELETE FROM reference WHERE ReferenceId = %s"
	cursor.execute(query, (ReferenceId,))
	connection.commit()
	connection.close()
	return { "success": True }
