from _Lib.Database import ConnectToDatabase
from datetime import datetime
import uuid

def add_reference_link(ReferenceId, LinkId, TargetType, URL, Notes):
	cursor, connection = ConnectToDatabase()
	try:
		now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
		if not ReferenceId:
			ReferenceId = str(uuid.uuid4())
			ref_query = """
				INSERT INTO reference (ReferenceId, URL, Notes, dateUpdated)
				VALUES (%s, %s, %s, %s)
			"""
			cursor.execute(ref_query, (ReferenceId, URL, Notes, now))
		else:
			ref_query = """
				UPDATE reference
				SET URL = %s, Notes = %s, dateUpdated = %s
				WHERE ReferenceId = %s
			"""
			cursor.execute(ref_query, (URL, Notes, now, ReferenceId))
		link_query = """
			INSERT INTO referencelinks (ReferenceId, LinkId, TargetType, dateUpdated)
			VALUES (%s, %s, %s, %s)
			ON DUPLICATE KEY UPDATE dateUpdated = VALUES(dateUpdated)
		"""
		cursor.execute(link_query, (ReferenceId, LinkId, TargetType, now))
		connection.commit()
		return {"success": True, "ReferenceId": ReferenceId}
	except Exception as e:
		connection.rollback()
		return {"error": str(e)}
	finally:
		connection.close()
