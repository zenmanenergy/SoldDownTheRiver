from _Lib import Database

def get_combinedtimelines(HumanId):
	cursor, connection = Database.ConnectToDatabase()

	response={}
	response['combinedTimeLine'] = []
	
	try:
		# Query the database for timelines related to the given HumanId, including location details
		query = """
			SELECT h.BirthDate, h.BirthDateAccuracy, h.HumanId, h.FirstName, h.LastName
			FROM humans h
			
			WHERE h.HumanId = %s
		"""
		cursor.execute(query, (HumanId,))
		human = cursor.fetchone()  # Already returns a dictionary due to DictCursor
		response['human']=human
		if human['BirthDate']:
			row={}
			row['DateCirca']=human['BirthDate']
			row['DateAccuracy']=human['BirthDateAccuracy']
			row['Description']="Birth date"
			response['combinedTimeLine'].append(row)
		# Query the database for timelines related to the given HumanId, including location details
		query = """
			SELECT ht.LocationId, ht.Date_Circa, ht.Date_Accuracy, ht.LocationType,ht.RoleId,
				l.Address, l.City, l.County, l.State, l.State_abbr, 
				l.Country, l.Latitude, l.Longitude, l.LocationType, h.FirstName, h.LastName
			FROM humantimeline ht
			LEFT JOIN locations l ON ht.LocationId = l.LocationId
			JOIN humans h on h.HumanId = ht.HumanId
			WHERE ht.HumanId = %s
			ORDER BY ht.Date_Circa ASC
		"""
		cursor.execute(query, (HumanId,))
		response['knowntimelines'] = cursor.fetchall() 
		
		# Process known timelines and add them to the combined timeline
		for timelinerow in response['knowntimelines']:
			row = {}
			row['DateCirca'] = timelinerow['Date_Circa']
			row['DateAccuracy'] = timelinerow['Date_Accuracy']
			row['Latitude'] = timelinerow['Latitude']
			row['Longitude'] = timelinerow['Longitude']
			
			# Build description based on location type and role
			description_parts = []
			
			if timelinerow['LocationType']:
				description_parts.append(f"Location Type: {timelinerow['LocationType']}")
			
			if timelinerow['RoleId']:
				description_parts.append(f"Role: {timelinerow['RoleId']}")
			
			# Add location information
			location_parts = []
			if timelinerow['Address']:
				location_parts.append(timelinerow['Address'])
			if timelinerow['City']:
				location_parts.append(timelinerow['City'])
			if timelinerow['County']:
				location_parts.append(timelinerow['County'])
			if timelinerow['State']:
				location_parts.append(timelinerow['State'])
			if timelinerow['Country']:
				location_parts.append(timelinerow['Country'])
			
			if location_parts:
				description_parts.append(f"Location: {', '.join(location_parts)}")
			
			row['Description'] = " - ".join(description_parts) if description_parts else "Timeline entry"
			response['combinedTimeLine'].append(row)
		query = """
			SELECT distinct
			t.TransactionId,
			t.date_circa,
			t.date_accuracy,
			t.TransactionType,
			th.RoleId,
			l.Latitude,
			l.Longitude

			
		FROM transactions t
			JOIN transactionhumans th ON t.TransactionId = th.TransactionId AND th.HumanId = %s
			join locations l on t.LocationId=l.LocationId
			
		order by t.date_circa asc
		"""
		cursor.execute(query, (HumanId))
		transactions = cursor.fetchall()  # Already returns a dictionary due to DictCursor
		
		for transaction in transactions:
			
			query = """
				SELECT distinct
				h.HumanId,
				h.FirstName,
				h.LastName
				
			FROM transactionhumans th 
			join humans h ON h.HumanId = th.HumanId AND th.TransactionId = %s and h.HumanId <> %s
			
			where th.RoleId = 'Seller' or  th.RoleId = 'Owner1' or th.RoleId='FirstParty'
			order by h.FirstName, h.LastName
				
			"""
			cursor.execute(query, (transaction['TransactionId'], human['HumanId']))
			transaction['Seller'] = cursor.fetchall()

		for transaction in transactions:
			query = """
				SELECT distinct
				h.HumanId,
				h.FirstName,
				h.LastName
				
			FROM transactionhumans th 
			join humans h ON h.HumanId = th.HumanId AND th.TransactionId = %s and h.HumanId <> %s
			where th.RoleId = 'Buyer' or  th.RoleId = 'Owner2' or th.RoleId='SecondParty'
			order by h.FirstName, h.LastName
				
			"""
			cursor.execute(query, (transaction['TransactionId'], human['HumanId']))
			transaction['Buyer'] = cursor.fetchall()

		for transaction in transactions:
			query = """
				SELECT distinct
				h.HumanId,
				h.FirstName,
				h.LastName
				
			FROM transactionhumans th 
			join humans h ON h.HumanId = th.HumanId AND th.TransactionId = %s and h.HumanId <> %s
			where th.RoleId = 'Notary'
			order by h.FirstName, h.LastName
				
		# 	"""
			cursor.execute(query, (transaction['TransactionId'], human['HumanId']))
			transaction['Notary'] = cursor.fetchall()

		response['transactions']=transactions

		for transaction in transactions:
			query = """
				SELECT distinct
				h.HumanId,
				h.FirstName,
				h.LastName
				
			FROM transactionhumans th 
			join humans h ON h.HumanId = th.HumanId AND th.TransactionId = %s and h.HumanId <> %s
			where th.RoleId = 'Enslaved'
			order by h.FirstName, h.LastName
				
		# 	"""
			cursor.execute(query, (transaction['TransactionId'], human['HumanId']))
			transaction['Enslaved'] = cursor.fetchall()

		response['transactions']=transactions
		query = """
			SELECT 
				h.HumanId,
				h.FirstName,
				h.LastName,
				vh.VoyageId,
				vh.RoleId,
				voyages.StartDate,
				voyages.StartDateAccuracy,
				voyages.EndDate,
				voyages.EndDateAccuracy,
				voyages.CustomsDate,
				voyages.CustomsDateAccuracy,
				startLocation.Latitude StartLatitude,
				startLocation.Longitude StartLongitude,
				startLocation.city AS startCity, 
				startLocation.State AS startState,
				endLocation.city AS endCity, 
				endLocation.State AS endState,
				endLocation.Latitude EndLatitude,
				endLocation.Longitude EndLongitude,
				s.ShipName
			FROM 
				voyagehumans vh
			JOIN voyages ON vh.VoyageId = voyages.VoyageId
			JOIN ships s ON voyages.ShipId = s.ShipId
			JOIN locations startLocation ON startLocation.LocationId = voyages.startLocationid
			JOIN locations endLocation ON endLocation.LocationId = voyages.endLocationid
			JOIN humans h ON h.HumanId = vh.HumanId
			WHERE 
				vh.HumanId = %s
			
			
		"""
		cursor.execute(query, (HumanId, ))
		voyages = cursor.fetchall()  # Already returns a dictionary due to DictCursor
		for voyage in voyages:
			
			query = """
				SELECT distinct
				h.HumanId,
				h.FirstName,
				h.LastName,
				vh.Notes
				
			FROM voyagehumans vh 
			join humans h ON h.HumanId = vh.HumanId AND vh.VoyageId = %s
			where vh.RoleId = 'Captain'
				
			"""
			cursor.execute(query, (voyage['VoyageId']))
			voyage['Captain'] = cursor.fetchall()
			

			query = """
				SELECT distinct
				h.HumanId,
				h.FirstName,
				h.LastName
				
			FROM voyagehumans vh 
			join humans h ON h.HumanId = vh.HumanId AND vh.VoyageId = %s
			where vh.RoleId = 'CollectorAgent'
				
			"""
			cursor.execute(query, (voyage['VoyageId']))
			voyage['CollectorAgent'] = cursor.fetchall()
			for collector in voyage['CollectorAgent']:
				query = """
					SELECT distinct
					h.HumanId,
					h.FirstName,
					h.LastName
					
				FROM voyagehumans vh 
				join humans h ON h.HumanId = vh.HumanId AND vh.VoyageId = %s and collectoragent_humanid =%s
				"""
				
				cursor.execute(query, (voyage['VoyageId'],collector['HumanId']))
				collector_enslaved = cursor.fetchall()
				collector['Enslaved']=collector_enslaved
				


			query = """
				SELECT distinct
				h.HumanId,
				h.FirstName,
				h.LastName
				
			FROM voyagehumans vh 
			join humans h ON h.HumanId = vh.HumanId AND vh.VoyageId = %s
			where vh.RoleId = 'ShippingAgent'
				
			"""
			cursor.execute(query, (voyage['VoyageId']))
			voyage['ShippingAgent'] = cursor.fetchall()
			for shipper in voyage['ShippingAgent']:
				query = """
					SELECT distinct
					h.HumanId,
					h.FirstName,
					h.LastName
					
				FROM voyagehumans vh 
				join humans h ON h.HumanId = vh.HumanId AND vh.VoyageId = %s and shippingagent_humanid =%s
				"""
				cursor.execute(query, (voyage['VoyageId'],shipper['HumanId']))
				collector_enslaved = cursor.fetchall()
				shipper['Enslaved']=collector_enslaved

			query = """
				SELECT distinct
				h.HumanId,
				h.FirstName,
				h.LastName
				
			FROM voyagehumans vh 
			join humans h ON h.HumanId = vh.HumanId AND vh.VoyageId = %s
			where vh.RoleId = 'Enslaved'
				
			"""
			cursor.execute(query, (voyage['VoyageId']))
			voyage['Enslaved'] = cursor.fetchall()
		

			query = """
				SELECT distinct
				h.HumanId,
				h.FirstName,
				h.LastName
				
			FROM voyagehumans vh 
			join humans h ON h.HumanId = vh.owner_humanid AND vh.VoyageId = %s
				
			"""
			cursor.execute(query, (voyage['VoyageId']))
			voyage['Seller'] = cursor.fetchall()
			for seller in voyage['Seller']:
				query = """
					SELECT distinct
					h.HumanId,
					h.FirstName,
					h.LastName
					
				FROM voyagehumans vh 
				join humans h ON h.HumanId = vh.HumanId AND vh.VoyageId = %s and owner_humanid =%s
				"""
				
				cursor.execute(query, (voyage['VoyageId'],seller['HumanId']))
				seller_enslaved = cursor.fetchall()
				seller['Enslaved']=seller_enslaved

			query = """
				SELECT distinct
				h.HumanId,
				h.FirstName,
				h.LastName
				
			FROM voyagehumans vh 
			join humans h ON h.HumanId = vh.owner2_humanid AND vh.VoyageId = %s
				
			"""
			cursor.execute(query, (voyage['VoyageId']))
			voyage['Buyer'] = cursor.fetchall()
			for Buyer in voyage['Buyer']:
				query = """
					SELECT distinct
					h.HumanId,
					h.FirstName,
					h.LastName
					
				FROM voyagehumans vh 
				join humans h ON h.HumanId = vh.HumanId AND vh.VoyageId = %s and owner2_humanid =%s
				"""
				
				cursor.execute(query, (voyage['VoyageId'],Buyer['HumanId']))
				Buyer_enslaved = cursor.fetchall()
				Buyer['Enslaved']=Buyer_enslaved
		response['voyages']=voyages
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
		

		connection.close()


		for transaction in response['transactions']:
			row={}
			row['DateCirca']=transaction['date_circa']
			row['DateAccuracy']=transaction['date_accuracy']
			row['Latitude']=transaction['Latitude']
			row['Longitude']=transaction['Longitude']
			name_parts = []
			# Wrap the human's name in a link to their report
			human_name = " ".join(
				filter(None, [human.get('FirstName'), human.get('LastName')])
			)
			if human_name:
				human_link = f'<a href="/Reports/Human?HumanId={human.get("HumanId")}">{human_name}</a>'
				name_parts.append(human_link)

			if transaction['RoleId']:
				role = str(transaction['RoleId'])
				if role == "Enslaved":
					EnslavedDescription(transaction,name_parts)

				elif role == "Buyer":
					BuyerDescription(transaction,name_parts)
				elif role == "Seller":
					SellerDescription(transaction,name_parts)
				elif role == "Notary":
					NotaryDescription(transaction,name_parts)

			row['Description'] = " ".join(name_parts)
			response['combinedTimeLine'].append(row)

		for voyage in response['voyages']:
			row={}
			
			name_parts = []
			# Wrap the human's name in a link to their report
			human_name = " ".join(
				filter(None, [human.get('FirstName'), human.get('LastName')])
			)
			if human_name:
				human_link = f'<a href="/Reports/Human?HumanId={human.get("HumanId")}">{human_name}</a>'
				name_parts.append(human_link)
			print(voyage['RoleId'])
			if voyage['RoleId']:
				role = str(voyage['RoleId'])
				if role == "Captain":
					row['DateCirca']=voyage['StartDate']
					row['DateAccuracy']=voyage['StartDateAccuracy']
					row['Latitude']=voyage['StartLatitude']
					row['Longitude']=voyage['StartLongitude']
					CaptainDescription(voyage,name_parts)
				elif role == "Owner2":
					row['Latitude']=voyage['EndLatitude']
					row['Longitude']=voyage['EndLongitude']
					row['DateCirca']=voyage['EndDate']
					row['DateAccuracy']=voyage['EndDateAccuracy']
					BuyerDescription(voyage,name_parts)

				elif role == "Owner1":
					row['Latitude']=voyage['StartLatitude']
					row['Longitude']=voyage['StartLongitude']
					row['DateCirca']=voyage['EndDate']
					row['DateAccuracy']=voyage['EndDateAccuracy']
					SellerDescription(voyage,name_parts)

				elif role == "CollectorAgent":
					row['Latitude']=voyage['EndLatitude']
					row['Longitude']=voyage['EndLongitude']
					row['DateCirca']=voyage['EndDate']
					row['DateAccuracy']=voyage['EndDateAccuracy']
					CollectorAgentDescription(voyage,name_parts)

				elif role == "ShippingAgent":
					row['Latitude']=voyage['StartLatitude']
					row['Longitude']=voyage['StartLongitude']
					row['DateCirca']=voyage['StartDate']
					row['DateAccuracy']=voyage['StartDateAccuracy']
					ShippingAgentDescription(voyage,name_parts)
				elif role == "Enslaved":
					row['Latitude']=voyage['EndLatitude']
					row['Longitude']=voyage['EndLongitude']
					row['DateCirca']=voyage['EndDate']
					row['DateAccuracy']=voyage['EndDateAccuracy']
					EnslavedDescription(voyage,name_parts)

				

			row['Description'] = " ".join(name_parts)
			response['combinedTimeLine'].append(row)

		# Sort the combined timeline by date
		def get_sort_key(item):
			date_value = item.get('DateCirca')
			if not date_value:
				return '1900-01-01'
			# Convert to string for consistent comparison
			if hasattr(date_value, 'strftime'):
				return date_value.strftime('%Y-%m-%d')
			return str(date_value)
		
		response['combinedTimeLine'].sort(key=get_sort_key)


		return {"success": True, "data": response}
	except Exception as e:
		return {"success": False, "error": str(e)}
	
