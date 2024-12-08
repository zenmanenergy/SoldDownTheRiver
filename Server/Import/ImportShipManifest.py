import uuid
from Lib import Database
from Lib import History
from datetime import datetime, date, timedelta,timezone
import traceback

from dateutil import parser
import googlemaps
from collections import Counter

gmaps = googlemaps.Client(key='AIzaSyB_a1_JJZBF0g43m9KeKVrSlr7ik6_AN_Y')


def import_Manifest(data,SessionId):
	
	headers = data['Headers']
	rows = data['Data']
	Manifest_Ids = data['Manifest_Ids']
	print("len",len(rows))
	# DeleteManifests(Manifest_Ids)
	for row in rows:
		# print(row)
		# print()
		rowData={}
		if isinstance(row, list):
			# Extract specific columns from the row (example)
			

			rowData['Manifest_Id'] = row[0]
			print(rowData['Manifest_Id'])
			Timestamp_str = row[1]
			try:
				rowData['Timestamp'] = datetime.strptime(Timestamp_str, "%Y-%m-%dT%H:%M:%S.%fZ")
			except ValueError:
				# Handle cases where the date string format might differ
				try:
					rowData['Timestamp'] = datetime.strptime(Timestamp_str, "%Y-%m-%dT%H:%M:%S.%f")
				except:
					print("Timestamp_str ERROR!",Timestamp_str)
					return False
				
			# print(Timestamp_str)
			rowData['Timestamp']=rowData['Timestamp'].replace(tzinfo=timezone.utc)
			



			rowData['LastName'] = row[2].replace("'", "`")
			rowData['FirstMiddleName'] = row[3].replace("'", "`")
			rowData['Sex'] = row[4].replace("'", "`")
			rowData['Age'] = row[5]
			rowData['Height_feet'] = row[6]
			rowData['Height_inches'] = row[7]
			rowData['Color'] = row[8].replace("'", "`")
			rowData['OwnerName'] = row[9].replace("'", "`")
			rowData['OwnerLocation'] = row[10].replace("'", "`")
			rowData['AgentName'] = row[11].replace("'", "`")
			rowData['ShippingAgentLocation'] = row[12].replace("'", "`")
			rowData['Owner2'] = row[13].replace("'", "`")
			rowData['Owner2Location'] = row[14].replace("'", "`")
			rowData['ShipName'] = row[15].replace("'", "`")
			rowData['ShipSize'] = row[16].replace("'", "`")
			rowData['ShipType'] = row[17].replace("'", "`")
			rowData['ShipCaptain'] = row[18].replace("'", "`")
			rowData['ShipHomePort'] = row[19].replace("'", "`")
			rowData['NorfolkCollectorName'] = row[20].replace("'", "`")
			# if row[33]:
			# 	rowData['DateNorfolk'] = datetime.strptime(row[35], "%m/%d/%Y")
			# else:
			# 	rowData['DateNorfolk']=None
			# if row[36]:

			# 	rowData['DateNola'] = datetime.strptime(row[38], "%m/%d/%Y")
			# else:
			# 	rowData['DateNola']=None
			rowData['YearManifestNorfolk'] = row[21]
			rowData['MonthDayManifestNorfolk'] = row[22].replace("'", "`")
			

			rowData['YearNOLA'] = row[24]
			rowData['MonthDayNOLA'] = row[25].replace("'", "`")
			
			
			


			rowData['Notes'] = str(row[26]).replace("'", "`")
			rowData['Transcribers'] = str(row[27]).replace("'", "`")
			rowData['VoyageId'] = str(row[28]).replace("'", "`")
			rowData['TeamNumber'] = str(row[29]).replace("'", "`")
			rowData['referencefilename'] = str(row[30]).replace("'", "`")
			rowData['secondaryreferenceFilename'] = str(row[31]).replace("'", "`")

			# print(rowData)
			SaveManifest(rowData)


	return "done"
			
