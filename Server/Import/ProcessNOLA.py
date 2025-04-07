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

# from InsertTransactions import InsertTransaction  # new import

gmaps = googlemaps.Client(key='AIzaSyB_a1_JJZBF0g43m9KeKVrSlr7ik6_AN_Y')


issues=[]

def ProcessNOLA():
	cursor, connection = Database.ConnectToDatabase()
	NOLAs = getNOLAs(cursor)
	cursor.close()
	connection.close()
	
	# Load human_map one time here
	connection2 = Database.ConnectToDatabase()[1]
	human_map = loadHumanMap(connection2)
	connection2.close()
	
	thedates = []
	for i, row in enumerate(NOLAs):
		cursor, connection = Database.ConnectToDatabase()
		
		# Parse and set the transaction date and other transaction fields
		NOLAs[i]['DateOfTransaction'] = ParseDate(row['DateOfTransaction'], row['NOLA_ID'])
		NOLAs[i]['NOLA_ID'] = row['NOLA_ID']
		NOLAs[i]['TransactionType'] = row.get('TransactionType', '')
		NOLAs[i]['Notes'] = row.get('Notes', '')
		NOLAs[i]['Act'] = row.get('Act', '')
		NOLAs[i]['Page'] = row.get('Page', '')
		NOLAs[i]['Volume'] = row.get('Volume', '')
		NOLAs[i]['URL'] = row.get('URL', '')
		# New variables
		NOLAs[i]['Transcriber'] = row.get('Transcriber', '')
		NOLAs[i]['Parsed_Notes'] = row.get('Parsed_Notes', '')
		NOLAs[i]['QuantityOfSlaves'] = row.get('QuantityOfSlaves', 0)
		NOLAs[i]['TotalPrice'] = row.get('TotalPrice', 0.0)
		
		# Parse the humans with proper roles
		Notary = ParseHumanNames(row['NotaryPublic'], 'Notary', NOLAs[i]['DateOfTransaction'])
		Sellers = ParseHumanNames(row['FirstParty'], 'Seller', NOLAs[i]['DateOfTransaction'])
		Buyers = ParseHumanNames(row['SecondParty'], 'Buyer', NOLAs[i]['DateOfTransaction'])
		# Merge all humans into a single list
		humans = Sellers + Buyers + Notary
		OfficeLocationId=None
		
		# Assign location IDs based on role
		for human in humans:
			if human['Human']['Role'] == 'Seller':
				human['Human']['ResidenceLocationId'] = getLocation(connection, cursor, row['LocationFirstParty'])
			elif human['Human']['Role'] == 'Buyer':
				human['Human']['ResidenceLocationId'] = getLocation(connection, cursor, row['LocationSecondParty'])
			elif human['Human']['Role'] == 'Notary':
				OfficeLocationId = getLocation(connection, cursor, 'New Orleans, Louisiana')
		
		# Check human map for pre-existing human IDs and collect new humans to save.
		to_save = []
		for human in humans:
			first = human['Human']['FirstName'].strip().lower()
			middle = human['Human']['MiddleName'].strip().lower()
			last = human['Human']['LastName'].strip().lower()
			key = f"{first}:{middle}:{last}"
			if key in human_map:
				human['Human']['HumanId'] = human_map[key]
			else:
				to_save.append(human)
		
		# Save new humans and update their HumanIds and the human_map
		if to_save:
			new_ids = SaveHuman(connection, cursor, to_save, human_map)
			for idx, h in enumerate(to_save):
				h['Human']['HumanId'] = new_ids[idx]
		
		# Insert into humantimeline by checking for a valid ResidenceLocationId and passing parameters
		date_circa = NOLAs[i]['DateOfTransaction']['parsed_date']
		for human in humans:
			if human['Human'].get('ResidenceLocationId') and human['Human']['ResidenceLocationId'] != "None":
				InsertHumanTimeline(
					cursor,
					human['Human']['HumanId'],
					human['Human']['ResidenceLocationId'],
					date_circa,
					"Residence",
					human['Human']['Role']
				)
		
		if OfficeLocationId:
			for human in humans:
			
				InsertHumanTimeline(
					cursor,
					human['Human']['HumanId'],
					OfficeLocationId,
					date_circa,
					"Notary Office",
					human['Human']['Role']
				)
		
		# Prepare a transaction dictionary and call InsertTransaction
		txn = {
			"NOLA_ID": row['NOLA_ID'],
			"date_circa": NOLAs[i]['DateOfTransaction']['parsed_date'],
			"date_accuracy": NOLAs[i]['DateOfTransaction']['DateAccuracy'],
			"TransactionType": NOLAs[i]['TransactionType'],
			"Notes": NOLAs[i]['Notes'],
			"Act": NOLAs[i]['Act'],
			"Page": NOLAs[i]['Page'],
			"Volume": NOLAs[i]['Volume'],
			"URL": NOLAs[i]['URL'],
			"NeedsReview": 0,
			"Transcriber": NOLAs[i]['Transcriber'],
			"Parsed_Notes": NOLAs[i]['Parsed_Notes'],
			"QuantityOfSlaves": NOLAs[i]['QuantityOfSlaves'],
			"TotalPrice": NOLAs[i]['TotalPrice'],
			"dataIssue": "",
			"Issues": "",
			"LocationId": None,
			"processedNotes": 0,
			"isApproved": 0,
			"DataQuestions": ""
		}
		# TransactionId=InsertTransaction(connection, cursor, txn)
		print("uncomment!")
		print("uncomment!")
		print("uncomment!")
		print("uncomment!")
		print("uncomment!")
		print("uncomment!")
		print("uncomment!")
		print("uncomment!")
		print("uncomment!")
		print("uncomment!")
		print("uncomment!")
		print("uncomment!")
		print("uncomment!")
		print("uncomment!")
		print("uncomment!")
		print("uncomment!")
		print("uncomment!")
		print("uncomment!")
		print("uncomment!")
		print("uncomment!")
		print("uncomment!")
		print("uncomment!")
		print("uncomment!")
		print("uncomment!")
		print("uncomment!")
		print("uncomment!")
		print("uncomment!")
		print("uncomment!")
		print("uncomment!")
		print("uncomment!")
		print("uncomment!")

		parsed_data = json.loads(row['Parsed_Notes'])
		# print(parsed_data)
		parsed_data=transform_json_packet(parsed_data)
		process_packet(NOLAs[i],parsed_data)
		
		connection.commit()
		cursor.close()
		connection.close()
		print(i)

		if i >=10:
			print(humans)
			break

	return str(i+1)




