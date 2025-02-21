import uuid
from _Lib import Database
from _Lib import History
from datetime import datetime, date, timedelta, timezone
import calendar
import traceback
import re


import time

from dateutil import parser
import googlemaps
from collections import Counter
from collections import defaultdict
# import openai
# import pandas as pd
import json
# openai.api_key = ''

gmaps = googlemaps.Client(key='AIzaSyB_a1_JJZBF0g43m9KeKVrSlr7ik6_AN_Y')


def import_NOLA(data,SessionId):
	
	headers = data['Headers']
	rows = data['Data']
	NOLA_IDs = data['NOLA_IDs']
	
	DeleteNolas(NOLA_IDs)
	for row in rows:
		rowData={}
		if isinstance(row, list):
			# Extract specific columns from the row (example)
			rowData['NOLA_ID'] = row[0]
			Timestamp_str = row[1]
			try:
				rowData['Timestamp'] = datetime.strptime(Timestamp_str, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc)
			except ValueError:
				# Handle cases where the date string format might differ
				try:
					rowData['Timestamp'] = datetime.strptime(Timestamp_str, "%Y-%m-%dT%H:%M:%S.%f").replace(tzinfo=timezone.utc)
				except:
					print("Timestamp_str ERROR!",Timestamp_str)
					return False
			rowData['FirstParty'] = row[2].replace("'", "`")
			rowData['LocationFirstParty'] = row[3].replace("'", "`")
			rowData['SecondParty'] = row[4].replace("'", "`")
			rowData['LocationSecondParty'] = row[5].replace("'", "`")
			rowData['TypeOfTransaction'] = row[6].replace("'", "`")
			TransactionDate_str = row[7].replace("'", "`")
			# print("TransactionDate_str",TransactionDate_str)
			# try:
			# 	TransactionDateTime = datetime.strptime(TransactionDate_str, "%Y-%m-%dT%H:%M:%S.%fZ")
			# except ValueError:
			# 	# Handle cases where the date string format might differ
			# 	TransactionDateTime = datetime.strptime(TransactionDate_str, "%Y-%m-%dT%H:%M:%S.%f")
			# TransactionDate_only = TransactionDateTime.date()  # This will give you a date object
			rowData['TransactionDate'] = TransactionDate_str.replace("'", "`")  # Convert back to string if needed
			rowData['act'] = str(row[8]).replace("'", "`")
			rowData['page'] = str(row[9]).replace("'", "`")
			rowData['NotaryPublic'] = row[10].replace("'", "`")
			rowData['volume'] = str(row[12]).replace("'", "`")
			rowData['notes'] = str(row[13]).replace("'", "`")
			rowData['url'] = str(row[14]).replace("'", "`")
			rowData['transcriber_info'] = row[15].replace("'", "`")
			SaveNOLA(rowData)
			


def ProcessNOLA():
	cursor, connection = Database.ConnectToDatabase()
	NOLAs=getNOLAs(cursor)
	cursor.close()
	connection.close()

	
	thedates=[]
	for i, row in enumerate(NOLAs):
		
		cursor, connection = Database.ConnectToDatabase()
		
		# Parse the FirstParty names and store the result back in the dictionary
		NOLAs[i]['DateOfTransaction']=ParseDate(row['DateOfTransaction'], row['NOLA_ID'])
		NOLAs[i]['NOLA_ID']=row['NOLA_ID']
		
		FirstParty = ParseHumanNames(row['FirstParty'], 'FirstParty',NOLAs[i]['DateOfTransaction'])
		NOLAs[i]['FirstParty'] = FirstParty
		NOLAs[i]['FirstParty'][0]['Human']['ResidenceLocationId']=getLocation(connection, cursor, row['LocationFirstParty'])
		
		SecondParty = ParseHumanNames(row['SecondParty'], 'SecondParty',NOLAs[i]['DateOfTransaction'])
		NOLAs[i]['SecondParty'] = SecondParty
		NOLAs[i]['SecondParty'][0]['Human']['ResidenceLocationId']=getLocation(connection, cursor, row['LocationSecondParty'])
		
		NotaryPublic = ParseHumanNames(row['NotaryPublic'], 'NotaryPublic',NOLAs[i]['DateOfTransaction'])
		NOLAs[i]['NotaryPublic'] = NotaryPublic
		NOLAs[i]['NotaryPublic'][0]['Human']['OfficeLocationId']=getLocation(connection, cursor, 'New Orleans, Louisiana')
		
	
		HumanIds=SaveHuman(connection, cursor, NOLAs[i]['FirstParty'])
		for count,HumanId in enumerate(HumanIds):
			NOLAs[i]['FirstParty'][count]['Human']['HumanId']=HumanId

		HumanIds=SaveHuman(connection, cursor, NOLAs[i]['SecondParty'])
		for count,HumanId in enumerate(HumanIds):
			NOLAs[i]['SecondParty'][count]['Human']['HumanId']=HumanId
		
		HumanIds=SaveHuman(connection, cursor, NOLAs[i]['NotaryPublic'])
		for count,HumanId in enumerate(HumanIds):
			NOLAs[i]['NotaryPublic'][count]['Human']['HumanId']=HumanId
		try:
			SaveTransaction(connection, cursor, NOLAs[i])
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

	return str(i+1)

def SaveTransaction(connection, cursor,Transaction):
	FirstPartyId=SaveParty(connection, cursor, Transaction['FirstParty'], 'FirstParty')
	SecondPartyId=SaveParty(connection, cursor, Transaction['SecondParty'], 'SecondParty')
	NotaryHumanId=Transaction['NotaryPublic'][0]['Human']['HumanId']
	date_circa=Transaction['DateOfTransaction']['parsed_date']
	date_accuracy=Transaction['DateOfTransaction']['DateAccuracy']
	Notes=Transaction['Notes']
	Parsed_Notes=Transaction['Parsed_Notes']
	if Parsed_Notes:
		Parsed_Notes=Parsed_Notes.replace("'", "\\'")
	NOLA_ID=Transaction['NOLA_ID']
	Act=Transaction['Act']
	Page=Transaction['Page']
	Volume=Transaction['Volume']
	ReferenceURL=Transaction['ReferenceURL']
	TransactionType=Transaction['TypeOfTransaction']
	transcriber_info=Transaction['NameOfTranscriber']

	sql_query = f"SELECT TransactionId from transactions WHERE FirstPartyId='{FirstPartyId}' and SecondPartyId='{SecondPartyId}' and NotaryHumanId='{NotaryHumanId}'"
	# print(sql_query)
	cursor.execute(sql_query)
	result = cursor.fetchone()

	if not result:
		TransactionId="TRN"+str(uuid.uuid4()).replace("-", "")
		insert_query = f"""
			INSERT into transactions (
				TransactionId, NOLA_ID, date_circa, date_accuracy, FirstPartyId, SecondPartyId, 
				TransactionType, Notes, Parsed_Notes, Act, Page, NotaryHumanId, Volume, URL, Transcriber
			)
			VALUES (
				'{TransactionId}', 
				{f"'{NOLA_ID}'" if NOLA_ID is not None else 'NULL'}, 
				{f"'{date_circa}'" if date_circa is not None else 'NULL'}, 
				{f"'{date_accuracy}'" if date_accuracy is not None else 'NULL'}, 
				{f"'{FirstPartyId}'" if FirstPartyId is not None else 'NULL'}, 
				{f"'{SecondPartyId}'" if SecondPartyId is not None else 'NULL'}, 
				{f"'{TransactionType}'" if TransactionType is not None else 'NULL'}, 
				{f"'{Notes}'" if Notes is not None else 'NULL'}, 
				{f"'{Parsed_Notes}'" if Parsed_Notes is not None else 'NULL'}, 
				{f"'{Act}'" if Act is not None else 'NULL'}, 
				{f"'{Page}'" if Page is not None else 'NULL'}, 
				{f"'{NotaryHumanId}'" if NotaryHumanId is not None else 'NULL'}, 
				{f"'{Volume}'" if Volume is not None else 'NULL'}, 
				{f"'{ReferenceURL}'" if ReferenceURL is not None else 'NULL'}, 
				{f"'{transcriber_info}'" if transcriber_info is not None else 'NULL'}
			)
			"""
		cursor.execute(insert_query)
		# Commit the transaction
		connection.commit()
	else:
		TransactionId=result['TransactionId']

	return TransactionId