def ProcessManifest():
	cursor, connection = Database.ConnectToDatabase()
	Manifests=getManifests(cursor)
	cursor.close()
	connection.close()

	DateOfTransactions=[]
	Processed=[]
	for i, row in enumerate(Manifests):
		newRow={}
		cursor, connection = Database.ConnectToDatabase()

		newRow['Manifest_ID']=row['Manifest_ID']
		newRow['Timestamp']=row['Timestamp']
		newRow['VoyageId']=row['shipVoyageId']
		newRow['Humans']={}
		newRow['Humans']['Enslaved']={}
		newRow['Humans']['Enslaved']=ParseHumanNames(f"{row['LastName']} {row['FirstNameMiddleName']}", 'Enslaved')
		
		newRow['Humans']['Enslaved'][0]['Age']=row['Age']
		newRow['Humans']['Enslaved'][0]['Color']=row['Color']
		newRow['Humans']['Enslaved'][0]['Height_feet']=row['Height_feet']
		newRow['Humans']['Enslaved'][0]['Height_inches']=row['Height_inches']
		newRow['Humans']['Enslaved'][0]['Height_cm']=height_to_cm(row['Height_feet'], row['Height_inches'])
		newRow['Humans']['Enslaved'][0]['Sex']=row['Sex']
		newRow['Humans']['Enslaved'][0]['Notes']=row['Notes']
		# print(newRow['Humans']['Enslaved'][0])
		# print(newRow['VoyageId'])
		newRow['Humans']['Enslaved'][0]['HumanId']=GetVoyageHuman(connection, cursor, newRow['Humans']['Enslaved'][0],newRow['VoyageId'])
		

		newRow['Humans']['Captain']=ParseHumanNames(row['ShipCaptain'], 'Captain')
		if newRow['Humans']['Captain']:
			newRow['Humans']['Captain'][0]['HumanId']=GetVoyageHuman(connection, cursor, newRow['Humans']['Captain'][0],newRow['VoyageId'])

		
		newRow['Humans']['ShippingAgent']=ParseHumanNames(row['ShippingAgent'], 'ShippingAgent')
		if newRow['Humans']['ShippingAgent']:
			for human in newRow['Humans']['ShippingAgent']:
				human['LocationId']=getLocation(connection, cursor, row['ShippingAgentLocation'])
				human['HumanId']=GetVoyageHuman(connection, cursor, human,newRow['VoyageId'])


		newRow['Humans']['CollectorAgent']=ParseHumanNames(row['CollectorAgent'], 'CollectorAgent')
		if newRow['Humans']['CollectorAgent']:
			newRow['Humans']['CollectorAgent'][0]['HumanId']=GetVoyageHuman(connection, cursor, newRow['Humans']['CollectorAgent'][0],newRow['VoyageId'])
		
		newRow['Humans']['Owner1']=ParseHumanNames(row['OwnersName'], 'Owner1')
		if newRow['Humans']['Owner1']:
			for human in newRow['Humans']['Owner1']:
				human['LocationId']=getLocation(connection, cursor, row['OwnersLocation'])
				human['HumanId']=GetVoyageHuman(connection, cursor, human,newRow['VoyageId'])

		newRow['Humans']['Owner2']=ParseHumanNames(row['Owner2'], 'Owner2')
		if newRow['Humans']['Owner2']:
			for human in newRow['Humans']['Owner2']:
				human['LocationId']=getLocation(connection, cursor, row['Owner2Location'])
				human['HumanId']=GetVoyageHuman(connection, cursor, human,newRow['VoyageId'])

		newRow['Norfolk']={}
		# newRow['Norfolk']

		newRow['New Orleans']={}
		# newRow['New Orleans']

		newRow['Ship']={}
		newRow['Ship']['ShipId']=GetShipId(connection, cursor, row['ShipName'])
		newRow['Ship']['ShipName']=row['ShipName']
		newRow['Ship']['ShipSize']=row['ShipSize']
		newRow['Ship']['ShipType']=row['ShipType']
		newRow['Ship']['ShipCaptain']=row['ShipCaptain']
		newRow['Ship']['ShipHomePort']=row['ShipHomePort']
		newRow['Ship']['ShipHomePortLocationId']=getLocation(connection, cursor, row['ShipHomePort'])
		newRow['Voyage']={}
		newRow['Voyage']['Start']={}
		newRow['Voyage']['Start']['Name']="Norfolk, VA"
		newRow['Voyage']['Start']['LocationId']=getLocation(connection, cursor, "Norfolk, VA")
		newRow['Voyage']['Start']['Date']=ParseDate(row['Manifest_ID'], row['MonthDayNorfolk'],row['YearNorfolk'])
		newRow['Voyage']['End']={}
		newRow['Voyage']['End']['Name']="New Orleans, LA"
		newRow['Voyage']['End']['LocationId']=getLocation(connection, cursor, "New Orleans, LA")
		newRow['Voyage']['End']['Date']=ParseDate(row['Manifest_ID'], row['MonthDayNOLA'],row['YearNOLA'])

		newRow['Reference']={}
		newRow['Reference']['teamNumber']=row['teamNumber']
		newRow['Reference']['ReferenceScan']=row['ReferenceScan']
		newRow['Reference']['SecondReference']=row['SecondReference']
		newRow['Reference']['Transcribers']=row['Transcribers']

		newRow['Notes']=row['Notes']
		Processed.append(newRow)
		try:
			SaveShip(connection, cursor, newRow)
			SaveHumans(connection, cursor, newRow)
			SaveVoyage(connection, cursor, newRow)

		except Exception as e:
			# Print the error type, message, and traceback
			print("ERROR!")
			print(f"Type: {type(e).__name__}")
			print(f"Message: {str(e)}")
			return str(traceback.print_exc())
		connection.commit()
		cursor.close()
		connection.close()
		print(i)

	# dat={}
	# dat['orig']=row
	# dat['processed']=Processed


	return str(i+1)
	return Processed

