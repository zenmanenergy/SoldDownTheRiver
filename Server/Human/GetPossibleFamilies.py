from _Lib import Database

def get_possible_Families(HumanId):
	# Connect to the database
	cursor, connection = Database.ConnectToDatabase()

	# Construct the SQL query
	query = "SELECT * from humans where HumanId<>%s and HumanId not in (select FamilyHumanId from families where families.HumanId=%s) order by LastName, FirstName"
	values = (HumanId,HumanId)

	# Execute the query and get the results
	cursor.execute(query, values)
	result = cursor.fetchall()
	if not result:
		result=[]
		
	# Close the database connection
	connection.close()

	# Return the result as a dictionary
	return result