def SaveParty(connection, cursor, Party, WhichParty):
	try:
		human_ids = [human['Human']['HumanId'] for human in Party]
	except KeyError:
		# Return None if 'HumanId' is not found
		print("KeyError: 'HumanId' not found in one of the entries")
		return None
	
	human_id_count = Counter(human_ids)
	human_ids_list = list(human_id_count.keys())
	human_ids_str = ', '.join(f"'{human_id}'" for human_id in human_ids_list)

	sql_query = f"SELECT PartyId FROM partyhumans WHERE HumanId IN ({human_ids_str}) GROUP BY PartyId HAVING COUNT(DISTINCT HumanId) = {len(human_ids_list)};"
	cursor.execute(sql_query)
	result = cursor.fetchone()
	
	if not result:
		# No existing party found, create a new PartyId
		PartyId = "PRT" + str(uuid.uuid4()).replace("-", "")
		insert_query = f"INSERT INTO parties (PartyId, WhichParty) VALUES ('{PartyId}', '{WhichParty}');"
		cursor.execute(insert_query)
		connection.commit()
		
		for human_id in human_ids_list:
			insert_query = f"INSERT INTO partyhumans (PartyId, HumanId) VALUES ('{PartyId}', '{human_id}');"
			cursor.execute(insert_query)

		# Commit the transaction
		connection.commit()
	else:
		PartyId = result['PartyId']
	
	# Return the PartyId (either new or existing)
	return PartyId


def SaveHuman(connection, cursor, humans):
	cursor, connection = Database.ConnectToDatabase()
	HumanIds=[]
	for human in humans:
		human=human['Human']
		if len(human['FirstName']) or len(human['LastName']):
			# Using parameterized query to handle special characters
			sql = f"SELECT HumanId from humans WHERE FirstName = '{human['FirstName']}' AND LastName = '{human['LastName']}'"
			cursor.execute(sql)
			result = cursor.fetchone()
			
			if result:
				HumanId=result['HumanId']
				# If a row exists, update it
				update_query = f"""
				update humans
				SET FirstName = '{human['FirstName']}', MiddleName = '{human['MiddleName']}', LastName = '{human['LastName']}'
				WHERE HumanId = '{HumanId}'
				"""
				cursor.execute(update_query)
				connection.commit()
			else:
				# If no row exists, insert a new row with a unique HumanId
				HumanId = "HUM"+str(uuid.uuid4()).replace("-", "")
				insert_query = f"""
				INSERT into humans (HumanId, FirstName, MiddleName, LastName)
				VALUES ('{HumanId}', '{human['FirstName']}', '{human['MiddleName']}', '{human['LastName']}')
				"""
				cursor.execute(insert_query)
				connection.commit()
			HumanIds.append(HumanId)

			insert_role = f"""
				INSERT into humanroles (HumanId, RoleId, date_circa, date_accuracy)
				VALUES ('{HumanId}', '{human['Role']}', 
						{f"'{human['date_circa']}'" if human['date_circa'] is not None else 'NULL'}, 
						{f"'{human['date_accuracy']}'" if human['date_accuracy'] is not None else 'NULL'})
				ON DUPLICATE KEY UPDATE 
					HumanId=VALUES(HumanId), 
					RoleId=VALUES(RoleId), 
					date_circa=VALUES(date_circa), 
					date_accuracy=VALUES(date_accuracy)
				"""
			cursor.execute(insert_role)
			connection.commit()

			if "ResidenceLocationId" in human:
				insert_role = f"""
					INSERT into humanlocations (HumanId, LocationId, date_circa, date_accuracy, LocationType)
					VALUES (
						'{HumanId}', 
						{f"'{human['ResidenceLocationId']}'" if human.get('ResidenceLocationId') is not None else 'NULL'}, 
						{f"'{human['date_circa']}'" if human['date_circa'] is not None else 'NULL'}, 
						{f"'{human['date_accuracy']}'" if human['date_accuracy'] is not None else 'NULL'}, 
						'Residence'
					)
					ON DUPLICATE KEY UPDATE 
						HumanId=VALUES(HumanId), 
						LocationId=VALUES(LocationId), 
						date_circa=VALUES(date_circa), 
						date_accuracy=VALUES(date_accuracy), 
						LocationType=VALUES(LocationType)
					"""
				cursor.execute(insert_role)
				connection.commit()

			if "OfficeLocationId" in human:
				insert_role = f"""
					INSERT into humanlocations (HumanId, LocationId, date_circa, date_accuracy, LocationType)
					VALUES (
						'{HumanId}', 
						{f"'{human['OfficeLocationId']}'" if human.get('OfficeLocationId') is not None else 'NULL'}, 
						{f"'{human['date_circa']}'" if human.get('date_circa') is not None else 'NULL'}, 
						{f"'{human['date_accuracy']}'" if human.get('date_accuracy') is not None else 'NULL'}, 
						'Notary Office'
					)
					ON DUPLICATE KEY UPDATE 
						HumanId=VALUES(HumanId), 
						LocationId=VALUES(LocationId), 
						date_circa=VALUES(date_circa), 
						date_accuracy=VALUES(date_accuracy), 
						LocationType=VALUES(LocationType)
					"""
				cursor.execute(insert_role)
				connection.commit()


	return HumanIds

def ParseDate(date_str, NOLA_ID):
	DateOfTransaction = {}
	DateOfTransaction['Original'] = date_str

	# Check for "xx-xx" pattern indicating incomplete date information
	
	if DateOfTransaction['Original'] == "":
		DateOfTransaction['parsed_date'] = None
		DateOfTransaction['DateAccuracy'] = None
		
	elif "xx-xx" in date_str:
		DateOfTransaction['DateAccuracy'] = "Y"  # Indicates that only the year is known
		# Attempt to parse the year only
		try:
			# Extract the year and create a date object with January 1st as a placeholder
			year = date_str.split("-")[0]
			DateOfTransaction['parsed_date'] = datetime.strptime(f"{year}-01-01", "%Y-%m-%d").date()
		except ValueError as e:
			DateOfTransaction['parsed_date'] = None
			DateOfTransaction['DateAccuracy'] = f"ERROR {e}"
			print(f"Error parsing year from date '{date_str}': {e}")
	elif "-xx" in date_str:
		DateOfTransaction['DateAccuracy'] = "M"  # Indicates that only the year is known
		# Attempt to parse the year only
		try:
			# Extract the year and create a date object with January 1st as a placeholder
			year = date_str.split("-")[0]
			month = date_str.split("-")[1]
			DateOfTransaction['parsed_date'] = datetime.strptime(f"{year}-{month}-01", "%Y-%m-%d").date()
		except ValueError as e:
			DateOfTransaction['parsed_date'] = None
			DateOfTransaction['DateAccuracy'] = f"ERROR {e}"
			print(f"Error parsing year from date '{date_str}': {e}")
	else:
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
			print(f"Error parsing date '{date_str}': No matching format found. {NOLA_ID}")




	return DateOfTransaction

	
	
def getLocation(connection, cursor, location_str):
	location_str=location_str.replace(" ","")
	location_str=location_str.replace(",","")
	location_str=location_str.replace(".","")

	if not len(location_str):
		return "None"
	query = f"SELECT LocationId from locationaddresses WHERE Address='{location_str}'"
	
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
	print(result)






	return None


	city, state, full_address = parse_location(location_str)
	# Attempt to find the location in the database
	print(location_str)
	query = f"SELECT State_abbr from locations WHERE (State = '{state}' or  State_abbr = '{state}')"
	print(query)
	cursor.execute(query)
	result = cursor.fetchone()
	if result:
		state_abbr=result["State_abbr"]
	else:
		state_abbr=None

	
	if city and state_abbr:
		parsed_location_str=location_str.replace(state, state_abbr)
		print("parsed_location_strparsed_location_str",parsed_location_str)
		parsed_location_str+= ", USA"
		query = f"SELECT LocationId from locations WHERE Address='{parsed_location_str}'"
		
		cursor.execute(query)
		result = cursor.fetchone()
		if result:
			print("resultresult",result)
			return result['LocationId']
		else:
			LocationId=geocode_location(connection, cursor,location_str)
			print("LocationId",LocationId)
			return LocationId
	
	elif len(location_str) >0 :
		LocationId=geocode_location(connection, cursor,location_str)
		print("LocationId",LocationId)
		return LocationId
	else:
		print("NO ADDRESS!")
		return None
		
		
	
