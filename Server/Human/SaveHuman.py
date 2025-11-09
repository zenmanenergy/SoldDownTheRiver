import uuid
from _Lib import Database

def convert_empty_to_none(val):
	return None if val == "" else val

def save_human(HumanId, FirstName, MiddleName, LastName, isCompany, BirthDate, BirthDateAccuracy, 
			   RacialDescriptor, Sex, Height_cm, Notes, age_string=None, 
			   BirthPlace=None, originCity=None, physical_features=None, 
			   profession=None, mergedHumanId=None, spouseHumanId=None, isApproved=False):
	# Connect to the database
	cursor, connection = Database.ConnectToDatabase()

	# Convert empty strings to None for all parameters
	HumanId = convert_empty_to_none(HumanId)
	FirstName = convert_empty_to_none(FirstName)
	MiddleName = convert_empty_to_none(MiddleName)
	LastName = convert_empty_to_none(LastName)
	isCompany = convert_empty_to_none(isCompany)
	BirthDate = convert_empty_to_none(BirthDate)
	BirthDateAccuracy = convert_empty_to_none(BirthDateAccuracy)
	RacialDescriptor = convert_empty_to_none(RacialDescriptor)
	Sex = convert_empty_to_none(Sex)
	Height_cm = convert_empty_to_none(Height_cm)
	Notes = convert_empty_to_none(Notes)
	age_string = convert_empty_to_none(age_string)
	BirthPlace = convert_empty_to_none(BirthPlace)
	originCity = convert_empty_to_none(originCity)
	physical_features = convert_empty_to_none(physical_features)
	profession = convert_empty_to_none(profession)
	mergedHumanId = convert_empty_to_none(mergedHumanId)
	spouseHumanId = convert_empty_to_none(spouseHumanId)
	
	# Convert isApproved to boolean (ensure it's either 0 or 1)
	isApproved = 1 if str(isApproved).lower() in ["true", "1", "yes"] else 0

	if HumanId:
		query = """
			UPDATE humans 
			SET FirstName = %s, MiddleName = %s, LastName = %s, isCompany=%s, BirthDate = %s, BirthDateAccuracy = %s, 
				RacialDescriptor = %s, Sex = %s, Height_cm = %s, Notes = %s, 
				age_string = %s, BirthPlace = %s, originCity = %s, physical_features = %s, 
				profession = %s, mergedHumanId = %s, spouseHumanId = %s, isApproved = %s, DateUpdated = NOW() 
			WHERE HumanId = %s
		"""
		values = (FirstName, MiddleName, LastName, isCompany, BirthDate, BirthDateAccuracy, RacialDescriptor, Sex, Height_cm, 
				  Notes, age_string, BirthPlace, originCity, physical_features, profession, mergedHumanId, spouseHumanId, isApproved, HumanId)
	else:
		HumanId = "HUM" + str(uuid.uuid4())
		query = """
			INSERT INTO humans (HumanId, FirstName, MiddleName, LastName, isCompany, BirthDate, BirthDateAccuracy, 
				RacialDescriptor, Sex, Height_cm, Notes, age_string, BirthPlace, originCity, 
				physical_features, profession, mergedHumanId, spouseHumanId, isApproved, DateUpdated) 
			VALUES (%s, %s, %s, %s, %s, %s, %s, %s,  %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
			ON DUPLICATE KEY UPDATE 
				FirstName = VALUES(FirstName), MiddleName = VALUES(MiddleName), LastName = VALUES(LastName), isCompany = VALUES(isCompany), 
				BirthDate = VALUES(BirthDate), BirthDateAccuracy = VALUES(BirthDateAccuracy), 
				RacialDescriptor = VALUES(RacialDescriptor), Sex = VALUES(Sex), 
				Height_cm = VALUES(Height_cm), Notes = VALUES(Notes), 
				age_string = VALUES(age_string), BirthPlace = VALUES(BirthPlace), originCity = VALUES(originCity), 
				physical_features = VALUES(physical_features), profession = VALUES(profession), 
				mergedHumanId = VALUES(mergedHumanId), spouseHumanId = VALUES(spouseHumanId), isApproved = VALUES(isApproved), DateUpdated = NOW()
		"""
		values = (HumanId, FirstName, MiddleName, LastName, isCompany, BirthDate, BirthDateAccuracy, RacialDescriptor, Sex, Height_cm, 
				  Notes, age_string, BirthPlace, originCity, physical_features, profession, mergedHumanId, spouseHumanId, isApproved)

	cursor.execute(query, values)
	connection.commit()

	return {'success': True, 'HumanId': HumanId}
