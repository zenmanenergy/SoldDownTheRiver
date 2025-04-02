from _Lib import Database
from _Lib.Debugger import Debugger

def delete_timeline(timeline_data):
	try:
		# Extract necessary fields using "LocationId"
		human_id = timeline_data.get('HumanId')
		location_id = timeline_data.get('LocationId')
		
		cursor, connection = Database.ConnectToDatabase()
		query = """
			DELETE FROM humantimeline
			WHERE HumanId = %s AND LocationId = %s
		"""
		cursor.execute(query, (human_id, location_id))
		connection.commit()
		return {"success": True}
	except Exception as e:
		return Debugger(e)