def parse_location(location_str):
	# Try to split by city and state
	if ',' in location_str:
		parts = location_str.split(',')
		if len(parts) == 2:
			city = parts[0].strip()
			state = parts[1].strip()
			return city, state, None  # No full address
	# If there's no comma or more complex address, return full address
	return None, None, location_str.strip()


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
		check_query = "SELECT LocationId from locations WHERE Address = %s"
		cursor.execute(check_query, (formatted_address,))
		result = cursor.fetchone()

		if result:
			# Formatted address already exists, return the existing LocationId
			print(f"Address already exists in the database: {formatted_address}")
			return result['LocationId']

		# Step 2: Insert new location
		location_id = "LOC" + str(uuid.uuid4()).replace("-", "")
		insert_query = """
		INSERT into locations (LocationId, Address, City, County, State, State_abbr, Country, Latitude, Longitude, DateUpdated)
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



def ParseHumanNames(Name, Role,DateOfTransaction):
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
				middle_name = ''  # No middle name present

			# Append the parsed data for each individual human
			parsed_names.append({
				'Human': {
					'Original': individual_human.strip(),  # Keep the full original string of each individual human
					'FirstName': first_name,
					'MiddleName': middle_name,
					'LastName': last_name,
					'Role': Role,
					'date_circa': DateOfTransaction['parsed_date'],
					'date_accuracy': DateOfTransaction['DateAccuracy'],
					'originalDate':DateOfTransaction['Original']
				}
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

		# Append the parsed data for the single human
		parsed_names.append({
			'Human': {
				'Original': original_name,  # Keep the full original string
				'FirstName': first_name,
				'MiddleName': middle_name,
				'LastName': last_name,
				'Role': Role,
				'date_circa': DateOfTransaction['parsed_date'],
				'date_accuracy': DateOfTransaction['DateAccuracy'],
				'originalDate':DateOfTransaction['Original']
			}
		})

	return parsed_names


def getNOLAs(cursor):
	sql=f"select distinct * from raw_nola"
	cursor.execute(sql)
	results=cursor.fetchall()
	
	return results







# def SaveParties(Parties):
# 	for party in Parties:
# 		first_name = party['Human']['FirstName']
# 		middle_name = party['Human']['MiddleName']
# 		last_name = party['Human']['LastName']
# 		date_circa =party['Human']['date_circa']
# 		date_accuracy =party['Human']['date_accuracy']

# 		human_id = insert_or_update_human(first_name, middle_name,last_name)
# 		insert_role_for_human(human_id, party['Human']['Role'])
# 		location_str = "New Orleans, Louisiana"  # Example location string
# 		location_id = insert_or_update_location(location_str)
# 		insert_human_location(human_id, location_id,date_circa, date_accuracy )


def DeleteNolas(NOLA_IDs):
	cursor, connection = Database.ConnectToDatabase()
	formatted_ids = ",".join(f"'{nola_id}'" for nola_id in NOLA_IDs)
	sql = f"SELECT * FROM raw_nola where NOLA_ID not in ({formatted_ids})"
	
	cursor.execute(sql)
	results = cursor.fetchall()
		
	for row in results:
		DeleteNOLA(row['NOLA_ID'])
	# return result
	connection.commit()
	cursor.close()
	connection.close()

def DeleteNOLA(NOLA_ID):
	cursor, connection = Database.ConnectToDatabase()
	sql = f"delete FROM raw_nola where NOLA_ID = '{NOLA_ID}'"
	cursor.execute(sql)
	connection.commit()
	cursor.close()
	connection.close()

def Get_LastNOLA():
	cursor, connection = Database.ConnectToDatabase()

	sql = f"SELECT CONVERT_TZ(MAX(Timestamp), @@session.time_zone, '+00:00') as LastTimestamp FROM raw_nola"
	cursor.execute(sql)
	result = cursor.fetchone()
		
	return result


def SaveNOLA(data):
	cursor, connection = Database.ConnectToDatabase()
	try:
		insert_query = f"""
			INSERT INTO raw_nola 
			(NOLA_ID, Timestamp, FirstParty, LocationFirstParty, SecondParty, LocationSecondParty, TypeOfTransaction, DateOfTransaction, Act, Page, NotaryPublic, Volume, Notes, ReferenceURL, NameOfTranscriber)
			VALUES (
				'{data['NOLA_ID']}', 
				'{data['Timestamp']}', 
				'{data['FirstParty']}', 
				'{data['LocationFirstParty']}', 
				'{data['SecondParty']}', 
				'{data['LocationSecondParty']}', 
				'{data['TypeOfTransaction']}', 
				'{data['TransactionDate']}', 
				'{data['act']}', 
				'{data['page']}', 
				'{data['NotaryPublic']}', 
				'{data['volume']}', 
				'{data['notes']}', 
				'{data['url']}', 
				'{data['transcriber_info']}'
			)
			ON DUPLICATE KEY UPDATE 
				Timestamp = VALUES(Timestamp),
				FirstParty = VALUES(FirstParty),
				LocationFirstParty = VALUES(LocationFirstParty),
				SecondParty = VALUES(SecondParty),
				LocationSecondParty = VALUES(LocationSecondParty),
				TypeOfTransaction = VALUES(TypeOfTransaction),
				DateOfTransaction = VALUES(DateOfTransaction),
				Act = VALUES(Act),
				Page = VALUES(Page),
				NotaryPublic = VALUES(NotaryPublic),
				Volume = VALUES(Volume),
				Notes = VALUES(Notes),
				ReferenceURL = VALUES(ReferenceURL),
				NameOfTranscriber = VALUES(NameOfTranscriber);
		"""
		
		cursor.execute(insert_query)
		connection.commit()
		cursor.close()
		connection.close()
	except:
		print(insert_query)
		raise "break?"





def parse_date(date_str):
	try:
		# Try to parse the date and return only the date part (year, month, day)
		date_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
		return date_obj.strftime("%Y-%m-%d")  # Format the date as YYYY-MM-DD
	except ValueError:
		# If parsing fails, return NULL
		return None

# Parse the date


def SaveTimeLine(HumanId, LocationId, DateThere):
	cursor, connection = Database.ConnectToDatabase()
	dateThere_dt = parse_date(DateThere)
	insert_TimeLine = """
	INSERT into humantimeline (HumanId, LocationId, dateThere_s, dateThere_dt)
	VALUES (%s, %s, %s, %s)
	ON DUPLICATE KEY update humanId=VALUES(HumanId), LocationId=VALUES(LocationId), dateThere_s=VALUES(dateThere_s), dateThere_dt=VALUES(dateThere_dt)
	"""
	cursor.execute(insert_TimeLine, (HumanId, LocationId, DateThere, dateThere_dt))
	connection.commit()


def Fix_Locations():
	
	cursor, connection = Database.ConnectToDatabase()

	query = """
	SELECT Address, MIN(LocationId) as MinLocationId
	from locations
	GROUP BY Address
	HAVING COUNT(*) > 1
	"""

	cursor.execute(query)
	duplicates = cursor.fetchall()

	# Step 2: update locationIds in locationaddresses table
	for row in duplicates:
		# Get all LocationIds associated with this Address
		query = f"SELECT LocationId from locations WHERE Address = '{row['Address']}'"
		print(query)
		cursor.execute(query)
		location_ids = cursor.fetchall()
		# For each LocationId (except the one to keep), update the locationaddresses table
		for (location_id,) in location_ids:
			if location_id != row['MinLocationId']:
				update_query = f"""
				update locationaddresses
				SET LocationId = '{row['MinLocationId']}'
				WHERE LocationId = '{location_id}' AND Address = '{row['Address']}'
				"""
				print(update_query)
				cursor.execute(update_query)
				connection.commit()

	# Step 3: Optionally, remove duplicate rows in the locations table (except the one to keep)
	for row in duplicates:
		delete_query = f"""
		DELETE from locations WHERE Address = '{row['Address']}' AND LocationId != '{row['MinLocationId']}'
		"""
		print(delete_query)
		cursor.execute(delete_query)
		connection.commit()

	# Close the connection
	cursor.close()
	connection.close()
	return "hello world"

import json

def GPTBatch():
	cursor, connection = Database.ConnectToDatabase()
	sql = "SELECT NOLA_ID, Notes FROM raw_nola WHERE Notes <>'' and Parsed_Notes IS NULL LIMIT 3000"
	print(sql)
	cursor.execute(sql)
	results = cursor.fetchall()
	
	# Initialize an empty string to hold all JSON data
	request_json = ""
	
	for row in results:
		# row[0] is NOLA_ID, row[1] is Notes
		request_json += GPTRequest(row['NOLA_ID'], row['Notes'])+ '\n'
		
	# # Write all the data to the file once
	file_name = 'gpt_requests.jsonl'
	with open(file_name, 'w') as file:
		file.write(request_json)
	return "done"

def GPTRequest(custom_id, user_content):
	request = {
		"custom_id": custom_id,
		"method": "POST",
		"url": "/v1/chat/completions",
		"body": {
			"model": "gpt-3.5-turbo",
			"messages": [
				{
					"role": "system",
					"content": (
						"Convert the following text into a JSON object: Extract information related to these keys if present: "
						"- quantity of slaves, seller, buyer, buyer_status (e.g., 'free woman of color'), seller_status, price, "
						"currency, location (venue, address), individual (name, skin color, age, status, origin (city, state), family relationships), "
						"previous_owner, percentage accuracy. Your task is to generate a concise JSON object that only includes relevant data explicitly mentioned in the text. "
						"Avoid including any unnecessary or placeholder information. General rules: - Only include keys that have meaningful, non-empty values. "
						"Omit any key or object with empty or undefined values, including nested keys. REMOVE all keys and values that have empty, undefined, unknown or '' values. "
						"REMOVE nested keys that have no child keys."
						"REMOVE excess whitespace from the json results"
						"If you see additional data that is not represented in the list of columns above take an educated guess at the key names and values"
					)
				},
				{
					"role": "user",
					"content": user_content
				}
			],
			"max_tokens": 200
		}
	}
	
	return json.dumps(request, separators=(',', ':'))


def GPTSave():
	file_name="C:\\Apache24\\htdocs\\personalProjects\\SoldDownTheRiver\\Server\\batch_66ff8f8a2ae08190b63f2ee59335da87_output.jsonl"

	cursor, connection = Database.ConnectToDatabase()
	
	with open(file_name, 'r') as file:
		for line in file:
			data = json.loads(line)
			custom_id = data['custom_id']
			message_content = data['response']['body']['choices'][0]['message']['content']
			
			# Verify if message_content is valid JSON
			try:
				parsed_content = json.loads(message_content)  # Try to parse message_content
			except json.JSONDecodeError as json_err:
				print(f"Invalid JSON in message_content for NOLA_ID '{custom_id}': {json_err}")
				continue  # Skip this entry if invalid JSON is found
			
			sql = f"UPDATE raw_nola SET Parsed_Notes='{message_content}' WHERE NOLA_ID='{custom_id}'"
			
			try:
				# Execute SQL and commit
				cursor.execute(sql)
				connection.commit()
				print(f"Successfully updated NOLA_ID '{custom_id}' with parsed notes.")
			except Exception as e:
				# Handle any errors during SQL execution
				print(f"Error executing SQL for NOLA_ID '{custom_id}': {e}")
				message_content_escaped = message_content.replace("'", "''")
				sql = f"UPDATE raw_nola SET Parsed_Notes='error', Error_Notes='{message_content_escaped}' WHERE NOLA_ID='{custom_id}'"
				cursor.execute(sql)
				connection.commit()
			
			
	
	return "saved"



def GPTNotes():
	cursor, connection = Database.ConnectToDatabase()
	sql = f"SELECT NOLA_ID,Notes FROM raw_nola where Parsed_Notes is null limit 1"
	print(sql)
	cursor.execute(sql)
	results = cursor.fetchall()
		
	response=[]
	for i,row in enumerate(results):

		print(i)
		# prompt = f"Convert the following text into a JSON object:\n Text: '{row['Notes']}'\n Please extract and format the data as JSON with the following keys: : quantity of slaves, seller, buyer, buyer_status (ex: 'free woman of color'), seller_status, price, currency, location (venue, address), individual (name, skin color, age, status, origin (city, state)), previous_owner and percentage accuracy of translation. ONLY add the keys and values if the text has those keys in it. if any of the keys in the list are not in the text, don't add the keys with empty values to the json packet. same thing if the sub keys are empty, don't add the parent keys. For example if there is no city and state, don't include an orgin with empty city and state values. If there is additional keys in the text not in the list of keys, do your best to add it to the output. "
		# prompt = (prompt)
		prompt = f"""
		Convert the following text into a JSON object:
		Text: '{row['Notes']}'

		Extract information related to these keys if present:
		- quantity of slaves, seller, buyer, buyer_status (e.g., 'free woman of color'), seller_status, price, currency, location (venue, address), individual (name, skin color, age, status, origin (city, state), family relationships), previous_owner, percentage accuracy.
		Your task is to generate a concise JSON object that only includes relevant data explicitly mentioned in the text. Avoid including any unnecessary or placeholder information.
		
		General rules:
		- Only include keys that have meaningful, non-empty values.
		- Omit any key or object with empty or undefined values, including nested keys.
		REMOVE all keys and values that have empty, undefined, unknown or "" values.
		REMOVE nested keys that have no child keys
		"""

		
		print("------")
		print(row['Notes'])
		JSONNotes = generate_text_with_openai(prompt)
		
		note={}
		note['orig_notes']=row['Notes']
		note['parsed_notes']=JSONNotes
		response.append(note)
		print("------")
		json_string = json.dumps(JSONNotes)

		# Replace single quotes in the JSON string to escape them for SQL
		escaped_json_string = json_string.replace("'", "''")
		sql = f"update raw_nola set Parsed_Notes='{escaped_json_string}' where NOLA_ID='{row['NOLA_ID']}'"

		# return sql
		cursor.execute(sql)
		connection.commit()
		# time.sleep(10)
	
	cursor.close()
	connection.close()
	response="<meta http-equiv='refresh' content='60 '>"
	return response

# def StripWhitespaceFromParsedNotes():
# 	cursor, connection = Database.ConnectToDatabase()

# 	# Query to fetch the relevant rows
# 	sql_query = "SELECT NOLA_ID, Parsed_Notes FROM raw_nola WHERE Parsed_Notes IS NOT NULL"
# 	cursor.execute(sql_query)
# 	result = cursor.fetchall()

# 	# Convert result to a pandas DataFrame
# 	df = pd.DataFrame(result)

# 	# Function to clean JSON
# 	def clean_json(json_string):
# 		try:
# 			# Parse the JSON and dump it back without whitespace
# 			parsed = json.loads(json_string)
# 			return json.dumps(parsed, separators=(',', ':'))
# 		except json.JSONDecodeError:
# 			return json_string  # Return as is if it's not valid JSON

# 	# Apply the cleaning function if the DataFrame is not empty
# 	if not df.empty:
# 		df['Parsed_Notes'] = df['Parsed_Notes'].apply(clean_json)

# 		# Update the cleaned data back into the database
# 		for index, row in df.iterrows():
# 			update_query = "UPDATE raw_nola SET Parsed_Notes = %s WHERE NOLA_ID = %s"
			
# 			cursor.execute(update_query, (row['Parsed_Notes'], row['NOLA_ID']))

# 		# Commit the changes
# 		connection.commit()

# 	# Close the cursor and connection
# 	cursor.close()
# 	connection.close()
# 	return result






def generate_text_with_openai(prompt, initial_max_tokens=400, max_retries=5):
	max_tokens = initial_max_tokens
	
	for attempt in range(max_retries):
		# Ensure max_tokens doesn't exceed 4096
		if max_tokens > 4096:
			max_tokens = 4096
		print("OPEN AI turned off")
		# try:
		# 	response = openai.ChatCompletion.create(
		# 		model="gpt-4o",
		# 		messages=[
		# 			{"role": "system", "content": "You are a helpful assistant."},
		# 			{"role": "user", "content": prompt}
		# 		],
		# 		max_tokens=max_tokens,
		# 		temperature=0.7
		# 	)
			
		# 	generated_text = response['choices'][0]['message']['content'].strip()
		# 	print(generated_text)
		# 	generated_text = generated_text.replace("```json", "")
		# 	generated_text = generated_text.replace("```", "")
			
		# 	try:
		# 		data = json.loads(generated_text)
		# 		# If parsing is successful, return the data
		# 		return data
		# 	except json.JSONDecodeError as e:
		# 		print(f"Attempt {attempt + 1} with max_tokens={max_tokens}")
		# 		print(f"JSON Decode Error: {e}. Retrying with larger max_tokens.")
		
		# except openai.error.RateLimitError as e:
		# 	print(f"Rate limit error: {e}")
		# 	print(f"Rate limit reached. Waiting before retrying... (Attempt {attempt + 1})")
		# 	time.sleep(20)  # Wait for 20 seconds before retrying

		# # Double the max_tokens for the next attempt
		# max_tokens *= 2
		# if max_tokens >= 4096:
		# 	print("Max tokens reached the limit of 4096, stopping further attempts.")
		# 	break
	
	# If no valid JSON is returned after all retries
	return "Failed to generate a valid JSON response after multiple attempts."
	raise ValueError("Failed to generate a valid JSON response after multiple attempts.")




	return "from gpt "


def replace_string_in_json():
	
	replaceThis="skin color"
	withThis="skin_color"

	cursor, connection = Database.ConnectToDatabase()

	# Query to select rows containing 'skin color' in Parsed_Notes
	select_query = f"""
	SELECT transactionId, Parsed_Notes
	FROM transactions
	WHERE Parsed_Notes LIKE '%{replaceThis}%'
	"""
	cursor.execute(select_query)
	rows = cursor.fetchall()

	# Process each row and replace 'skin color' with 'skin_color'
	for row in rows:
		transaction_id = row['transactionId']
		parsed_notes = row['Parsed_Notes']
		
		# Replace 'skin color' with 'skin_color' in the JSON
		try:


			modified_notes = parsed_notes.replace(replaceThis, withThis)

			
			update_query = f"""
			UPDATE transactions
			SET Parsed_Notes = '{modified_notes}'
			WHERE transactionId = '{transaction_id}'
			"""
			print(parsed_notes)
			print(update_query)
			cursor.execute(update_query)
			connection.commit()
			print(f"Updated transactionId {transaction_id}")

		except json.JSONDecodeError as e:
			print(f"Error decoding JSON for transactionId {transaction_id}: {e}")

	cursor.close()
	connection.close()

	return "done"




# def process_row(parsed_data, row, cursor, key_count):
# 	print(parsed_data)
# 	transaction_id = row['TransactionId']
# 	date_circa = row['date_circa']
	
# 	# Convert date_circa to a datetime object if it’s a string
# 	if isinstance(date_circa, str):
# 		try:
# 			transaction_date = datetime.strptime(date_circa, "%Y-%m-%d")
# 		except ValueError:
# 			print(f"Invalid date format for TransactionId {transaction_id}")
# 			transaction_date = None
# 	else:
# 		transaction_date = date_circa

# 	# Hardcoded keys for processed status
# 	processed_keys = {
# 		"price": False,
# 		"individuals.name": False,
# 		"individuals.age": False,
# 		"individuals.skin_color": False,
# 		"individuals.price": False,
# 		"individuals.origin.city": False,
# 	}

# 	# Helper function to process individual records
# 	def process_individual(transaction_id,individual, transaction_id):
# 		name = individual.get('name')
# 		age = individual.get('age')
# 		skin_color = individual.get('skin_color')
# 		physical_features = individual.get('physical_features')
# 		price = individual.get('price')
# 		originCity = individual.get('origin', {}).get('city') if 'origin' in individual else None

# 		if name:
# 			# Step 1: Check if the human record exists using a JOIN with transactionhumans
# 			query = (
# 				f"SELECT h.HumanId "
# 				f"from humans h "
# 				f"JOIN transactionhumans th ON h.HumanId = th.HumanId "
# 				f"WHERE h.FirstName = '{name}' AND th.TransactionId = '{transaction_id}'"
# 			)
# 			cursor.execute(query)
# 			human_record = cursor.fetchone()
			
# 			if human_record:
# 				HumanId = human_record['HumanId']
# 				query = (
# 					f"update humans SET FirstName = '{name}',physical_features='{physical_features}', Color = '{skin_color}', originCity='{originCity}', DateUpdated = '{datetime.now()}' "
# 					f"WHERE HumanId = '{HumanId}'"
# 				)
# 				cursor.execute(query)
# 			else:
# 				# Step 2: Insert new human record
# 				HumanId = "HUM" + str(uuid.uuid4()).replace("-", "")
# 				if age is not None and transaction_date:
# 					birth_date = transaction_date.replace(year=transaction_date.year - age)
# 				else:
# 					birth_date = None
# 				query = (
# 					f"INSERT into humans (HumanId, FirstName, Color, physical_features, BirthDate, BirthDateAccuracy, originCity, DateUpdated) "
# 					f"VALUES ('{HumanId}', '{name}', '{skin_color}', '{physical_features}','{birth_date}', 'Y', '{originCity}', '{datetime.now()}')"
# 				)
# 				cursor.execute(query)
# 				print(f"New human record created for {name} (HumanId: {HumanId}).")
			
# 			# Update processed status for individual fields
# 			processed_keys["individuals.name"] = True
# 			processed_keys["individuals.age"] = age is not None
# 			processed_keys["individuals.skin_color"] = skin_color is not None
# 			processed_keys["individuals.physical_features"] = physical_features is not None
# 			processed_keys["individuals.origin.city"] = originCity is not None

# 			# Step 3: Insert into transactionhumans table
# 			price_value = 'NULL' if price is None else price
# 			query = (
# 				f"INSERT into transactionhumans (TransactionId, HumanId, Notes, Price) "
# 				f"VALUES ('{transaction_id}', '{HumanId}', '{json.dumps(individual)}', {price_value}) "
# 				f"ON DUPLICATE KEY update transactionId = TransactionId"
# 			)
# 			cursor.execute(query)
# 			processed_keys["individuals.price"] = price is not None

# 	# Process the main JSON data
# 	if 'price' in parsed_data:
# 		price = parsed_data['price']
# 		if isinstance(price, (int, float)) and price > 0:
# 			query = f"update transactions SET TotalPrice = {price} WHERE TransactionId = '{transaction_id}'"
# 			cursor.execute(query)
# 			processed_keys["price"] = True
# 			print("price: Processed")




# 	# Process 'individuals' (list) or 'individual' (single entry)
# 	if 'individuals' in parsed_data and isinstance(parsed_data['individuals'], list):
# 		for individual in parsed_data['individuals']:
# 			process_individual(individual, transaction_id)
# 	elif 'individual' in parsed_data and isinstance(parsed_data['individual'], dict):
# 		process_individual(parsed_data['individual'], transaction_id)

# 	# Output the final processed status of each hardcoded key
# 	print("Processed Keys Status:")
# 	for key, status in processed_keys.items():
# 		print(f"{key}: {'Processed' if status else 'Not Processed'}")



def transform_json_packet(packet):
	# Initialize the transformed packet
	transformed_packet = {}

	# Special handling for 'individual' to make it a list of 'individuals' if needed
	if 'individual' in packet and isinstance(packet['individual'], dict):
		packet['individuals'] = [packet.pop('individual')]

	# print("packet",packet)
	# Iterate over the items in the packet
	for key, value in packet.items():
		# Handle lists and transform each dictionary within them
		if isinstance(value, list):
			transformed_packet[key] = [transform_json_packet(item) if isinstance(item, dict) else item for item in value]

		# Special handling for 'location' if it has nested fields
		elif key == 'location' and isinstance(value, dict):
			# Recursively transform nested dictionary within 'location'
			transformed_packet[key] = transform_json_packet(value)

		# Recursively transform nested dictionaries (e.g., 'origin')
		elif isinstance(value, dict):
			transformed_packet[key] = transform_json_packet(value)
		
		# Otherwise, wrap simple values in 'data' and 'status'
		else:
			transformed_packet[key] = {
				'data': value,
				'status': 0
			}

	return transformed_packet

issues=[]
def display_json_paths(packet, prefix=''):
	for key, value in packet.items():
		# Construct the full path for the current key
		full_path = f"{prefix}.{key}" if prefix else key
		
		if isinstance(value, dict) and 'data' in value and 'status' in value:
			# Display the full path along with data and status
			# print(f"Path: {full_path}, Data: {value['data']}, Status: {value['status']}")
			if value['status']==0:
				issues.append(full_path)
		elif isinstance(value, dict):
			# Recursively call the function for nested dictionaries
			display_json_paths(value, full_path)
		
		elif isinstance(value, list):
			# Loop through list items and process each item if it's a dictionary
			for index, item in enumerate(value):
				if isinstance(item, dict):
					display_json_paths(item, f"{full_path}[{index}]")

def update_status(packet, full_path, status):
	# Split the full path by dots and brackets to get each part of the path
	keys = full_path.replace(']', '').replace('[', '.').split('.')
	
	current = packet
	for i, key in enumerate(keys):
		if key.isdigit():  # Check if the key represents a list index
			index = int(key)
			if isinstance(current, list):
				# Expand the list if needed
				while len(current) <= index:
					current.append({})
				current = current[index]
			else:
				print(f"Expected list at '{key}', got {type(current).__name__}")
				return
		
		else:  # Handle dictionary keys
			if isinstance(current, dict):
				# Create a nested dictionary if the key does not exist
				if key not in current:
					current[key] = {}
				current = current[key]
			else:
				print(f"Expected dictionary at '{key}', got {type(current).__name__}")
				return

		# Set a status field for each nested level along the path
		if isinstance(current, dict) and 'status' not in current:
			current['status'] = status

	# Set status for the final target element in the path
	if isinstance(current, dict):
		current['status'] = status
	else:
		print(f"Cannot set status for non-dictionary at path '{full_path}'")

def replace_none_to_null(query):
	# Replace occurrences of 'None' with 'NULL' in the query string
	query = query.replace("'None'", "NULL")
	query = query.replace("=NULL", " IS NULL")
	query = query.replace("= NULL", " IS NULL")
	return query

def splitName(fullName):
	# Split the full name by spaces
	nameParts = fullName.split()

	# Assign parts to FirstName, MiddleName, and LastName
	if len(nameParts) == 1:
		firstName = nameParts[0]
		middleName = None
		lastName = None
	elif len(nameParts) == 2:
		firstName = nameParts[0]
		middleName = None
		lastName = nameParts[1]
	elif len(nameParts) >= 3:
		firstName = nameParts[0]
		middleName = " ".join(nameParts[1:-1])  # Join middle parts if there are more than one
		lastName = nameParts[-1]
	else:
		firstName=None
		middleName=None
		lastName=None

	return firstName, middleName, lastName
def calculateBirthDate(currentDate, age):
	if not age or not currentDate:
		return None
	
	# Extract the year, month, and day from the current date object
	currentYear = currentDate.year
	currentMonth = currentDate.month
	currentDay = currentDate.day
	
	# Calculate the birth year by subtracting the age from the current year
	birthYear = currentYear - age
	
	# Ensure the day is valid for the month and year
	last_day_of_month = calendar.monthrange(birthYear, currentMonth)[1]
	validDay = min(currentDay, last_day_of_month)
	
	# Create the birth date using the calculated birth year and adjusted day
	birthDate = datetime(birthYear, currentMonth, validDay).date()
	
	return birthDate

def process_individual(transaction,packet, individual, index, individualNAME):
	# print(individual)
	cursor, connection = Database.ConnectToDatabase()
	# Set variables for each field, handling synonyms and existence checks
	name = individual.get('name', {}).get('data') if 'name' in individual else None
	# aliases = individual.get('aliases', {}).get('data') if 'aliases' in individual else None
	aliases = ', '.join(individual.get('aliases', [])) if isinstance(individual.get('aliases'), list) else None
	RacialDescriptor = individual.get('skin_color', {}).get('data') if 'skin_color' in individual else None
	age_string = individual.get('age', {}).get('data') if 'age' in individual else None
	seller = individual.get('seller', {}).get('data') if 'seller' in individual else None
	relationship = individual.get('relationship', {}).get('data') if 'relationship' in individual else None
	physical_features = individual.get('physical_features', {}).get('data') if 'physical_features' in individual else None
	previous_owner = individual.get('previous_owner', {}).get('data') if 'previous_owner' in individual else None
	profession = individual.get('profession', {}).get('data') if 'profession' in individual else None
	year_acquired = individual.get('year_acquired', {}).get('data') if 'year_acquired' in individual else None
	age = individual.get('age', {}).get('data') if 'age' in individual else None
	physical_features = individual.get('physical_features', {}).get('data') if 'physical_features' in individual else None
	origindata = individual.get('origin')


	if isinstance(origindata, dict):  # If 'origindata' is a dictionary
		city = origindata.get('city',{}).get('data', None)
		state = origindata.get('state',{}).get('data', None)
		if city and state:
			origin = f"{city}, {state}"  # Combine city and state
		elif city:  # Only city exists
			origin = city
		else:
			origin = None
	elif isinstance(origindata, str):  # If 'origindata' is a string
		origin = origindata  # Use the string as-is
	else:  # Handle cases where 'origindata' is None or unexpected
		origin = None
	destinationdata = individual.get('destination')
	print("destinationdata",destinationdata)
	if isinstance(destinationdata, dict):  # If 'destinationdata' is a dictionary
		city = destinationdata.get('city',{}).get('data', None)
		state = destinationdata.get('state',{}).get('data', None)
		if city and state:
			destination = f"{city}, {state}"  # Combine city and state
		elif city:  # Only city exists
			destination = city
		else:
			destination = None
	elif isinstance(destinationdata, str):  # If 'destinationdata' is a string
		destination = destinationdata  # Use the string as-is
	else:  # Handle cases where 'destinationdata' is None or unexpected
		destination = None
	# arrival_date
	BirthDate=None
	BirthDateAccuracy=None
	originLocationId=None
	destinationLocationId=None
	sex=None

	FirstName=None
	MiddleName=None
	LastName=None
	# print("origin",origin)

	# Handle `status` as either an integer or a dictionary
	if isinstance(individual.get('status'), dict):
		job = individual['status'].get('data')
	elif isinstance(individual.get('status'), int):
		job = individual['status']  # Status is an integer, so treat it as such
	else:
		job = None

	price = individual.get('price', {}).get('data') if 'price' in individual else individual.get('value', {}).get('data')
	
	# Process each field and update status if they exist
	if name is not None:
		# print(f"Processing individual: {name}")
		update_status(packet, f"{individualNAME}[{index}].name",0.5)
		FirstName, MiddleName, LastName = splitName(name)
	if origin is not None:
		update_status(packet, f"{individualNAME}[{index}].origin",0.5)
		originLocationId=getLocation(connection, cursor, origin)
	if destination is not None:
		update_status(packet, f"{individualNAME}[{index}].destination",0.5)
		destinationLocationId=getLocation(connection, cursor, destination)
	if RacialDescriptor is not None:
		# print(f" - RacialDescriptor: {RacialDescriptor}")
		update_status(packet, f"{individualNAME}[{index}].RacialDescriptor",0.5)
		if RacialDescriptor=="negro":
			sex="male"
		elif  RacialDescriptor=="negress":
			sex="female"
		elif RacialDescriptor=='mulatress':
			sex="female"
		elif RacialDescriptor=='mulatress':
			sex="female"
	if aliases is not None:
		# print(f" - aliases: {aliases}")
		update_status(packet, f"{individualNAME}[{index}].aliases",0.5)
	if year_acquired is not None:
		# print(f" - year_acquired: {year_acquired}")
		update_status(packet, f"{individualNAME}[{index}].year_acquired",0.5)
	if age_string is not None:
		# print(f" - age_string: {age_string}")
		update_status(packet, f"{individualNAME}[{index}].age_string",0.5)
		agematch = re.match(r'(\d+)', str(age_string))
		if agematch:
			age=int(agematch.group(1))
		else:
			age=None
		if transaction['date_circa']:
			BirthDate=calculateBirthDate(transaction['date_circa'], age)
			BirthDateAccuracy="Y"
		print("BirthDate",BirthDate)
	if physical_features is not None:
		# print(f" - physical_features: {physical_features}")
		update_status(packet, f"{individualNAME}[{index}].physical_features",0.5)
	if previous_owner is not None:
		# print(f" - Previous Owner: {previous_owner}")
		update_status(packet, f"{individualNAME}[{index}].previous_owner",0.5)
	if previous_owner is not None:
		# print(f" - Previous Owner: {previous_owner}")
		update_status(packet, f"{individualNAME}[{index}].previous_owner",0.5)
	if profession is not None:
		# print(f" - profession: {profession}")
		update_status(packet, f"{individualNAME}[{index}].profession",0.5)
		
	if age is not None:
		# print(f" - Age: {age}")
		update_status(packet, f"{individualNAME}[{index}].age",0.5)
	if seller is not None:
		# print(f" - Seller: {seller}")
		update_status(packet, f"{individualNAME}[{index}].seller",0.5)
	if seller is not None:
		# print(f" - Seller: {seller}")
		update_status(packet, f"{individualNAME}[{index}].seller",0.5)
	if relationship is not None:
		# print(f" - relationship: {relationship}")
		update_status(packet, f"{individualNAME}[{index}].relationship",0.5)
	
	if job is not None:
		# print(f" - Job: {job}")
		# print(individualNAME[index])
		pass
		# Update status directly if it’s an integer, otherwise use the existing path
		# if isinstance(individual.get('status'), int):
		# 	print("has status??", individual.get('status'))
		# 	
		# else:
		# 	update_status(packet, f"{individualNAME}[{index}].status",0.5)
	if 'origin' in individual:
		# print(f"Processing origin for individual: {name}")
		process_origin(packet, f"{individualNAME}[{index}].origin")
	if price is not None:
		# print(f" - Price: {price}")
		# Update both "price" and "value" statuses if either exists
		if 'price' in individual:
			update_status(packet, f"{individualNAME}[{index}].price",0.5)
		if 'value' in individual:
			update_status(packet, f"{individualNAME}[{index}].value",0.5)

		price = str(price)
		price=re.sub(r'[^0-9.]', '', price)
	individual['status'] = 0.4




	sql=f"select transactionhumans.HumanId from transactionhumans join humans on transactionhumans.HumanId=humans.HumanId where TransactionId='{transaction['TransactionId']}' and FirstName='{FirstName}' and LastName='{LastName}'"
	sql=replace_none_to_null(sql)
	# print(sql)
	cursor.execute(sql)
	result = cursor.fetchall()
	if not result:
		print("new!")
		HumanId = "HUM"+str(uuid.uuid4()).replace("-", "")
	else:
		print("old")
		HumanId=result[0]['HumanId']

	
	
	sql = f"""
		INSERT into humans (HumanId, FirstName, MiddleName, LastName, RacialDescriptor, age_string, BirthDate, BirthDateAccuracy, physical_features, profession,sex)
		VALUES ('{HumanId}', '{FirstName}', '{MiddleName}', '{LastName}', '{RacialDescriptor}', '{age_string}', '{BirthDate}', '{BirthDateAccuracy}', '{physical_features}', '{profession}','{sex}')
		ON DUPLICATE KEY UPDATE 
			FirstName = VALUES(FirstName),
			MiddleName = VALUES(MiddleName),
			LastName = VALUES(LastName),
			RacialDescriptor = VALUES(RacialDescriptor),
			age_string = VALUES(age_string),
			BirthDate = VALUES(BirthDate),
			BirthDateAccuracy = VALUES(BirthDateAccuracy),
			physical_features = VALUES(physical_features),
			profession = VALUES(profession);
	"""

	sql=replace_none_to_null(sql)
	# print(sql)
	cursor.execute(sql)
	connection.commit()
	sql = f"""
		INSERT into transactionhumans (TransactionId, HumanId, Notes, parsedNotes, originLocationId, destinationLocationId, price)
		VALUES ('{transaction['TransactionId']}', '{HumanId}', '{transaction['Notes'].replace("'", "''")}','{transaction['Parsed_Notes'].replace("'", "''")}','{originLocationId}','{destinationLocationId}','{price}')
		ON DUPLICATE KEY UPDATE 
			price = VALUES(price),
			originLocationId=values(originLocationId),
			destinationLocationId=values(destinationLocationId);
	"""

	sql=replace_none_to_null(sql)
	# print(sql)
	cursor.execute(sql)
	connection.commit()

	sql = f"""
		update transactions set processedNotes=1 where TransactionId='{transaction['TransactionId']}'
	"""

	sql=replace_none_to_null(sql)
	# print(sql)
	cursor.execute(sql)
	connection.commit()
	
	

def process_quantity_of_slaves(packet):
	# print(f"Processing quantity of slaves: {packet['quantity_of_slaves']['data']}")
	update_status(packet, 'quantity_of_slaves',0.5)
def process_quantity(packet):
	# print(f"Processing quantity of slaves: {packet['quantity']['data']}")
	update_status(packet, 'quantity',0.5)

def process_price(packet):
	# print(f"Processing price: {packet['price']['data']}")
	update_status(packet, 'price',0.5)
def process_total_sales_price(packet):
	# print(f"Processing price: {packet['total_sales_price']['data']}")
	update_status(packet, 'total_sales_price',0.5)
def process_total_price(packet):
	# print(f"Processing total_price: {packet['total_price']['data']}")
	update_status(packet, 'total_price',0.5)
def process_buyer(packet):
	# print(f"Processing buyer: {packet['buyer']['data']}")
	update_status(packet, 'buyer',0.5)
def process_buyer_status(packet):
	# print(f"Processing buyer_status: {packet['buyer_status']['data']}")
	update_status(packet, 'buyer_status',0.5)
def process_seller(packet):
	# print(f"Processing seller: {packet['seller']['data']}")
	update_status(packet, 'seller', 0.5)
def process_seller_status(packet):
	# print(f"Processing seller_status: {packet['seller_status']['data']}")
	update_status(packet, 'seller_status',0.5)
def process_previous_owner(packet):
	# print(f"Processing previous_owner: {packet['previous_owner']['data']}")
	update_status(packet, 'previous_owner',0.5)
def process_currency(packet):
	# print(f"Processing currency: {packet['currency']['data']}")
	update_status(packet, 'currency',0.5)
def process_date_of_purchase(packet):
	# print(f"Processing date_of_purchase: {packet['date_of_purchase']['data']}")
	update_status(packet, 'date_of_purchase',0.5)
def process_date(packet):
	# print(f"Processing process_date: {packet['date']['data']}")
	update_status(packet, 'date',0.5)
def process_percentage_accuracy(packet):
	# print(f"Processing percentage_accuracy: {packet['percentage_accuracy']['data']}")
	update_status(packet, 'percentage_accuracy',0.5)

	
def process_location(transaction, packet):
	# Check if 'location' exists and is a dictionary
	if 'location' in packet and isinstance(packet['location'], dict):
		location = packet['location']
		# If 'location' has a 'data' key, treat it as a simple entry
		if 'data' in location:
			# print(f"Processing location: {location['data']}")
			update_status(packet, 'location', 0.5)
			
		# Otherwise, handle each subfield in the nested 'location' dictionary
		else:
			if 'venue' in location:
				print(f"Processing venue: {location['venue']['data']}")
				update_status(packet, 'location.venue', 0.5)
			
			if 'address' in location and 'data' in location['address']:
				print(f"Processing address: {location['address']['data']}")
				update_status(packet, 'location.address', 0.5)
			if 'state' in location:
				print(f"Processing state: {location['state']['data']}")
				update_status(packet, 'location.state', 0.5)
			if 'city' in location:
				print(f"Processing city: {location['city']['data']}")
				update_status(packet, 'location.city', 0.5)
	else:
		print("Location data is missing or not in expected format")

	# print("location.venue",location['venue']['data'])
	# print("location.address",location['address']['data'])
	# print("location.state",location['state']['data'])
	# print("location.city",location['city']['data'])
	# cursor, connection = Database.ConnectToDatabase()
	# location=getLocation(connection, cursor, row['LocationFirstParty'])
	# sql = f"""
	# 	select * from locationaddresses where transactionId='{transaction['TransactionId']}'
	# 	VALUES ('{transaction['TransactionId']}', '{HumanId}', '{price}')
	# 	ON DUPLICATE KEY UPDATE 
	# 		price = VALUES(price);
	# """

