import uuid
from Lib import Database
from datetime import datetime, timedelta
from dateutil import parser

def save_ship_manifest(ShipInfo,ShipManifest):
	# Connect to the database
	cursor, connection = Database.ConnectToDatabase()

	
	# ['ShipName', 'ShipSize', 'ShipType', 'ShipHomePort', 'ShipHomePortCity', 'ShipHomePortState', 'CaptainLastName', 'CaptainFirstName', 'VoyageStartDate', 'VoyageEndDate']
	
	try:
		query = "select LocationId from Locations where City = %s and State=%s and Address is null"
		values=(ShipInfo['ShipHomePortCity'],ShipInfo['ShipHomePortState'],)
		cursor.execute(query, values)
		result = cursor.fetchone()

		if result is None:
			ShipHomePortLocationId = "LOC" + str(uuid.uuid4())
			query = "INSERT INTO Locations (LocationId, City, State) VALUES (%s, %s, %s)"
			values = (ShipHomePortLocationId, ShipInfo['ShipHomePortCity'],ShipInfo['ShipHomePortState'],)
			cursor.execute(query, values)
			
		else:
			ShipHomePortLocationId = result['LocationId']

		print("ShipHomePortLocationId",ShipHomePortLocationId)

		query = "select ShipId from Ships where ShipName = %s and ShipType=%s"
		values=(ShipInfo['ShipName'], ShipInfo['ShipType'])
		cursor.execute(query, values,)
		result = cursor.fetchone()
		if result is None:
			ShipId = "SHP" + str(uuid.uuid4())
			query = "INSERT INTO Ships (ShipId, ShipName,ShipType,Size,HomePortLocationId) VALUES (%s, %s, %s, %s, %s)"
			values = (ShipId, ShipInfo['ShipName'], ShipInfo['ShipType'],ShipInfo['ShipSize'],ShipHomePortLocationId,)
			cursor.execute(query, values)
		else:
			ShipId = result['ShipId']

		print("ShipId",ShipId)

		query = "select Humans.HumanId from Humans "
		query += " where Humans.FirstName = %s and Humans.LastName=%s "
		values=(ShipInfo['CaptainFirstName'], ShipInfo['CaptainLastName'],)
		
		cursor.execute(query, values)
		result = cursor.fetchone()

		if result is None:
			CaptainHumanId = "HUM" + str(uuid.uuid4())
			query = "INSERT INTO Humans(HumanId,FirstName,LastName) VALUES (%s, %s, %s) "
		
			values = (CaptainHumanId, ShipInfo['CaptainFirstName'], ShipInfo['CaptainLastName'],)
			cursor.execute(query, values)
		else:
			CaptainHumanId = result['HumanId']


		query = "select LocationId from Locations where City = %s and State=%s and Address is null"
		values=("Norfolk","Virginia",)
		
		cursor.execute(query, values)
		result = cursor.fetchone()
		if result is None:
			StartLocationId = "LOC" + str(uuid.uuid4())
			query = "INSERT INTO Locations(LocationId, City, State) VALUES (%s, %s, %s) "
		
			values = (StartLocationId, OwnerCity, OwnerState,)
			cursor.execute(query, values)
		else:
			StartLocationId = result['LocationId']


		query = "select LocationId from Locations where City = %s and State=%s and Address is null"
		values=("New Orleans","Louisiana",) 
		
		cursor.execute(query, values)
		result = cursor.fetchone()
		if result is None:
			EndLocationId = "LOC" + str(uuid.uuid4())
			query = "INSERT INTO Locations(LocationId, City, State) VALUES (%s, %s, %s) "
		
			values = (EndLocationId, OwnerCity, OwnerState,)
			cursor.execute(query, values)
		else:
			EndLocationId = result['LocationId']


		




		query = "select VoyageId from Voyages where ShipId = %s and StartDate=%s and EndDate=%s"
		values=(ShipId,ShipInfo['VoyageStartDate'], ShipInfo['VoyageEndDate'],) 
		
		cursor.execute(query, values)
		result = cursor.fetchone()
		if result is None:

			VoyageId = ShipInfo['VoyageId'] + "-"+ str(uuid.uuid4())
			
			query = "INSERT INTO Voyages(VoyageId, ShipId, CaptainHumanId,StartLocationId,EndLocationId,StartDate,EndDate) VALUES (%s, %s, %s,%s, %s, %s,%s) "
		
			values = (VoyageId[:39], ShipId, CaptainHumanId,StartLocationId,EndLocationId,ShipInfo['VoyageStartDate'], ShipInfo['VoyageEndDate'],)
			cursor.execute(query, values)
		else:
			VoyageId=result['VoyageId']


		names = list(ShipManifest[0].keys())
		print(names)

		# ['EnslavedLastName', 'EnslavedFirstName', 'EnslavedGender', 'EnslavedHeightInInches', 'EnslavedColor', 'EnslavedBirthDateAccuracy', 'EnslavedBirthDate', 'OwnerStartFirstName', 'OwnerStartLastName', 'OwnerStartCity', 'OwnerStartState', 'ShippingAgentFirstName', 'ShippingAgentLastName', 'OwnerEndFirstName', 'OwnerEndLastName', 'Notes', 'Transcriber']
		for row in ShipManifest:
			query = "select LocationId from Locations where City = %s and State=%s and Address is null"
			values=(row['OwnerStartCity'],row['OwnerStartState'],)
			
			cursor.execute(query, values)
			result = cursor.fetchone()
			if result is None:
				OwnerStartLocationId = "LOC" + str(uuid.uuid4())
				query = "INSERT INTO Locations(LocationId, City, State) VALUES (%s, %s, %s) "
			
				values = (OwnerStartLocationId, row['OwnerStartCity'],row['OwnerStartState'],)
				cursor.execute(query, values)
			else:
				OwnerStartLocationId = result['LocationId']



			query = "select HumanId from Humans where Humans.FirstName = %s and Humans.LastName=%s"
			values=(row['OwnerStartFirstName'],row['OwnerStartLastName'],)
			
			cursor.execute(query, values)
			result = cursor.fetchone()

			if result is None:
				OwnerStartHumanId = "HUM" + str(uuid.uuid4())
				query = "INSERT INTO Humans(HumanId,FirstName,LastName) VALUES (%s, %s, %s) "
				
				values = (OwnerStartHumanId, row['OwnerStartFirstName'],row['OwnerStartLastName'],)
				cursor.execute(query, values)
			else:
				OwnerStartHumanId=result['HumanId']
			
			OwnerStartBusinessId = "BUS" + str(uuid.uuid4())
			query = "INSERT INTO Businesses(BusinessId, BusinessName, LocationId) VALUES (%s, %s, %s) "
		
			values = (OwnerStartBusinessId, row['OwnerStartFirstName']+" "+row['OwnerStartLastName'],OwnerStartLocationId,)
			cursor.execute(query, values)

			query = "INSERT INTO BusinessHumans(BusinessId, HumanId, RoleId) VALUES (%s, %s, %s) "
		
			values = (OwnerStartBusinessId, OwnerStartHumanId,"ROL-SLV-OWN-8f-82-49b-8aee-1b5b6e696ca9")
			cursor.execute(query, values)





			query = "select LocationId from Locations where City = %s and State=%s and Address is null"
			values=(row['OwnerEndCity'],row['OwnerEndState'],)
			
			cursor.execute(query, values)
			result = cursor.fetchone()
			if result is None:
				OwnerEndLocationId = "LOC" + str(uuid.uuid4())
				query = "INSERT INTO Locations(LocationId, City, State) VALUES (%s, %s, %s) "
			
				values = (OwnerEndLocationId, row['OwnerEndCity'],row['OwnerEndState'],)
				cursor.execute(query, values)
			else:
				OwnerEndLocationId = result['LocationId']



			query = "select HumanId from Humans  where Humans.FirstName = %s and Humans.LastName=%s"
			values=(row['OwnerEndFirstName'],row['OwnerEndLastName'],)
			
			cursor.execute(query, values)
			result = cursor.fetchone()

			if result is None:
				OwnerEndHumanId = "HUM" + str(uuid.uuid4())
				query = "INSERT INTO Humans(HumanId,FirstName,LastName) VALUES (%s, %s, %s) "
				
				values = (OwnerEndHumanId, row['OwnerEndFirstName'],row['OwnerEndLastName'],)
				cursor.execute(query, values)
			else:
				OwnerEndHumanId=result['HumanId']
			OwnerEndBusinessId = "BUS" + str(uuid.uuid4())
			query = "INSERT INTO Businesses(BusinessId, BusinessName, LocationId) VALUES (%s, %s, %s) "
		
			values = (OwnerEndBusinessId, row['OwnerEndFirstName']+" "+row['OwnerEndLastName'],OwnerEndLocationId,)
			cursor.execute(query, values)

			query = "INSERT INTO BusinessHumans(BusinessId, HumanId, RoleId) VALUES (%s, %s, %s) "
		
			values = (OwnerEndBusinessId, OwnerEndHumanId,"ROL-SLV-OWN-8f-82-49b-8aee-1b5b6e696ca9")
			cursor.execute(query, values)



			ShippingAgentLocationId=None
			query = "select HumanId from Humans  where Humans.FirstName = %s and Humans.LastName=%s"
			values=(row['ShippingAgentFirstName'],row['ShippingAgentLastName'],)
			
			cursor.execute(query, values)
			result = cursor.fetchone()

			if result is None:
				ShippingAgentLastNameHumanId = "HUM" + str(uuid.uuid4())
				query = "INSERT INTO Humans(HumanId,FirstName,LastName) VALUES (%s, %s, %s) "
				
				values = (ShippingAgentLastNameHumanId, row['ShippingAgentFirstName'],row['ShippingAgentLastName'],)
				cursor.execute(query, values)
			else:
				ShippingAgentLastNameHumanId=result['HumanId']
			ShippingAgentBusinessId = "BUS" + str(uuid.uuid4())
			query = "INSERT INTO Businesses(BusinessId, BusinessName, LocationId) VALUES (%s, %s, %s) "
		
			values = (ShippingAgentBusinessId, row['ShippingAgentFirstName']+" "+row['ShippingAgentLastName'],ShippingAgentLocationId,)
			cursor.execute(query, values)

			query = "INSERT INTO BusinessHumans(BusinessId, HumanId, RoleId) VALUES (%s, %s, %s) "
		
			values = (ShippingAgentBusinessId, ShippingAgentLastNameHumanId,"ROL-SLV-OWN-8f-82-49b-8aee-1b5b6e696ca9")
			cursor.execute(query, values)

			




			query = "select HumanId from Humans  where Humans.FirstName = %s and Humans.LastName=%s and BirthDate=%s"
			values=(row['EnslavedFirstName'],row['EnslavedLastName'],row['EnslavedBirthDate'])
			
			cursor.execute(query, values)
			result = cursor.fetchone()

			if result is None:
				HumanId = "HUM" + str(uuid.uuid4())
				query = "INSERT INTO Humans(HumanId,FirstName,LastName, BirthDate, Gender, HeightInInches, RaceId) VALUES (%s, %s, %s, %s, %s, %s, %s) "
				
				values = (HumanId, row['EnslavedFirstName'], row['EnslavedLastName'], row['EnslavedBirthDate'], row['EnslavedGender'], float(row['EnslavedHeightInInches']), row['EnslavedColor'],)
				cursor.execute(query,values)
			else:
				HumanId = result['HumanId']


			query = "INSERT INTO HumanOwners(HumanId, OwnerBusinessId, OwnDate) VALUES (%s, %s, %s) "

			values = (HumanId, OwnerStartBusinessId,ShipInfo['VoyageStartDate'])
			cursor.execute(query, values)
			connection.commit()

			query = "INSERT INTO HumanOwners(HumanId, OwnerBusinessId, OwnDate) VALUES (%s, %s, %s) "

			values = (HumanId, OwnerEndBusinessId,ShipInfo['VoyageEndDate'])
			cursor.execute(query, values)
			connection.commit()
			
			query = "INSERT INTO VoyageHumans(VoyageId, HumanId, RoleId, OwnerStartBusinessId, OwnerEndBusinessId, ShippingAgentBusinessId, Notes) VALUES (%s, %s, %s,%s, %s, %s, %s) "

			query += "ON DUPLICATE KEY UPDATE OwnerStartBusinessId=values(OwnerStartBusinessId),OwnerEndBusinessId=values(OwnerEndBusinessId),ShippingAgentBusinessId=values(ShippingAgentBusinessId),Notes=values(Notes)"
			values = (VoyageId, HumanId, "ROL-EN-SLV-ba45f-4ed4-aa44-63cf5114b0c1",OwnerStartBusinessId, OwnerEndBusinessId,ShippingAgentBusinessId, row['Notes'])
			
			cursor.execute(query, values)
			connection.commit()
		
	except Exception as e:
		# Handle the error
		print("An error occurred:", str(e))

		# Rollback the changes
		connection.rollback()

	finally:
		# Close the cursor and the database connection
		connection.commit()
		cursor.close()
		connection.close()
		
		
	

	# else:
	#	 ShipId = result['ShipId']

	# VoyageStartDate=None
	# CaptainFirstName=None
	# CaptainLastName=None
	# for row in spreadsheet_array:
	#	 StartYear=row["Year of Manifest Recorded in Norfolk (yyyy)"]
	#	 MonthAndDay=row["Month and day of Manifest Recorded in Norfolk (mm-dd)"]
		
	#	 if len(StartYear):
	#		 if "-" in MonthAndDay:
	#			 sd = MonthAndDay+ "-" + StartYear
	#			 # VoyageStartDate = datetime.strptime(sd, "%m-%d-%Y")
	#		 else:
	#			 sd = MonthAndDay+ " " + StartYear
	#			 # VoyageStartDate = datetime.strptime(sd, "%B %d %Y")

	#		 try:
	#			 VoyageStartDate = parser.parse(sd)
	#		 except Exception as e:
	#			 print("EXCEPTION!",e)
	#			 VoyageStartDate=None
	#	 print("VoyageStartDate",VoyageStartDate)
	#	 CaptainName=row["Ship Captain's Name (Last, First Middle)"]
	#	 if len(CaptainName):
	#		 CaptainLastName=CaptainName.split(",")[0].strip()
	#		 CaptainFirstName=CaptainName.split(",")[1].strip()
			
	# 


	# BusinessId = "BUS" + str(uuid.uuid4())
	# query = "INSERT INTO Businesses(BusinessId, BusinessName) VALUES (%s, %s) "

	# values = (BusinessId, ShipName,)
	# cursor.execute(query, values)
	# connection.commit()

	# query = "INSERT INTO BusinessHumans(BusinessId, HumanId, RoleId) VALUES (%s, %s, %s) "

	# values = (BusinessId, CaptainHumanId,"ROL-CAP-2da-c1cc-4100-abbb-3da1508fc827")
	# cursor.execute(query, values)
	# connection.commit()


	# for row in spreadsheet_array:
		
	#	 EnslavedLastName=row["Last Name"]
	#	 EnslavedFirstName=row["First and Middle Names"]
	#	 EnslavedGender=row["Sex"]
	#	 EnslavedAge=row["Age"]
	#	 if "months" in EnslavedAge :
	#		 EnslavedAge = int(EnslavedAge.split(" ")[0])/12
	#	 EnslavedHeightInInches=float(row["Height (feet)"])*12+fraction_to_float(row["Height (inches)"])
	#	 EnslavedColor=row["Color"]
	#	 bd = "January 1 "+ str(int(StartYear)-int(EnslavedAge))
	#	 EnslavedBirthDate = datetime.strptime(bd, "%B %d %Y")

	#	 OwnerName=row["Owner's Name (Last, First Middle)"]
	#	 OwnerFirstName=""
	#	 OwnerLastName=""
	#	 if len(OwnerName) and "," in OwnerName:
	#		 OwnerFirstName=OwnerName.split(",")[1].strip()
	#		 OwnerLastName=OwnerName.split(",")[0].strip()

	#	 OwnerLocation=row["Owner's Location (Locality, State)"]
	#	 OwnerLocationId=None
	#	 OwnerCity=""
	#	 OwnerState=""
	#	 if len(OwnerLocation) and "," in OwnerLocation:
	#		 OwnerCity=OwnerLocation.split(",")[0].strip()
	#		 OwnerState=OwnerLocation.split(",")[1].strip()
	#	 elif len(OwnerLocation) and " " in OwnerLocation:
	#		 OwnerCity=OwnerLocation.split(" ")[0].strip()
	#		 OwnerState=OwnerLocation.split(" ")[1].strip()

	

	#	 ShippingAgentName=row["Shipping Agent (Last Name, First and Middle)"]
	#	 ShippingAgentFirstName=None
	#	 ShippingAgentLastName=None
	#	 if len(ShippingAgentName) and "," in ShippingAgentName :
	#		 ShippingAgentFirstName=ShippingAgentName.split(",")[1].strip()
	#		 ShippingAgentLastName=ShippingAgentName.split(",")[0].strip()

	#	 OwnerAgentName=row["Owner/Agent 2 Location (Locality, State)"]
	#	 OwnerAgentFirstName=None
	#	 OwnerAgentLastName=None
	#	 if len(OwnerAgentName) and "," in OwnerAgentName:
	#		 OwnerAgentFirstName=OwnerAgentName.split(",")[1].strip()
	#		 OwnerAgentLastName=OwnerAgentName.split(",")[0].strip()

	#	 query = "select Humans.HumanId from Humans join HumanOwners on Humans.HumanId=HumanOwners.HumanId "
	#	 query += " join Businesses on Businesses.BusinessId=HumanOwners.OwnerBusinessId "
	#	 query += " join BusinessHumans on BusinessHumans.BusinessId=Businesses.BusinessId "
	#	 query += " join Humans Owners on Owners.HumanId = BusinessHumans.HumanId "
	#	 query += " where Humans.FirstName = %s and Humans.LastName=%s and Owners.FirstName = %s and Owners.LastName=%s"
	#	 values=(EnslavedFirstName,EnslavedLastName,OwnerFirstName,OwnerLastName,)
		
	#	 cursor.execute(query, values)
	#	 result = cursor.fetchone()

	

	#	 query = "select Humans.HumanId from Humans "
	#	 query += " join BusinessHumans on BusinessHumans.HumanId=Humans.HumanId "
	#	 query += " join HumanOwners on HumanOwners.OwnerBusinessId=BusinessHumans.BusinessId "

	




	

	#		 query = "INSERT INTO HumanOwners(HumanId, OwnerBusinessId, OwnDate) VALUES (%s, %s, %s) "
		
	#		 values = (HumanId, BusinessId,VoyageStartDate)
	#		 cursor.execute(query, values)
	#		 connection.commit()
	#	 else:
	#		 OwnerHumanId = result['HumanId']

	# connection.close()
	

	# Return the HumanId as a JSON response
	return {'success': True}

