import uuid
from _Lib import Database
import googlemaps

# Initialize Google Maps client
gmaps = googlemaps.Client(key='AIzaSyB_a1_JJZBF0g43m9KeKVrSlr7ik6_AN_Y')

def save_location(LocationId, Name, Address, City, State, County, Country, Latitude, Longitude, isApproved=False):
	# Connect to the database
	cursor, connection = Database.ConnectToDatabase()

	sql = ""

	

	# Perform geocode lookup if Latitude and Longitude are not provided
	if not Latitude or not Longitude:
		address = f"{City}, {State}, {Country}"
		geocode_result = gmaps.geocode(address)
		if geocode_result:
			print(geocode_result)

			location = geocode_result[0]['geometry']['location']
			Latitude = location['lat']
			Longitude = location['lng']

			# Extract additional details from geocode result
			address_components = {comp['types'][0]: comp['long_name'] for comp in geocode_result[0]['address_components']}
			Address = geocode_result[0].get('formatted_address', '')
			City = address_components.get('locality', City)
			County = address_components.get('administrative_area_level_2', '')
			State = address_components.get('administrative_area_level_1', State)
			Country = address_components.get('country', Country)
		else:
			Latitude = 0.0
			Longitude = 0.0

	# Convert Latitude & Longitude to float safely
	Latitude = float(Latitude) if Latitude else 'NULL'
	Longitude = float(Longitude) if Longitude else 'NULL'

	# Replace blank values with NULL for other fields
	Name = f"'{Name}'" if Name else 'NULL'
	Address = f"'{Address}'" if Address else 'NULL'
	City = f"'{City}'" if City else 'NULL'
	County = f"'{County}'" if County else 'NULL'
	State = f"'{State}'" if State else 'NULL'
	Country = f"'{Country}'" if Country else 'NULL'
	
	# Convert isApproved to boolean (ensure it's either 0 or 1)
	isApproved = 1 if str(isApproved).lower() in ["true", "1", "yes"] else 0

	if LocationId:
		# Update existing location
		sql = f"""
		UPDATE locations 
		SET Name={Name},
			Address = {Address},
			City = {City}, 
			County = {County},
			State = {State}, 
			Country = {Country}, 
			Latitude = {Latitude}, 
			Longitude = {Longitude}, 
			isApproved = {isApproved},
			DateUpdated = NOW() 
		WHERE LocationId = '{LocationId}'
		"""
	else:
		# Create new LocationId
		LocationId = "LOC" + str(uuid.uuid4())

		# Insert new location
		sql = f"""
		INSERT INTO locations (LocationId, Name, Address, City, County, State, Country, Latitude, Longitude, isApproved, DateUpdated)
		VALUES ('{LocationId}', {Name}, {Address}, {City}, {County}, {State}, {Country}, {Latitude}, {Longitude}, {isApproved}, NOW())
		ON DUPLICATE KEY UPDATE 
			Name = VALUES(Name),
			Address = VALUES(Address),
			City = VALUES(City), 
			County = VALUES(County),
			State = VALUES(State), 
			Country = VALUES(Country), 
			Latitude = VALUES(Latitude), 
			Longitude = VALUES(Longitude), 
			isApproved = VALUES(isApproved),
			DateUpdated = NOW()
		"""

	# Execute the query
	print("Executing SQL:", sql)  # Debugging output
	cursor.execute(sql)
	connection.commit()
	connection.close()

	response = {'success': True, 'LocationId': LocationId}
	print(response)
	return response
