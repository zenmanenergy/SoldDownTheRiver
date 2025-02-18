import uuid
from _Lib import Database
from datetime import datetime, timedelta
from dateutil import parser
from dateutil.relativedelta import relativedelta


def extract_Notary( spreadsheet_name, spreadsheet_array):
	# Connect to the database
	cursor, connection = Database.ConnectToDatabase()
	
	
	

	


	rows=[]
	for row in spreadsheet_array:
		rowData={}
		#  - [Last Name, First and Middle Names]  Be sure to add connections to this person especially if they are acting as an agent for someone else."]
		
		
		rowData['FromHumans']=[]
		rowData['FromCity']=""
		rowData['FromState']=""
		rowData['ToCity']=""
		rowData['ToState']=""
		Notary = row['Notary Public']
		print(Notary, row['Location of First Party [Locality, State]'], row["Second Party (To) - [Last Name, First and Middle Names]"])
		
		FromParty=row['First Party (From)']
		rowData['FromParty']=FromParty
		FromParty=FromParty.split("and")
		rowData['NotaryLastName']= Notary.split(",")[0].strip()
		rowData['NotaryFirstName'] = Notary.split(",")[1]
		rowData['NotaryFirstName'] =  rowData['NotaryFirstName'].split("(")[0].strip()
		for party in FromParty:
			party=party.replace("Mr.", "").strip()
			From={}
			if ',' in party:
				From['FirstName']= party.split(",")[1].strip()
				From['LastName']=""
				if len(party.split(",")[0].strip()) > 1:
					From['LastName']= party.split(",")[0].strip()

			else:
				
				From['FirstName']= party.split(" ")[0].strip()
				From['LastName']=""
				if len(party.split(" ")) > 1:
					From['LastName']= party.split(" ")[1].strip()
			rowData['FromHumans'].append(From)

		

		FromLocation=row['Location of First Party [Locality, State]'].split(",")
		if len(FromLocation) > 0:
			rowData['FromCity']=FromLocation[0].strip()
		if len(FromLocation) > 1:
			rowData['FromState']=FromLocation[1].strip()





		ToParty=row["Second Party (To) - [Last Name, First and Middle Names]"]
		rowData['ToParty']=ToParty
		ToParty=ToParty.split("and")
		
		rowData['ToHumans']=[]
		for party in ToParty:
			party=party.replace("Mr.", "").strip()
			To={}
			if ',' in party:
				To['FirstName']= party.split(",")[1].strip()
				To['LastName']=""
				if len(party.split(",")[0].strip()) > 1:
					To['LastName']= party.split(",")[0].strip()

			else:
				
				To['FirstName']= party.split(" ")[0].strip()
				To['LastName']=""
				if len(party.split(" ")) > 1:
					To['LastName']= party.split(" ")[1].strip()
			rowData['ToHumans'].append(To)


		
		

		ToLocation=row['Location of Second Party [Locality, State]'].split(",")
		if len(ToLocation) > 0:
			rowData['ToCity']=ToLocation[0].strip()
		if len(ToLocation) > 1:
			rowData['ToState']=ToLocation[1].strip()

		
		rowData['TransactionType']=row['Type of Transaction']
		rowData['TransactionDate']=row['Date (yyyy-mm-dd) - [ex. 1825-05-05]']
		
		
		try:
			rowData['TransactionDate'] = parser.parse(rowData['TransactionDate'])
		except Exception as e:
			rowData['TransactionDate']=None


		rowData['Act']=row['Act']
		rowData['Page']=row['Page/Folio']
		rowData['Volume']=row['Volume #']
		
		rowData['Notes']=row['Notes']
		#  (Be sure to add total sale\'s price, name of slave,  ethnicity, gender, age, and sale\'s price.)   [Ex.  Total sales price - $ 1,200.  Tom, negro boy aged 12 years old  who was sold for $ 600. Jane, mulatto woman aged 23 years old who was sold for $ 600.] ']
		

		# Total sales price - $ 1,200. Mary, negro woman aged about 27 years
		Price=rowData['Notes'].split("$")
		rowData['TotalPrice']=0
		if "." in Price:
			Price=Price[1].strip().split(".")
			if len(Price)>0:
				rowData['TotalPrice']=Price[0].replace(",", "").strip()

		EnslavedHumans=rowData['Notes'].replace("Total sales price -", "").strip()
		rowData['TransactionHumans']=[]
		if "." in EnslavedHumans:
			
			EnslavedHumansSTR=EnslavedHumans.split(".")[1]
			EnslavedHumansSTR=EnslavedHumansSTR.replace(", negro"," a negro")
			EnslavedHumansSTR=EnslavedHumansSTR.replace(" and "," ")
			EnslavedHumansSTR=EnslavedHumansSTR.replace("  "," ")
			EnslavedHumans=EnslavedHumansSTR.split(",")
			# print("0",EnslavedHumans)

			for EnslavedHuman in EnslavedHumans:
				HumanInfo={}
				HumanInfo['Notes']=EnslavedHuman.strip()
				EnslavedHuman=EnslavedHuman.strip()
				EnslavedHuman=EnslavedHuman.replace(" a ",";")
				EnslavedHuman=EnslavedHuman.replace(" aged ",";")
				EnslavedHuman=EnslavedHuman.replace(" age ",";")
				EnslavedHuman=EnslavedHuman.replace(" infant",";0 years")
				EnslavedHuman=EnslavedHuman.replace(" years old","")
				EnslavedHuman=EnslavedHuman.replace(" years","")
				EnslavedHuman=EnslavedHuman.replace(" ten ","10")
				
				if ";" in EnslavedHuman:
					EnslavedHuman=EnslavedHuman.split(";")
					
					HumanInfo['EnslavedHumanName']=""
					HumanInfo['EnslavedHumanFirstName']=""
					HumanInfo['EnslavedHumanLastName']=""
					HumanInfo['EnslavedHumanGender']=""
					HumanInfo['EnslavedHumanColor']=""
					HumanInfo['EnslavedHumanAge']=None
					HumanInfo['EnslavedHumanBirthDate']=None
					HumanInfo['EnslavedHumanBirthDateAccuracy']=""
					# Total sales price - $20,000. Jack a negro man aged 46 years old, Albert a mulatto man aged 20 years old, Barnaby a negro man aged about 46 years old, Lee a negro man aged about 32 years old, Harry a negro man aged about 26 years old, Watt a negro man aged about 36 years, Stratsward a negro man aged 27 years old, Franklin a negro man aged 41 years old, Washington a "brown colored man" aged 24 years old, Tony a negro man aged 23, Henry Greene a negro man aged 25 years, Armstead a negro man aged 29 years, Kel a brown colored man aged 43 years, Sam Thompson a negro man aged 25 years old, Joe a negro man aged 41 years old, Ben a negro man aged 46 years old, Julius a yellow man aged 71 years old, Ben Ellis a negro man aged 46 years old, Henry Bedford a negro man aged 28 years old, Cedar L a negro man aged 39 years old, Tom Anderson a negro man aged 45 years old, Vapper a negro man aged 36 years old, Billy Ellis a yellow man aged 41 years old, Sam a negro man aged 21 years old, Yarman a brown man aged 27 years old, Cesar Griffen a negro man aged 20 years old, Anderson a negro man aged 20 years old, Nelson a negro man aged 19 years old, Beverly a negro man aged 18 years old, Winston a negro man aged 18 years old, Bob a negro man aged 41 years old, Billy Baker a negro man aged 46 years old, Alexander Ellis a yellow man boy aged 15 years old, Godfrey a yellow boy aged 17 years, Lewis Ellis a yellow boy aged 14 years old, Jesse a negro boy aged 17 years old, Bill a black boy aged 15 years old, Alexander W a negro lad aged 19 years, Brick a negro lad aged 18 years, Austin a negro lad aged 16 years, George a negro boy aged 13 years, Harry a brown boy aged 14 years, Cuffy a negro man aged 25 years, Sam Page a negro man aged 29 years, Peter a negro man aged 41 years, Humphrey a black boy aged 14 years, John Napper a brown boy aged 14 years, Solomon a brown boy aged 14 years, John Carr a brown boy aged 17 years, Betty a black woman aged 47 years, Lotty a negress aged 38 years, Emily a negress aged 97 years, Eugenia a negress aged 21 years, Susan a negress aged 21 years, Sucky Bole a negress aged 37 years, Linda a negress aged 30 years, Elsey a negress aged 23 years, Judy a negress aged 36 years, Nelly a brown woman aged 24 years, Mana a brown woman aged 24 years, Elizabeth a mulatress aged 27 years old, Winny a brown woman aged 21 years, Fanny a negress aged 35 years old, Silvy a negress aged 20 years, Souisa a negress aged 17 years, Sarah a negress aged 41 years, Mary Ellis a negress aged 26, Mary Prince a negress aged 24 years, Harriet a brown colored girl aged 15 years, Delphy a negress aged 14 years, Lucy a negress aged 27 years, Betsy Ellis a mulatress aged 21 years old, Sucky Ellis a mulatress aged 46 years old, Nancy Napper a mulatress aged 35, Frances Napper a brown colored girl aged 15 years old, Dolly a negress woman aged 35 years, Louisa Ellis a negress aged 13 years, Robert Ester a negro boy aged 9 years, Jackson Ellis a negro boy aged 6 years, Fanny Ellis a black infant, Milly a negress aged 3 years, Judy Cole a negress aged ten years, Stephen Rowe a mulatto boy aged 6 years, Sidney a negro boy aged 3 years, Tom a brown colored boy aged 11 years, Dilla a yellow girl aged 7 years, Jane a negress aged 4 years, Mo a black aged 3 years, Stephen Napper a brown colored boy, Blank Napper a brown colored boy aged 9, Jacob Napper a brown colored boy age 4, Angelina a negress aged 10 years, Gabriel a negro boy aged 3 years, Nancy a negress aged 4 years, Cary Arm a black infant, Peggy a yellow girl aged 13 years, Swina Ellis a yellow girl aged 10 years, Violet Ellis a yellow girl aged 10 years, Susan Ellis a yellow girl aged 10 years, William Blue a mulatto boy aged 8 years, Dan Blue brown colored boy aged 6, Lucinda Blue a mulatress aged 14 years, John Blue a brown colored infant, Franky a negro boy aged 7 years,  and Tom a negro boy aged 7 years.
					
					
					
					
					if " " in EnslavedHuman[0].strip():
						Names=EnslavedHuman[0].strip().split(" ")
						
						HumanInfo['EnslavedHumanFirstName']=Names[0]
						HumanInfo['EnslavedHumanLastName']=' '.join(Names[1:])
					else:

						HumanInfo['EnslavedHumanFirstName']=EnslavedHuman[0]
						

							
					if len(EnslavedHuman)>1:
						EnslavedHumanLook=EnslavedHuman[1]
						if "negro" in EnslavedHuman[1]:
							HumanInfo['EnslavedHumanColor']="Negro"
							HumanInfo['EnslavedHumanGender']="Male"
						elif "negress" in EnslavedHuman[1]:
							HumanInfo['EnslavedHumanColor']="Negress"
							HumanInfo['EnslavedHumanGender']="Female"
						elif "mulatress" in EnslavedHuman[1]:
							HumanInfo['EnslavedHumanColor']="mulatress"
							HumanInfo['EnslavedHumanGender']="Female"
						elif "black" in EnslavedHuman[1]:
							HumanInfo['EnslavedHumanColor']="Black"
						elif "yellow" in EnslavedHuman[1]:
							HumanInfo['EnslavedHumanColor']="Yellow"
						elif "brown" in EnslavedHuman[1]:
							HumanInfo['EnslavedHumanColor']="Brown"
						elif "mulatto" in EnslavedHuman[1]:
							HumanInfo['EnslavedHumanColor']="Mulatto"
							

						if "woman" in EnslavedHuman[1]:
							HumanInfo['EnslavedHumanGender']="Female"
						elif "man" in EnslavedHuman[1]:
							HumanInfo['EnslavedHumanGender']="Male"
						elif "boy" in EnslavedHuman[1]:
							HumanInfo['EnslavedHumanGender']="Male"
						elif "girl" in EnslavedHuman[1]:
							HumanInfo['EnslavedHumanGender']="Female"

					if len(EnslavedHuman)>2:
						HumanInfo['EnslavedHumanAge']=EnslavedHuman[2]
						HumanInfo['EnslavedHumanAge']=HumanInfo['EnslavedHumanAge'].replace("about","")
						HumanInfo['EnslavedHumanAge']=HumanInfo['EnslavedHumanAge'].replace("ten","10")
						HumanInfo['EnslavedHumanAge']=HumanInfo['EnslavedHumanAge'].strip()
						HumanInfo['EnslavedHumanAge']=HumanInfo['EnslavedHumanAge']
						if rowData['TransactionDate'] and HumanInfo['EnslavedHumanAge'].isdigit():
							HumanInfo['EnslavedHumanBirthDateAccuracy']="Year"
							HumanInfo['EnslavedHumanBirthDate'] = rowData['TransactionDate'] - relativedelta(years=int(HumanInfo['EnslavedHumanAge']))
						# print(HumanInfo['EnslavedHumanName'])
						# print(HumanInfo['EnslavedHumanGender'])
						# print(HumanInfo['EnslavedHumanColor'])
						# print(HumanInfo['EnslavedHumanAge'])
						# print(HumanInfo['TransactionDate'])
						# print(HumanInfo['EnslavedHumanBirthDate'])
						# print(HumanInfo['EnslavedHumanBirthDateAccuracy'])
					
					
					if len(HumanInfo['Notes'])> 3:
						rowData['TransactionHumans'].append(HumanInfo)   

