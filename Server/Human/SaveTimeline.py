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
		
		# Generate a unique LocationId
		location_id = str(uuid.uuid4())
		
		cursor, connection = Database.ConnectToDatabase()
		query = """
			INSERT INTO humantimeline (HumanId, LocationId, date_circa, date_accuracy, LocationType)
			VALUES (%s, %s, %s, %s, %s)
			ON DUPLICATE KEY UPDATE 
				date_circa = VALUES(date_circa),
				date_accuracy = VALUES(date_accuracy)
		"""
		cursor.execute(query, (human_id, location_id, date_circa, date_accuracy, location_type))
		
		# Prepare fields for the locations table
		name = sanitize(timeline_data.get("Name"))
		address = sanitize(timeline_data.get("Address"))
		city = sanitize(timeline_data.get("City"))
		county = sanitize(timeline_data.get("County"))
		state = sanitize(timeline_data.get("State"))
		state_abbr = sanitize(timeline_data.get("State_abbr"))
		country = sanitize(timeline_data.get("Country"))
		latitude = timeline_data.get("Latitude")
		longitude = timeline_data.get("Longitude")
		# Use same location_type as before
		
		insert_query = """
			INSERT INTO locations (LocationId, Name, Address, City, County, State, State_abbr, Country, Latitude, Longitude, LocationType, DateUpdated)
			VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
			ON DUPLICATE KEY UPDATE
				Address = VALUES(Address),
				City = VALUES(City),
				County = VALUES(County),
				State = VALUES(State),
				State_abbr = VALUES(State_abbr),
				Country = VALUES(Country),
				Latitude = VALUES(Latitude),
				Longitude = VALUES(Longitude),
				LocationType = VALUES(LocationType)
		"""
		cursor.execute(insert_query, (location_id, name, address, city, county, state, state_abbr, country, latitude, longitude, location_type))
		connection.commit()
		return {"success": True, "TimelineId": location_id}
	except Exception as e:
		return Debugger(e)
