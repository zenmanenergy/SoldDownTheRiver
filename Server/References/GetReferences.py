from _Lib.Database import ConnectToDatabase

def get_references(SessionId):
	cursor, connection = ConnectToDatabase()
	query = """
		SELECT ReferenceId, URL, Notes, dateUpdated 
		FROM reference
		ORDER BY dateUpdated DESC, URL;
	"""
	cursor.execute(query)
	result = cursor.fetchall() or []
	connection.close()
	return result