def process_origin(packet, origin_data_path):
	# Split the path by separating list indices and dictionary keys
	path_segments = []
	for segment in origin_data_path.split('.'):
		if '[' in segment and ']' in segment:
			key, index = segment.split('[')
			index = int(index[:-1])  # Remove the closing bracket and convert to int
			path_segments.append(key)  # Add the dictionary key
			path_segments.append(index)  # Add the list index as an integer
		else:
			path_segments.append(segment)  # Just add the key directly if no list index

	# Traverse to the 'origin' field in the packet based on the parsed path segments
	current = packet
	for segment in path_segments:
		if isinstance(segment, int):  # If segment is an integer, treat as a list index
			if isinstance(current, list) and len(current) > segment:
				current = current[segment]
			else:
				print(f"Error: List index '{segment}' out of range in path '{origin_data_path}'")
				return
		else:  # Otherwise, treat as a dictionary key
			if isinstance(current, dict) and segment in current:
				current = current[segment]
			else:
				print(f"Error: Key '{segment}' not found in path '{origin_data_path}'")
				return

	# At this point, `current` should be the 'origin' dictionary
	origin = current

	# Process fields within 'origin' if they exist
	if 'city' in origin:
		# print(f"Processing city: {origin['city']['data']}")
		update_status(packet, f"{origin_data_path}.city", 0.5)
	if 'state' in origin:
		# print(f"Processing state: {origin['state']['data']}")
		update_status(packet, f"{origin_data_path}.state", 0.5)