def ShippingAgentDescription(voyage, name_parts):
	# Build enslaved string
	enslaved = []
	for person in voyage.get('Enslaved', []):
		person_name = " ".join(
			filter(None, [person.get('FirstName'), person.get('LastName')])
		)
		link = f'<a href="/Reports/Human?HumanId={person.get("HumanId")}">{person_name}</a>'
		enslaved.append(link)
	enslaved_str = ", ".join(enslaved) if enslaved else "Unnamed Enslaved Person"
	# Get start location
	start_city = voyage.get('startCity', '')
	start_state = voyage.get('startState', '')
	desc = f"shipped these enslaved people: {enslaved_str} from {start_city} {start_state}"
	name_parts.append(desc)
	return name_parts

def CollectorAgentDescription(voyage, name_parts):
	# Build enslaved string
	enslaved = []
	for person in voyage.get('Enslaved', []):
		person_name = " ".join(
			filter(None, [person.get('FirstName'), person.get('LastName')])
		)
		link = f'<a href="/Reports/Human?HumanId={person.get("HumanId")}">{person_name}</a>'
		enslaved.append(link)
	enslaved_str = ", ".join(enslaved) if enslaved else "Unnamed Enslaved Person"
	# Get end location
	end_city = voyage.get('endCity', '')
	end_state = voyage.get('endState', '')
	desc = f"collected these enslaved people: {enslaved_str} at {end_city} {end_state}"
	name_parts.append(desc)
	return name_parts