def getNOLAs(cursor):
	sql=f"select distinct * from raw_nola"
	cursor.execute(sql)
	results=cursor.fetchall()
	
	return results



def loadHumanMap(connection):
	cursor, conn2 = Database.ConnectToDatabase()
	query = "SELECT HumanId, FirstName, MiddleName, LastName FROM humans where FirstName is not null and MiddleName is not null and LastName is not null"
	cursor.execute(query)
	rows = cursor.fetchall()
	human_map = {}
	for r in rows:
		# Ensure None values become empty strings and all parts must be present
		first = (r['FirstName'] or '').strip().lower()
		middle = (r.get('MiddleName') or '').strip().lower()
		last = (r['LastName'] or '').strip().lower()
		if first and middle and last:
			key = f"{first}:{middle}:{last}"
			human_map[key] = r['HumanId']
	cursor.close()
	conn2.close()
	return human_map

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
		query = f"insert into locationaddresses(LocationId,Address,DateUpdated) values('{LocationId}','{location_str}',NOW())"
		cursor.execute(query)
		connection.commit()

		print("LocationId",LocationId)
		return LocationId






	return None

def SaveHuman(connection, cursor, humans, human_map):
	new_ids = []
	for human in humans:
		first = human['Human']['FirstName'].strip().lower()
		middle = human['Human']['MiddleName'].strip().lower()
		last = human['Human']['LastName'].strip().lower()
		key = f"{first}:{middle}:{last}"
		# Check if human already exists in the database
		query_check = f"SELECT HumanId FROM humans WHERE LOWER(FirstName)='{first}' AND LOWER(MiddleName)='{middle}' AND LOWER(LastName)='{last}'"
		cursor.execute(query_check)
		result = cursor.fetchone()
		if result:
			HumanId = result['HumanId']
		else:
			HumanId = "HUM" + str(uuid.uuid4()).replace("-", "")
			query = f"INSERT INTO humans (HumanId,FirstName, MiddleName, LastName, DateUpdated) VALUES ('{HumanId}','{first}', '{middle}', '{last}', NOW())"
			print(query)
			cursor.execute(query)
			connection.commit()
		human_map[key] = HumanId
		new_ids.append(HumanId)
	return new_ids

def InsertHumanTimeline(cursor, human_id, location_id, date_circa, location_type, role):
	query_tl = (
		f"INSERT INTO humantimeline (HumanId, LocationId, Date_Circa, Date_Accuracy, LocationType, RoleId, DateUpdated) "
		f"VALUES ('{human_id}', '{location_id}', '{date_circa}', 'D', '{location_type}', '{role}', NOW()) "
		f"ON DUPLICATE KEY UPDATE LocationType = VALUES(LocationType), RoleId = VALUES(RoleId), DateUpdated = NOW()"
	)
	print(query_tl)
	cursor.execute(query_tl)

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
		INSERT into transactionhumans (TransactionId, HumanId, Notes, parsedNotes, originLocationId, destinationLocationId, price, DateUpdated)
		VALUES ('{transaction['TransactionId']}', '{HumanId}', '{transaction['Notes'].replace("'", "''")}', '{transaction['Parsed_Notes'].replace("'", "''")}', '{originLocationId}', '{destinationLocationId}', '{price}', NOW())
		ON DUPLICATE KEY UPDATE 
			price = VALUES(price),
			originLocationId = VALUES(originLocationId),
			destinationLocationId = VALUES(destinationLocationId),
			DateUpdated = NOW();
	"""

	sql=replace_none_to_null(sql)
	# print(sql)
	cursor.execute(sql)
	connection.commit()

	sql = f"""
		update transactions set processedNotes=1, DateUpdated=NOW() where TransactionId='{transaction['TransactionId']}'
	"""

	sql=replace_none_to_null(sql)
	# print(sql)
	cursor.execute(sql)
	connection.commit()


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

def replace_none_to_null(query):
	# Replace occurrences of 'None' with 'NULL' in the query string
	query = query.replace("'None'", "NULL")
	query = query.replace("=NULL", " IS NULL")
	query = query.replace("= NULL", " IS NULL")
	return query

	

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