def GetVoyageHuman(connection, cursor, data, VoyageId):
	# print(data)

	# Base SQL query
	sql = f"""
	SELECT h.HumanId
	FROM humans h
	INNER JOIN voyagehumans vh ON h.HumanId = vh.HumanId
	WHERE h.FirstName = '{data['FirstName']}' 
	  AND h.LastName = '{data['LastName']}'
	  AND vh.VoyageId = '{VoyageId}'
	"""

	# Adding optional filters based on provided values
	if 'BirthDateAccuracy' in data and data['BirthDateAccuracy']:
		sql += f" AND h.BirthDateAccuracy = '{data['BirthDateAccuracy']}'"

	if 'Notes' in data and data['Notes']:
		sql += f" AND h.Notes = '{data['Notes']}'"

	if 'Color' in data and data['Color']:
		sql += f" AND h.Color = '{data['Color']}'"

	if 'Sex' in data and data['Sex']:
		sql += f" AND h.Sex = '{data['Sex']}'"

	if 'Height_cm' in data and data['Height_cm'] is not None:
		sql += f" AND h.Height_cm = {data['Height_cm']}"

	# Print the final SQL query for debugging purposes

	# Execute the query
	cursor.execute(sql)
	result = cursor.fetchone()

	# Return the HumanId if found
	if result:
		return result['HumanId']  # HumanId is in the first column
	else:
		return None  # No matching human found

def convert_mixed_number_to_float(mixed_str):
	# Split the string by space
	parts = mixed_str.split()

	# Initialize the result
	result = 0.0

	# Handle different cases
	if len(parts) == 1:
		# Case 1: Only a whole number or a fraction
		if "/" in parts[0]:
			# It's a fraction (e.g., "7/8")
			numerator, denominator = parts[0].split("/")
			result = float(numerator) / float(denominator)
		else:
			# It's a whole number (e.g., "6")
			result = float(parts[0])

	elif len(parts) == 2:
		# Case 2: Mixed number (e.g., "3 1/4")
		# Convert the whole number part
		result = float(parts[0])
		# Convert the fraction part
		numerator, denominator = parts[1].split("/")
		fraction = float(numerator) / float(denominator)
		result += fraction

	return result


def calculate_birthdate(age, reference_date):
	# Subtract age from the reference date to get an approximate birthdate
	age=convert_mixed_number_to_float(age)
	birth_year = reference_date.year - int(age)
	return reference_date.replace(year=birth_year)