def BuyerDescription(voyage, name_parts):
	# Build buyer's name (already in name_parts if called from timeline loop)
	# Build enslaved string
	enslaved = []
	for person in voyage.get('Enslaved', []):
		person_name = " ".join(
			filter(None, [person.get('FirstName'), person.get('LastName')])
		)
		link = f'<a href="/Reports/Human?HumanId={person.get("HumanId")}">{person_name}</a>'
		enslaved.append(link)
	enslaved_str = ", ".join(enslaved) if enslaved else "Unnamed Enslaved Person"
	# Build seller string
	sellers = []
	for seller in voyage.get('Seller', []):
		seller_name = " ".join(
			filter(None, [seller.get('FirstName'), seller.get('LastName')])
		)
		link = f'<a href="/Reports/Human?HumanId={seller.get("HumanId")}">{seller_name}</a>'
		sellers.append(link)
	sellers_str = " and ".join(sellers) if sellers else "Unknown Seller"
	# Get start and end locations
	start_city = voyage.get('startCity', '')
	start_state = voyage.get('startState', '')
	end_city = voyage.get('endCity', '')
	end_state = voyage.get('endState', '')
	desc = f"bought {enslaved_str} from {sellers_str} shipped from {start_city} {start_state} to {end_city} {end_state}"
	name_parts.append(desc)
	return name_parts