def process_packet(transaction,packet):
	for key, value in packet.items():
		# Process each individual in the individuals array and pass index
		if key =='transactions' and isinstance(value, list):
			issues.append('transactions')
			break
		if key == 'individuals' and isinstance(value, list):
			for index, individual in enumerate(value):
				process_individual(transaction,packet, individual, index, "individuals")
		elif key == 'individual':
			# Handle both list and dictionary cases for 'individual'
			if isinstance(value, list):
				for index, individual in enumerate(value):
					process_individual(transaction,packet, individual, index, "individual")
			elif isinstance(value, dict):
				# Process single individual as if it's the first element in a list
				process_individual(transaction,packet, value, 0, "individual")
		elif key == 'quantity_of_slaves':
			process_quantity_of_slaves(packet)
		elif key == 'quantity':
			process_quantity(packet)
		elif key == 'price':
			process_price(packet)
		elif key == 'total_sales_price':
			process_total_sales_price(packet)
		elif key == 'currency':
			process_currency(packet)
		elif key=='total_price':
			process_total_price(packet)
		elif key=='buyer':
			process_buyer(packet)
		elif key=='buyer_status':
			process_buyer_status(packet)
		elif key=='seller':
			process_seller(packet)
		elif key=='seller_status':
			process_seller_status(packet)
		elif key=='previous_owner':
			process_previous_owner(packet)
		elif key=='date_of_purchase':
			process_date_of_purchase(packet)
		elif key=='location':
			process_location(transaction,packet)
		elif key=='percentage_accuracy':
			process_percentage_accuracy(packet)
			
		elif key=='date':
			process_date(packet)
		else:
			# print(f"No specific function to handle key: {key}")
			pass
			