def SaveHumans(connection, cursor, data):
	for role in data['Humans']:
		for human in data['Humans'][role]:
			if len(human['FirstName'])==0 and len(human['LastName'])==0:
				continue
			if human.get('Age'):
				human['birth_date'] = calculate_birthdate(human['Age'], data['Voyage']['Start']['Date']['parsed_date'])
			else:
				human['birth_date'] = None
			# print(human)
			if human['HumanId']:
				
				HumanId=human['HumanId']
				# If a row exists, update it
				update_query = f"""
					UPDATE humans
					SET FirstName = '{human['FirstName']}', 
						MiddleName = '{human['MiddleName']}', 
						LastName = '{human['LastName']}',
						Notes = {f"'{human.get('Notes')}'" if human.get('Notes') else 'NULL'},
						BirthDate = {f"'{human['birth_date']}'" if human['birth_date'] else 'NULL'},
						BirthDateAccuracy = {f"'{human.get('BirthDateAccuracy')}'" if human.get('BirthDateAccuracy') else 'NULL'},
						BirthPlace = {f"'{human.get('BirthPlace')}'" if human.get('BirthPlace') else 'NULL'},
						Color = {f"'{human.get('Color')}'" if human.get('Color') else 'NULL'},
						Sex = {f"'{human.get('Sex')}'" if human.get('Sex') else 'NULL'},
						Height_cm = {f"'{human.get('Height_cm')}'" if human.get('Height_cm') else 'NULL'},
						DateUpdated = NOW()
					WHERE HumanId = '{HumanId}'
					"""
				# print(update_query)
				cursor.execute(update_query)
				connection.commit()
			else:
				# If no row exists, insert a new row with a unique HumanId
				HumanId = "HUM"+str(uuid.uuid4()).replace("-", "")
				insert_query = f"""
					INSERT INTO humans (HumanId, FirstName, MiddleName, LastName, Notes, BirthDate, BirthDateAccuracy, BirthPlace, Color, Sex, Height_cm, DateUpdated)
					VALUES (
						'{HumanId}', 
						'{human.get('FirstName')}', 
						'{human.get('MiddleName')}', 
						'{human.get('LastName')}', 
						{f"'{human.get('Notes')}'" if human.get('Notes') else 'NULL'},
						{f"'{human['birth_date']}'" if human['birth_date'] else 'NULL'},
						{f"'{human.get('BirthDateAccuracy')}'" if human.get('BirthDateAccuracy') else 'NULL'},
						{f"'{human.get('BirthPlace')}'" if human.get('BirthPlace') else 'NULL'},
						{f"'{human.get('Color')}'" if human.get('Color') else 'NULL'},
						{f"'{human.get('Sex')}'" if human.get('Sex') else 'NULL'},
						{f"'{round(human.get('Height_cm'),1)}'" if human.get('Height_cm') else 'NULL'},
						NOW()
					)
					"""
				# print(insert_query)
				cursor.execute(insert_query)

			insert_role = f"""
				INSERT INTO humanroles (HumanId, RoleId, date_circa, date_accuracy)
				VALUES ('{HumanId}', '{role}', 
						{f"'{data['Voyage']['Start']['Date']['parsed_date']}'" if data['Voyage']['Start']['Date']['parsed_date'] is not None else 'NULL'}, 
						{f"'{data['Voyage']['Start']['Date']['DateAccuracy']}'" if data['Voyage']['Start']['Date']['DateAccuracy'] is not None else 'NULL'})
				ON DUPLICATE KEY UPDATE 
					RoleId=VALUES(RoleId), 
					date_circa=VALUES(date_circa), 
					date_accuracy=VALUES(date_accuracy)
				"""
			# print(insert_role)
			cursor.execute(insert_role)

			insert_role = f"""
				INSERT INTO voyagehumans (VoyageId,HumanId, RoleId)
				VALUES ('{data['VoyageId']}','{HumanId}', '{role}')
				ON DUPLICATE KEY UPDATE 
					RoleId=VALUES(RoleId)
				"""
			# print(insert_role)
			cursor.execute(insert_role)
			connection.commit()