def CaptainDescription(voyage, name_parts):
	# Get captain's name (already in name_parts)
	# Build enslaved string
	enslaved = []
	for person in voyage.get('Enslaved', []):
		person_name = " ".join(
			filter(None, [person.get('FirstName'), person.get('LastName')])
		)
		link = f'<a href="/Reports/Human?HumanId={person.get("HumanId")}">{person_name}</a>'
		enslaved.append(link)
	enslaved_str = ", ".join(enslaved) if enslaved else "Unnamed Enslaved Person"
	# Get start and end locations
	start_city = voyage.get('startCity', '')
	start_state = voyage.get('startState', '')
	end_city = voyage.get('endCity', '')
	end_state = voyage.get('endState', '')
	# If you have separate end location fields, use them here
	desc = f"shipped these enslaved people: {enslaved_str} from {start_city} {start_state}"
	# If you have end location info, append it
	if end_city or end_state:
		desc += f" to {end_city} {end_state}"
	name_parts.append(desc)
	return name_parts

def NotaryDescription(transaction, name_parts):
	# Build notary string
	notaries = []
	for notary in transaction.get('Notary', []):
		notary_name = " ".join(
			filter(None, [notary.get('FirstName'), notary.get('LastName')])
		)
		link = f'<a href="/Reports/Human?HumanId={notary.get("HumanId")}">{notary_name}</a>'
		notaries.append(link)
	notaries_str = " and ".join(notaries) if notaries else "Unknown Notary"

	# Build enslaved string
	enslaved = []
	for person in transaction.get('Enslaved', []):
		person_name = " ".join(
			filter(None, [person.get('FirstName'), person.get('LastName')])
		)
		link = f'<a href="/Reports/Human?HumanId={person.get("HumanId")}">{person_name}</a>'
		enslaved.append(link)
	enslaved_str = ", ".join(enslaved) if enslaved else "Unnamed Enslaved Person"

	# Build sellers string
	sellers = []
	for seller in transaction.get('Seller', []):
		seller_name = " ".join(
			filter(None, [seller.get('FirstName'), "" ,seller.get('LastName')])
		)
		link = f'<a href="/Reports/Human?HumanId={seller.get("HumanId")}">{seller_name}</a>'
		sellers.append(link)
	sellers_str = " and ".join(sellers) if sellers else "Unknown Seller"

	# Build buyers string
	buyers = []
	for buyer in transaction.get('Buyer', []):
		buyer_name = " ".join(
			filter(None, [buyer.get('FirstName'), buyer.get('LastName')])
		)
		link = f'<a href="/Reports/Human?HumanId={buyer.get("HumanId")}">{buyer_name}</a>'
		buyers.append(link)
	buyers_str = " and ".join(buyers) if buyers else "Unknown Buyer"

	# Make "notarized the sale of" a link to the transaction report
	transaction_id = transaction.get('TransactionId')
	sale_link = f'<a href="/Reports/Transaction?TransactionId={transaction_id}">notarized the sale of</a>'

	desc = f"{notaries_str} {sale_link} {enslaved_str} from: {sellers_str} to: {buyers_str}"
	name_parts.append(desc)
	return name_parts