def extractKeys():
	"""
	Connect to the database, fetch rows with JSON data, and extract all unique keys 
	from the `parsed_notes` column recursively.
	"""
	# Connect to the database
	cursor, connection = Database.ConnectToDatabase()
	sql = "SELECT transactionId, parsed_notes from transactions WHERE parsed_notes IS NOT NULL LIMIT 5000"
	cursor.execute(sql)
	result = cursor.fetchall()  # Fetch all rows as dictionaries
	all_keys = set()
	
	for record in result:
		try:
			# Access parsed_notes as a dictionary key
			parsed_notes = record['parsed_notes']
			parsed = json.loads(parsed_notes)  # Parse JSON
			extracted = extract_keys(parsed)
			all_keys.update(extracted)  # Add extracted keys to the set
		except json.JSONDecodeError:
			print(f"Skipping invalid JSON: {record['parsed_notes']}")
			print(record['transactionId'])
		except KeyError:
			print(f"Missing 'parsed_notes' in record: {record}")
		except Exception as e:
			print(f"Unexpected error while processing record: {e}")
		
	print(f"Extracted Keys: {sorted(all_keys)}")
	return "done"

def extract_keys(data):
	"""
	Recursively extract only keys from nested JSON, ignoring all values.
	"""
	keys = set()
	if isinstance(data, dict):
		for key, value in data.items():
			keys.add(key)  # Add the key
			# Debug print to verify values are skipped
			print(f"Processing key: {key}, value type: {type(value)}")
			keys.update(extract_keys(value))  # Recurse into value
	elif isinstance(data, list):
		for item in data:
			keys.update(extract_keys(item))  # Recurse into list items
	# If `data` is not a dict or list, do nothing (ignore values)
	return keys