def SaveVoyage(connection, cursor, data):
	# Extracting relevant information from the data
	ship_id = data['Ship']['ShipId']
	captain_human_id = data['Humans']['Captain'][0]['HumanId']
	start_location_id = data['Voyage']['Start']['LocationId']
	end_location_id = data['Voyage']['End']['LocationId']
	start_date = data['Voyage']['Start']['Date']['parsed_date']
	end_date = data['Voyage']['End']['Date']['parsed_date']
	Notes = data.get('Notes', '')

	# Use the provided VoyageId or generate a new one
	voyage_id = data['VoyageId'] if 'VoyageId' in data else "VYG" + str(uuid.uuid4()).replace("-", "")

	# SQL query to insert or update the voyage record
	sql = f"""
	INSERT INTO voyages (VoyageId, ShipId, CaptainHumanId, StartLocationId, EndLocationId, StartDate, EndDate, Notes)
	VALUES ('{voyage_id}', '{ship_id}', '{captain_human_id}', '{start_location_id}', '{end_location_id}', {f"'{end_date}'" if end_date else 'NULL'}, {f"'{end_date}'" if end_date else 'NULL'}, '{Notes}')
	ON DUPLICATE KEY UPDATE
	ShipId = VALUES(ShipId),
	CaptainHumanId = VALUES(CaptainHumanId),
	StartLocationId = VALUES(StartLocationId),
	EndLocationId = VALUES(EndLocationId),
	StartDate = VALUES(StartDate),
	EndDate = VALUES(EndDate),
	Notes = VALUES(Notes);
	"""
	# Execute the query
	cursor.execute(sql)
	connection.commit()

	# Print the inserted/updated data for verification


def SaveShip(connection, cursor, data):
	# Use the provided ShipId or generate a new one
	if not data['Ship']['ShipId']:
		data['Ship']['ShipId'] = "SHP" + str(uuid.uuid4()).replace("-", "")
		
	ship_id = data['Ship']['ShipId']

	ship_name = data['Ship']['ShipName']
	ship_type = data['Ship']['ShipType']
	ship_size = data['Ship']['ShipSize']
	home_port_location_id = data['Ship'].get('ShipHomePortLocationId', None)

	# SQL query to insert or update the ship record
	sql = f"""
	INSERT INTO ships (ShipId, ShipName, BuildDate, Notes, ShipType, Size, HomePortLocationId)
	VALUES ('{ship_id}', '{ship_name}', NULL, NULL, '{ship_type}', '{ship_size}', '{home_port_location_id}')
	ON DUPLICATE KEY UPDATE
	ShipName = VALUES(ShipName),
	ShipType = VALUES(ShipType),
	Size = VALUES(Size),
	HomePortLocationId = VALUES(HomePortLocationId);
	"""

	# Execute the query
	cursor.execute(sql)
	connection.commit()

	# Print the inserted/updated data['Ship'] for verification
	return data

def GetShipId(connection, cursor, ShipName):
	# SQL query to find the ShipId based on ShipName
	sql = f"SELECT ShipId FROM ships WHERE ShipName = '{ShipName}'"
	
	# Execute the query
	cursor.execute(sql)
	result = cursor.fetchone()
	
	# Check if a result was found and return the ShipId
	if result:
		return result['ShipId']  # ShipId is in the first column
	else:
		return None  # No matching ShipName found
def parse_inches(inches_str):
	# Split the string by space to handle fractions like '8 1/2'
	parts = inches_str.split()
	if len(parts) == 1:
		# If there's only one part, it's a whole number
		return float(parts[0])
	elif len(parts) == 2:
		# If there are two parts, it's a fraction
		whole_number = float(parts[0])
		numerator, denominator = map(float, parts[1].split('/'))
		return whole_number + (numerator / denominator)
	else:
		# Handle any unexpected cases
		raise ValueError("Invalid inch format")

def height_to_cm(height_feet, height_inches):
	try:
		# Convert feet to float
		height_feet = float(height_feet)
		
		# Parse inches correctly
		height_inches = convert_mixed_number_to_float(height_inches)

		# Convert feet to inches and add the extra inches
		total_inches = (height_feet * 12) + height_inches

		# Convert inches to centimeters
		height_cm = total_inches * 2.54

		# Round to 1 decimal place
		return round(height_cm, 1)

	except ValueError as e:
		return f"Invalid input: {e}"
	
