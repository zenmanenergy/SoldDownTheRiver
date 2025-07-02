from _Lib.Database import ConnectToDatabase

def get_link_references(LinkId, TargetType):
	cursor, connection = ConnectToDatabase()
	sql = """
			SELECT r.ReferenceId, r.URL, r.Notes, r.dateUpdated
			FROM referencelinks rl
			JOIN reference r ON rl.ReferenceId = r.ReferenceId
			WHERE rl.LinkId = %s AND rl.TargetType = %s
		"""
	cursor.execute(sql, (LinkId, TargetType))
	result = cursor.fetchall() or []
	connection.close()
	return result