# def extract_keys(obj, keys=None):
# 	if keys is None:
# 		keys = set()
# 	if isinstance(obj, dict):
# 		for key, value in obj.items():
# 			keys.add(key)
# 			extract_keys(value, keys)
# 	elif isinstance(obj, list):
# 		for item in obj:
# 			extract_keys(item, keys)
# 	return keys





def GetParsedErrors():
	"""
	Fetches the top two transactions from the 'transactions' table
	where 'Issues' and 'dataIssue' are null, ordered by 'parsed_notes' in descending order.
	"""
	# Establish a database connection and get a cursor
	cursor, connection = Database.ConnectToDatabase()
	
	# SQL query to select data
	sql_query = """
		select DISTINCT transactionId, Notes  from transactions where transactionid='TRN012cc6945d6a4ab6a9857434bd34a048'
		limit 4
		
		"""

	
	# Debug: Print the SQL query for verification
	print(sql_query)
	
	# Execute the query and fetch results
	cursor.execute(sql_query)
	result = cursor.fetchall()
	
	# Close the cursor and connection
	cursor.close()
	connection.close()
	
	# Debug: Print the fetched results
	print(result)
	return result


def UpdateParsedErrors():



	parsed=[{"transactionId":"TRN012cc6945d6a4ab6a9857434bd34a048","parsed_notes":{"buyer":"Doyle","price":"$675","individuals":[{"name":"Betsey","skin_color":"negress","age":19,"price":"$675"}]}}]

	# print(len(parsed))

	cursor, connection = Database.ConnectToDatabase()

	try:
		# Loop through each record in the parsed list
		for record in parsed:
			transaction_id = record["transactionId"]
			parsed_notes = record["parsed_notes"]

			# SQL query to update the database
			sql_query = """
				update transactions
				SET parsed_notes = %s
				WHERE TransactionId = %s
			"""
			# print(sql_query)
			# Execute the query with parameters to prevent SQL injection
			cursor.execute(sql_query, (json.dumps(parsed_notes), transaction_id))

		# Commit the changes to the database
		connection.commit()

		print(f"Updated {cursor.rowcount} rows.")
	finally:
		# Ensure the cursor and connection are closed
		cursor.close()
		connection.close()

	return "Saved"