def ParseHumanNames(Name, Role):
	parsed_names = []
	original_name = Name.strip()  # Keep the original value intact

	# Check if there are multiple people listed
	if ' and ' in original_name:
		# Split the names by ' and '
		multiple_names = original_name.split(' and ')
		
		for individual_human in multiple_names:
			# Process each name individually
			if ',' in individual_human:
				# Split by comma for {LastName, FirstName} format
				last_name, first_name = [part.strip() for part in individual_human.split(',', 1)]
			else:
				# Assume {FirstName LastName} format if no comma
				parts = individual_human.split(' ', 1)
				if len(parts) == 2:
					first_name, last_name = parts
				else:
					# Handle edge case where there might be only one name (though unlikely)
					first_name = parts[0]
					last_name = ''

			# Further split the first name into FirstName and MiddleName if it contains a space
			first_name_parts = first_name.split(' ', 1)
			if len(first_name_parts) == 2:
				first_name = first_name_parts[0]
				middle_name = first_name_parts[1]
			else:
				middle_name = ""  # No middle name present

			if (len(first_name) and len(last_name)) or Role=='Enslaved':
				# Append the parsed data for each individual human
				parsed_names.append({
				
					'Original': individual_human.strip(),  # Keep the full original string of each individual human
					'FirstName': first_name,
					'MiddleName': middle_name,
					'LastName': last_name,
					'Role': Role
					
					
				})
	else:
		# Process single human names
		if ',' in original_name:
			# Split by comma for {LastName, FirstName} format
			last_name, first_name = [part.strip() for part in original_name.split(',', 1)]
		else:
			# Assume {FirstName LastName} format if no comma
			parts = original_name.split(' ', 1)
			if len(parts) == 2:
				first_name, last_name = parts
			else:
				# Handle edge case where there might be only one name (though unlikely)
				first_name = parts[0]
				last_name = ''

		# Further split the first name into FirstName and MiddleName if it contains a space
		first_name_parts = first_name.split(' ', 1)
		if len(first_name_parts) == 2:
			first_name = first_name_parts[0]
			middle_name = first_name_parts[1]
		else:
			middle_name = ""  # No middle name present

		# print(Role)
		if (len(first_name) and len(last_name)) or Role=='Enslaved':
			
			# Append the parsed data for the single human
			parsed_names.append({
				'Original': original_name,  # Keep the full original string
				'FirstName': first_name,
				'MiddleName': middle_name,
				'LastName': last_name,
				'Role': Role
			})

	return parsed_names

def ParseDate(ManifestId,MonthDay,Year):


	MonthDay=MonthDay.replace("-","/")
	MonthDay_list = MonthDay.split("/")
	date_string = f"{MonthDay}/{Year}"
	DateOfTransaction={}
	DateOfTransaction['Original']={}
	DateOfTransaction['Original']['MonthDayNorfolk']=MonthDay
	DateOfTransaction['Original']['YearNorfolk']=Year
	
	if Year == "":
		DateOfTransaction['parsed_date'] = None
		DateOfTransaction['DateAccuracy'] = None
		return DateOfTransaction
	elif MonthDay=="":
		date_str= f"xx/xx/{Year}"

		DateOfTransaction['DateAccuracy'] = "Y"  # Indicates that only the year is known
		# Attempt to parse the year only
		try:
			# Extract the year and create a date object with January 1st as a placeholder
			year = Year
			DateOfTransaction['parsed_date'] = datetime.strptime(f"{year}-01-01", "%Y-%m-%d").date()
		except ValueError as e:
			DateOfTransaction['parsed_date'] = None
			DateOfTransaction['DateAccuracy'] = f"ERROR {e}"
			print(f"Error parsing year from date '{date_str}': {e}")

	elif len(MonthDay_list)==1:
		print("ONLY MONTH!")
		date_str= f"{MonthDay}/xx/{Year}"

		DateOfTransaction['DateAccuracy'] = "M"  # Indicates that only the year is known
		# Attempt to parse the year only
		try:
			# Extract the year and create a date object with January 1st as a placeholder
			year = Year
			DateOfTransaction['parsed_date'] = datetime.strptime(f"{year}-{MonthDay}-01", "%Y-%m-%d").date()
		except ValueError as e:
			DateOfTransaction['parsed_date'] = None
			DateOfTransaction['DateAccuracy'] = f"ERROR {e}"
			print(f"Error parsing year from date '{date_str}': {e}")
	else:
		date_str= f"{MonthDay}/{Year}"

		DateOfTransaction['DateAccuracy'] = "D"
		# List of possible date formats
		date_formats = [
			"%Y-%m-%d",  # "1831-03-19"
			"%Y-%m-%dT%H:%M:%S.%fZ",  # "1839-02-05T04:56:02.000Z"
			"%m/%d/%Y"
		]

		# Try to parse the date string with each format
		for fmt in date_formats:
			try:
				# Parse the date and store it in the dictionary as a date object
				DateOfTransaction['parsed_date'] = datetime.strptime(date_str, fmt).date()
				break  # Exit the loop if parsing succeeds
			except ValueError:
				# If the format doesn't match, continue to the next one
				continue
		else:
			# If none of the formats match, store None
			DateOfTransaction['parsed_date'] = None
			DateOfTransaction['DateAccuracy'] = f"ERROR - No matching format"
			print(f"Error parsing date '{date_str}': No matching format found. {ManifestId}")

	return DateOfTransaction


