import uuid
from _Lib import Database
from _Lib.Debugger import Debugger

def sanitize(value):
	# Simple helper to convert None to empty string
	return "" if value is None else value

def save_timeline(timeline_data):
	try:
		# Extract timeline fields from request data
		human_id = timeline_data.get('HumanId')
		date_circa = timeline_data.get('Date_Circa')  # expected format: YYYY-MM-DD
		# Check for both 'date_accuracy' (lowercase) and 'Date_Accuracy' (uppercase); default to "D"
		date_accuracy = timeline_data.get('date_accuracy') or timeline_data.get('Date_Accuracy') or "D"
		location_type = timeline_data.get('LocationType')
		role_id = timeline_data.get('RoleId')  # Extract RoleId from request data
		
		# Generate a unique LocationId
		location_id =  timeline_data.get('LocationId')
		
		cursor, connection = Database.ConnectToDatabase()
		query = """
			INSERT INTO humantimeline (HumanId, LocationId, date_circa, date_accuracy, LocationType, RoleId, DateUpdated)
			VALUES (%s, %s, %s, %s, %s, %s, NOW())
			ON DUPLICATE KEY UPDATE 
				date_circa = VALUES(date_circa),
				date_accuracy = VALUES(date_accuracy),
				LocationType = VALUES(LocationType),
				RoleId = VALUES(RoleId),
				DateUpdated = NOW()
		"""
		cursor.execute(query, (human_id, location_id, date_circa, date_accuracy, location_type, role_id))
		
		
		connection.commit()
		return {"success": True, "TimelineId": location_id}
	except Exception as e:
		return Debugger(e)