def SaveParsedNotes():

	DebugRowNumber=1
	skip=False
	debug=True
	# Connect to database and set up cursor
	cursor, connection = Database.ConnectToDatabase()
	key_count = defaultdict(int)

	# Query to fetch JSON data
	sql_query ="SELECT TransactionId, Parsed_Notes, Notes, date_circa, date_accuracy,transactions.* from transactions where "
	sql_query+=" (processedNotes is null or processedNotes<>1) and Issues like '%[%' and Parsed_Notes <>'{}' "
	
	# sql_query+=" transactionId='TRN02cc9756d79b40cdbc8d2a37bc758025' "
	sql_query += " ORDER BY parsed_notes DESC LIMIT 500"
	# where Issues is null and dataIssue is null and parsed_notes is not null "
	# if debug:
	# 	sql_query +="  order by parsed_notes desc"
	# 	sql_query +=f" LIMIT 400 OFFSET {DebugRowNumber}"
	# print(sql_query)
	cursor.execute(sql_query)
	result = cursor.fetchall()
	
	
	

	# Process each row
	count = 0
	for transaction in result:
		if skip:
			updatequery=f"update transactions set dataIssue='double check' where TransactionId='{transaction['TransactionId']}'"
			
			cursor.execute(updatequery)
			connection.commit()
			# print(updatequery)
			break
		if transaction['Parsed_Notes'] and transaction['Parsed_Notes'] != 'error':
			try:
				transaction_id = transaction['TransactionId']
				# print("**********************")
				# print("transaction_id",transaction_id)
				# print(transaction['Notes'])
				parsed_data = json.loads(transaction['Parsed_Notes'])
				# print(parsed_data)
				parsed_data=transform_json_packet(parsed_data)
				transaction['parsed_data']=parsed_data
				process_packet(transaction,parsed_data)
				# update_status(parsed_data,"individuals[1].skin_color", 0.5)
				
				display_json_paths(parsed_data)
				# process_row(parsed_data, transaction, cursor, key_count)  # Process each JSON packet
				
				escaped_issues = str(issues).replace("'", "''")
				updatequery=f"update transactions set Issues='{escaped_issues}' where TransactionId='{transaction['TransactionId']}'"
				# print(updatequery)
				cursor.execute(updatequery)
				connection.commit()
			except json.JSONDecodeError as e:
				print(f"Error decoding JSON for TransactionId {transaction_id}: {e}")
				pass
			connection.commit()
			
	
	cursor.close()
	connection.close()

	# print("Key counts across all records (sorted by key name):")
	# for key, count in sorted(key_count.items()):
	# 	print(f"{key}: {count}")
	return "finished"