def getLocation(connection, cursor, location_str):
	location_str=location_str.replace(" ","")
	location_str=location_str.replace(",","")
	location_str=location_str.replace(".","")

	if not len(location_str):
		return "None"
	query = f"SELECT LocationId FROM locationaddresses WHERE Address='{location_str}'"
	
	cursor.execute(query)
	result = cursor.fetchone()

	if result:
		return result['LocationId']
	
	else:
		print(location_str)
		print("geocode lookup")
		LocationId=geocode_location(connection, cursor,location_str)
		query = f"insert into locationaddresses(LocationId,Address) values('{LocationId}','{location_str}')"
		cursor.execute(query)
		connection.commit()

		print("LocationId",LocationId)
		return LocationId
	
	
def geocode_location(connection, cursor, address):
	# Perform geocode lookup
	print("Geocode lookup:", address)
	geocode_result = gmaps.geocode(address)
	if geocode_result:
		print("Geocode result found.")
		location_data = geocode_result[0]
		location = location_data['geometry']['location']
		lat, lng = location['lat'], location['lng']
		
		# Extract more detailed location components
		address_components = {comp['types'][0]: comp['long_name'] for comp in location_data['address_components']}
		formatted_address = location_data.get('formatted_address', None)
		city = address_components.get('locality', None)
		county = address_components.get('administrative_area_level_2', None)
		state = address_components.get('administrative_area_level_1', None)
		country = address_components.get('country', None)
		
		# Extract the state abbreviation (short_name)
		state_abbr = None
		country_abbr = None
		for comp in location_data['address_components']:
			if 'administrative_area_level_1' in comp['types']:
				state_abbr = comp['short_name']
			if 'country' in comp['types']:
				country_abbr = comp['short_name']

		location_data = {
			"address": formatted_address,
			"city": city,
			"county": county,
			"state": state,
			"state_abbr": state_abbr,
			"country": country,
			"country_abbr": country_abbr,
			"latitude": lat,
			"longitude": lng
		}
		print(location_data)

		# Step 1: Check if the formatted_address already exists in the locations table
		check_query = "SELECT LocationId FROM locations WHERE Address = %s"
		cursor.execute(check_query, (formatted_address,))
		result = cursor.fetchone()

		if result:
			# Formatted address already exists, return the existing LocationId
			print(f"Address already exists in the database: {formatted_address}")
			return result['LocationId']

		# Step 2: Insert new location
		location_id = "LOC" + str(uuid.uuid4()).replace("-", "")
		insert_query = """
		INSERT INTO locations (LocationId, Address, City, County, State, State_abbr, Country, Latitude, Longitude, DateUpdated)
		VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
		"""
		cursor.execute(insert_query, (
			location_id,
			location_data['address'],
			location_data['city'],
			location_data['county'],
			location_data['state'],
			location_data['state_abbr'],
			location_data['country_abbr'],
			location_data['latitude'],
			location_data['longitude'],
			datetime.now()
		))
		print("Inserted new location into the database.")
		connection.commit()
		return location_id

	return None


def getManifests(cursor):
	sql=f"select distinct * from raw_manifest"
	cursor.execute(sql)
	results=cursor.fetchall()
	
	return results