def SellerDescription(transaction, name_parts):
	# Build buyers string
	buyers = []
	for buyer in transaction.get('Buyer', []):
		buyer_name = " ".join(
			filter(None, [buyer.get('FirstName'), buyer.get('LastName')])
		)
		link = f'<a href="/Reports/Human?HumanId={buyer.get("HumanId")}">{buyer_name}</a>'
		buyers.append(link)
	buyers_str = " and ".join(buyers) if buyers else "Unknown Buyer"
	# Build enslaved string
	enslaved = []
	for person in transaction.get('Enslaved', []):
		person_name = " ".join(
			filter(None, [person.get('FirstName'), person.get('LastName')])
		)
		link = f'<a href="/Reports/Human?HumanId={person.get("HumanId")}">{person_name}</a>'
		enslaved.append(link)
	enslaved_str = ", ".join(enslaved) if enslaved else "Unnamed Enslaved Person"
	# Make "sold" a link to the transaction report
	transaction_id = transaction.get('TransactionId')
	sold_link = f'<a href="/Reports/Transaction?TransactionId={transaction_id}">sold</a>: '
	desc = f"{sold_link} {enslaved_str} to: {buyers_str}"
	# Add notary if present
	notaries = []
	for notary in transaction.get('Notary', []):
		notary_name = " ".join(
			filter(None, [notary.get('FirstName'), notary.get('LastName')])
		)
		link = f'<a href="/Reports/Human?HumanId={notary.get("HumanId")}">{notary_name}</a>'
		notaries.append(link)
	if notaries:
		desc += f", notarized by: {' and '.join(notaries)}"
	name_parts.append(desc)
	return name_parts

