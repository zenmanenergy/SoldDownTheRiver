import uuid
from _Lib import Database

def save_human(HumanId, FirstName, MiddleName, LastName, BirthDate, BirthDateAccuracy, RacialDescriptor, Sex, Height_cm, Notes, age_string=None, BirthPlace=None, originCity=None, physical_features=None, profession=None, mergedHumanId=None, spouseHumanId=None):
	# Connect to the database
	cursor, connection = Database.ConnectToDatabase()

	# Check if the HumanId is present
	if HumanId:
		# If the HumanId is present, update the existing human
		query = """
			UPDATE humans 
			SET FirstName = %s, MiddleName = %s, LastName = %s, BirthDate = %s, BirthDateAccuracy = %s, 
				RacialDescriptor = %s, Sex = %s, Height_cm = %s, Notes = %s, 
				age_string = %s, BirthPlace = %s, originCity = %s, physical_features = %s, 
				profession = %s, mergedHumanId = %s, spouseHumanId = %s, DateUpdated = NOW() 
			WHERE HumanId = %s
		"""
		values = (FirstName, MiddleName, LastName, BirthDate, BirthDateAccuracy, RacialDescriptor, Sex, Height_cm, Notes, age_string, BirthPlace, originCity, physical_features, profession, mergedHumanId, spouseHumanId, HumanId)
	else:
		# If the HumanId is not present, create a new human
		HumanId = "HUM" + str(uuid.uuid4())
		query = """
			INSERT INTO humans (HumanId, FirstName, MiddleName, LastName, BirthDate, BirthDateAccuracy, 
				RacialDescriptor, Sex, Height_cm, Notes, age_string, BirthPlace, originCity, 
				physical_features, profession, mergedHumanId, spouseHumanId, DateUpdated) 
			VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
			ON DUPLICATE KEY UPDATE 
				FirstName = VALUES(FirstName), MiddleName = VALUES(MiddleName), LastName = VALUES(LastName), 
				BirthDate = VALUES(BirthDate), BirthDateAccuracy = VALUES(BirthDateAccuracy), 
				RacialDescriptor = VALUES(RacialDescriptor), Sex = VALUES(Sex), 
				Height_cm = VALUES(Height_cm), Notes = VALUES(Notes), 
				age_string = VALUES(age_string), BirthPlace = VALUES(BirthPlace), originCity = VALUES(originCity), 
				physical_features = VALUES(physical_features), profession = VALUES(profession), 
				mergedHumanId = VALUES(mergedHumanId), spouseHumanId = VALUES(spouseHumanId), DateUpdated = NOW()
		"""
		values = (HumanId, FirstName, MiddleName, LastName, BirthDate, BirthDateAccuracy, RacialDescriptor, Sex, Height_cm, Notes, age_string, BirthPlace, originCity, physical_features, profession, mergedHumanId, spouseHumanId)

	# Execute the query and commit the changes
	cursor.execute(query, values)
	connection.commit()

	# Return the HumanId as a JSON response
	return {'success': True, 'HumanId': HumanId}
