import uuid
from _Lib import Database

def save_Family(HumanId, FamilyHumanId, Relationship):
	# Connect to the database
	cursor, connection = Database.ConnectToDatabase()

	# Check if the HumanId is present
	query = "INSERT INTO Families (HumanId, FamilyHumanId,Relationship) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE FamilyHumanId=values(FamilyHumanId),HumanId=values(HumanId),Relationship=values(Relationship)"
	values = (HumanId, FamilyHumanId,Relationship)
	print(query % tuple(map(repr, values))) 
	# Execute the query and commit the changes
	cursor.execute(query, values)
	connection.commit()


	
	OppositeRelationship="Unknown"
	if Relationship=="Father":
		OppositeRelationship="Son"
	elif Relationship=="Mother":
		OppositeRelationship="Daughter"


	# Check if the HumanId is present
	query = "INSERT INTO Families (HumanId, FamilyHumanId,Relationship) VALUES (%s, %s,%s) ON DUPLICATE KEY UPDATE FamilyHumanId=values(FamilyHumanId),HumanId=values(HumanId),Relationship=values(Relationship)"
	values = (FamilyHumanId,HumanId,OppositeRelationship)
	print(query % tuple(map(repr, values)))
	# Execute the query and commit the changes
	cursor.execute(query, values)
	connection.commit()

	# Close the database connection
	connection.close()

	# Return the HumanId as a JSON response
	return {'success': True, 'HumanId': HumanId}
