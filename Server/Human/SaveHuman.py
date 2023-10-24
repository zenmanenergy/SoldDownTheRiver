import uuid
from Lib import Database

def save_human(HumanId, FirstName, MiddleName, LastName, Notes):
	# Connect to the database
	cursor, connection = Database.ConnectToDatabase()

	# Check if the HumanId is present
	if HumanId:
		# If the HumanId is present, update the existing human
		query = "UPDATE Humans SET FirstName = %s, MiddleName = %s, LastName = %s,  Notes = %s WHERE HumanId = %s"
		values = (FirstName, MiddleName, LastName,  Notes, HumanId)
	else:
		# If the HumanId is not present, create a new human
		HumanId = "HUM"+str(uuid.uuid4())
		query = "INSERT INTO Humans (HumanId, FirstName, MiddleName, LastName,  Notes) VALUES (%s, %s, %s, %s, %s)"
		query +="  ON DUPLICATE KEY UPDATE FirstName=values(FirstName),MiddleName=values(MiddleName),LastName=values(LastName),Notes=values(Notes)"
		values = (HumanId, FirstName, MiddleName, LastName, Notes)

	
	# Execute the query and commit the changes
	cursor.execute(query, values)
	connection.commit()

	

	# Return the HumanId as a JSON response
	return {'success': True, 'HumanId': HumanId}