def BuyerDescription(transaction, name_parts):
	# Build sellers string
	sellers = []
	for seller in transaction.get('Seller', []):
		seller_name = " ".join(
			filter(None, [seller.get('FirstName'), seller.get('LastName')])
		)
		link = f'<a href="/Reports/Human?HumanId={seller.get("HumanId")}">{seller_name}</a>'
		sellers.append(link)
	sellers_str = " and ".join(sellers) if sellers else "Unknown Seller"
	# Build buyers string
	buyers = []
	for buyer in transaction.get('Buyer', []):
		buyer_name = " ".join(
			filter(None, [buyer.get('FirstName'), buyer.get('LastName')])
		)
		link = f'<a href="/Reports/Human?HumanId={buyer.get("HumanId")}">{buyer_name}</a>'
		buyers.append(link)
	buyers_str = " and ".join(buyers) if buyers else "Unknown Buyer"
	# Build enslaved string
	enslaved = []
	for person in transaction.get('Enslaved', []):
		person_name = " ".join(
			filter(None, [person.get('FirstName'), person.get('LastName')])
		)
		link = f'<a href="/Reports/Human?HumanId={person.get("HumanId")}">{person_name}</a>'
		enslaved.append(link)
	enslaved_str = ", ".join(enslaved) if enslaved else "Unnamed Enslaved Person"
	# Make "bought" a link to the transaction report
	transaction_id = transaction.get('TransactionId')
	bought_link = f'<a href="/Reports/Transaction?TransactionId={transaction_id}">bought</a>:'
	desc = f"{bought_link} {enslaved_str} from: {sellers_str}"
	# Add notary if present
	notaries = []
	for notary in transaction.get('Notary', []):
		notary_name = " ".join(
			filter(None, [notary.get('FirstName'), notary.get('LastName')])
		)
		link = f'<a href="/Reports/Human?HumanId={notary.get("HumanId")}">{notary_name}</a>'
		notaries.append(link)
	if not notaries:
		desc += ""
	else:
		desc += f", notarized by: {' and '.join(notaries)}"
	name_parts.append(desc)
	return name_parts

def EnslavedDescription(transaction, name_parts):
	role = "Enslaved Person"
	# Build sellers string
	sellers = []
	for seller in transaction.get('Seller', []):
		seller_name = " ".join(
			filter(None, [seller.get('FirstName'), seller.get('LastName')])
		)
		link = f'<a href="/Reports/Human?HumanId={seller.get("HumanId")}">{seller_name}</a>'
		sellers.append(link)
	sellers_str = " and ".join(sellers) if sellers else "Unknown Seller"
	# Build buyers string
	buyers = []
	for buyer in transaction.get('Buyer', []):
		buyer_name = " ".join(
			filter(None, [buyer.get('FirstName'), buyer.get('LastName')])
		)
		link = f'<a href="/Reports/Human?HumanId={buyer.get("HumanId")}">{buyer_name}</a>'
		buyers.append(link)
	buyers_str = " and ".join(buyers) if buyers else "Unknown Buyer"
	desc = f"was sold by: {sellers_str} to: {buyers_str}"
	# Add notary if present
	notaries = []
	for notary in transaction.get('Notary', []):
		notary_name = " ".join(
			filter(None, [notary.get('FirstName'), notary.get('LastName')])
		)
		link = f'<a href="/Reports/Human?HumanId={notary.get("HumanId")}">{notary_name}</a>'
		notaries.append(link)
	if notaries:
		desc += f", notarized by: {' and '.join(notaries)}"
	name_parts.append(desc)
	return name_parts