def SaveManifest( data):
	cursor, connection = Database.ConnectToDatabase()
	# SQL query to insert data into the raw_manifest table using an f-string
	sql = f"""
		INSERT INTO raw_manifest ( Manifest_ID,  Timestamp,  LastName,  FirstNameMiddleName,  Sex,  Age,  Height_feet,  Height_inches,  Color,  OwnersName,  OwnersLocation,  ShippingAgent,  ShippingAgentLocation,  Owner2, Owner2Location, ShipName,  ShipSize,  ShipType,  ShipCaptain,  ShipHomePort, CollectorAgent,  YearNorfolk,  MonthDayNorfolk,   YearNOLA,  MonthDayNOLA,   Notes,  Transcribers,  shipVoyageId,  teamNumber,  ReferenceScan,  SecondReference
		) VALUES ( '{data['Manifest_Id']}',  '{data['Timestamp'].strftime('%Y-%m-%d %H:%M:%S.%f')}',  '{data['LastName']}',  '{data['FirstMiddleName']}',  '{data['Sex']}',  '{data['Age']}',  '{data['Height_feet']}',  '{data['Height_inches']}',  '{data['Color']}',  '{data['OwnerName']}',  '{data['OwnerLocation']}',  '{data['AgentName']}',  '{data['ShippingAgentLocation']}',  '{data['Owner2']}', '{data['Owner2Location']}', '{data['ShipName']}',  '{data['ShipSize']}',  '{data['ShipType']}',  '{data['ShipCaptain']}',  '{data['ShipHomePort']}', 
		
		'{data['NorfolkCollectorName']}',
		'{str(data['YearManifestNorfolk'])}', 
		'{str(data['MonthDayManifestNorfolk'])}', 
		'{str(data['YearNOLA'])}', 
		'{str(data['MonthDayNOLA'])}', 
		'{data['Notes']}',  '{data['Transcribers']}',  '{data['VoyageId']}',  '{data['TeamNumber']}',  '{data['referencefilename']}',  '{data['secondaryreferenceFilename']}'
		) 
		ON DUPLICATE KEY UPDATE  Timestamp = VALUES(Timestamp), LastName = VALUES(LastName), FirstNameMiddleName = VALUES(FirstNameMiddleName), Sex = VALUES(Sex), Age = VALUES(Age), Height_feet = VALUES(Height_feet), Height_inches = VALUES(Height_inches), Color = VALUES(Color), OwnersName = VALUES(OwnersName), OwnersLocation = VALUES(OwnersLocation), ShippingAgent = VALUES(ShippingAgent), ShippingAgentLocation = VALUES(ShippingAgentLocation),Owner2 = VALUES(Owner2), Owner2Location = VALUES(Owner2Location),ShipName = VALUES(ShipName), ShipSize = VALUES(ShipSize), ShipType = VALUES(ShipType), ShipCaptain = VALUES(ShipCaptain), ShipHomePort = VALUES(ShipHomePort), YearNorfolk = VALUES(YearNorfolk), MonthDayNorfolk = VALUES(MonthDayNorfolk), CollectorAgent = VALUES(CollectorAgent), YearNOLA = VALUES(YearNOLA), MonthDayNOLA = VALUES(MonthDayNOLA),Notes = VALUES(Notes), Transcribers = VALUES(Transcribers), shipVoyageId = VALUES(shipVoyageId), teamNumber = VALUES(teamNumber), ReferenceScan = VALUES(ReferenceScan), SecondReference = VALUES(SecondReference)
	"""

	# print(sql)
	# Execute the SQL query
	cursor.execute(sql)
	
	# Commit the transaction
	connection.commit()

	cursor.execute(sql)
	connection.commit()
	cursor.close()
	connection.close()

def DeleteManifests(Manifest_Ids):
	cursor, connection = Database.ConnectToDatabase()
	formatted_ids = ",".join(f"'{Manifest_Id}'" for Manifest_Id in Manifest_Ids)
	sql = f"SELECT * FROM raw_manifest where Manifest_Id not in ({formatted_ids})"
	
	cursor.execute(sql)
	results = cursor.fetchall()
		
	for row in results:
		DeleteManifest(row['Manifest_Id'])
	# return result
	connection.commit()
	cursor.close()
	connection.close()
def DeleteManifest(Manifest_Id):

	cursor, connection = Database.ConnectToDatabase()
	sql = f"delete FROM raw_manifest where Manifest_Id = '{Manifest_Id}'"
	cursor.execute(sql)
	connection.commit()
	cursor.close()
	connection.close()

	
def Get_LastManifest():
	cursor, connection = Database.ConnectToDatabase()

	sql = f"SELECT MAX(Timestamp) as LastTimestamp FROM raw_manifest"
	cursor.execute(sql)
	result = cursor.fetchone()
		
	return result