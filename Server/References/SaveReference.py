from _Lib.Database import ConnectToDatabase
import uuid
from datetime import datetime

def save_reference(SessionId, ReferenceId, URL, Notes):
	cursor, connection = ConnectToDatabase()
	if not ReferenceId:
		ReferenceId = str(uuid.uuid4())
		query = """
			INSERT INTO reference (ReferenceId, URL, Notes, dateUpdated)
			VALUES (%s, %s, %s, NOW())
		"""
		cursor.execute(query, (ReferenceId, URL, Notes))
	else:
		query = """
			UPDATE reference
			SET URL = %s, Notes = %s, dateUpdated = NOW()
			WHERE ReferenceId = %s
		"""
		cursor.execute(query, (URL, Notes, ReferenceId))
	connection.commit()
	connection.close()
	return { "success": True, "ReferenceId": ReferenceId }
