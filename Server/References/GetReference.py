from _Lib.Database import ConnectToDatabase

def get_reference(SessionId, ReferenceId):
	cursor, connection = ConnectToDatabase()
	query = """
		SELECT ReferenceId, URL, Notes, dateUpdated
		FROM reference
		WHERE ReferenceId = %s
	"""
	cursor.execute(query, (ReferenceId,))
	result = cursor.fetchone() or {}
	connection.close()
	return result