# Total sales price - $20,000. Jack a negro man aged 46 years old, Albert a mulatto man aged 20 years old, Barnaby a negro man aged about 46 years old, Lee a negro man aged about 32 years old, Harry a negro man aged about 26 years old, Watt a negro man aged about 36 years, Stratsward a negro man aged 27 years old, Franklin a negro man aged 41 years old, Washington a "brown colored man" aged 24 years old, Tony a negro man aged 23, Henry Greene a negro man aged 25 years, Armstead a negro man aged 29 years, Kel a brown colored man aged 43 years, Sam Thompson a negro man aged 25 years old, Joe a negro man aged 41 years old, Ben a negro man aged 46 years old, Julius a yellow man aged 71 years old, Ben Ellis a negro man aged 46 years old, Henry Bedford a negro man aged 28 years old, Cedar L a negro man aged 39 years old, Tom Anderson a negro man aged 45 years old, Vapper a negro man aged 36 years old, Billy Ellis a yellow man aged 41 years old, Sam a negro man aged 21 years old, Yarman a brown man aged 27 years old, Cesar Griffen a negro man aged 20 years old, Anderson a negro man aged 20 years old, Nelson a negro man aged 19 years old, Beverly a negro man aged 18 years old, Winston a negro man aged 18 years old, Bob a negro man aged 41 years old, Billy Baker a negro man aged 46 years old, Alexander Ellis a yellow man boy aged 15 years old, Godfrey a yellow boy aged 17 years, Lewis Ellis a yellow boy aged 14 years old, Jesse a negro boy aged 17 years old, Bill a black boy aged 15 years old, Alexander W a negro lad aged 19 years, Brick a negro lad aged 18 years, Austin a negro lad aged 16 years, George a negro boy aged 13 years, Harry a brown boy aged 14 years, Cuffy a negro man aged 25 years, Sam Page a negro man aged 29 years, Peter a negro man aged 41 years, Humphrey a black boy aged 14 years, John Napper a brown boy aged 14 years, Solomon a brown boy aged 14 years, John Carr a brown boy aged 17 years, Betty a black woman aged 47 years, Lotty a negress aged 38 years, Emily a negress aged 97 years, Eugenia a negress aged 21 years, Susan a negress aged 21 years, Sucky Bole a negress aged 37 years, Linda a negress aged 30 years, Elsey a negress aged 23 years, Judy a negress aged 36 years, Nelly a brown woman aged 24 years, Mana a brown woman aged 24 years, Elizabeth a mulatress aged 27 years old, Winny a brown woman aged 21 years, Fanny a negress aged 35 years old, Silvy a negress aged 20 years, Souisa a negress aged 17 years, Sarah a negress aged 41 years, Mary Ellis a negress aged 26, Mary Prince a negress aged 24 years, Harriet a brown colored girl aged 15 years, Delphy a negress aged 14 years, Lucy a negress aged 27 years, Betsy Ellis a mulatress aged 21 years old, Sucky Ellis a mulatress aged 46 years old, Nancy Napper a mulatress aged 35, Frances Napper a brown colored girl aged 15 years old, Dolly a negress woman aged 35 years, Louisa Ellis a negress aged 13 years, Robert Ester a negro boy aged 9 years, Jackson Ellis a negro boy aged 6 years, Fanny Ellis a black infant, Milly a negress aged 3 years, Judy Cole a negress aged ten years, Stephen Rowe a mulatto boy aged 6 years, Sidney a negro boy aged 3 years, Tom a brown colored boy aged 11 years, Dilla a yellow girl aged 7 years, Jane a negress aged 4 years, Mo a black aged 3 years, Stephen Napper a brown colored boy, Blank Napper a brown colored boy aged 9, Jacob Napper a brown colored boy age 4, Angelina a negress aged 10 years, Gabriel a negro boy aged 3 years, Nancy a negress aged 4 years, Cary Arm a black infant, Peggy a yellow girl aged 13 years, Swina Ellis a yellow girl aged 10 years, Violet Ellis a yellow girl aged 10 years, Susan Ellis a yellow girl aged 10 years, William Blue a mulatto boy aged 8 years, Dan Blue a brown colored boy aged 6, Lucinda Blue a mulatress aged 14 years, John Blue a brown colored infant, Franky a negro boy aged 7 years,  and Tom a negro boy aged 7 years.

		if 'Paste the Web address (URL)' in row:
			rowData['URL']=row['Paste the Web address (URL)']
		else:
			rowData['URL']=""
		rowData['TranscriberFirstName']=None
		rowData['TranscriberLastName']=None
		# try:
		Transcriber=row['Name of Transcriber, School Initials, Semester Year (ex. John Smith, NSU, Spring 2022)']
		rowData['TranscriberFirstName']=Transcriber.split(" ")[0]
		rowData['TranscriberLastName']=Transcriber.split(" ")[1:]
		rowData['TranscriberLastName']=' '.join(rowData['TranscriberLastName'])
		# except KeyError:
		#	 print("Key 'Name of Transcriber' not found in row.", str(KeyError()))
		#	 Transcriber=""
		# except Exception as e:
		#	 Transcriber=""
		#	 print("An error occurred:", str(e))
		
		rows.append(rowData)
		

	return rows



