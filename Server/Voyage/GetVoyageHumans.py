from Lib import Database

def get_VoyageHumans(VoyageId):
  

	# Connect to the database
	cursor, connection = Database.ConnectToDatabase()

	# Construct the SQL sql
	sql = "SELECT Humans.*, VoyageHumans.*,VoyageHumans.notes as VoyageNotes, Roles.RoleId,Roles.Role  "
	sql +=" FROM Humans join VoyageHumans on Humans.HumanId=VoyageHumans.HumanId "
	sql +=" left join Roles on VoyageHumans.RoleId=Roles.RoleId "
	sql +=f" where VoyageHumans.VoyageId='{VoyageId}' order by Firstname, Lastname"

	print(sql)
	cursor.execute(sql)
	result = cursor.fetchall()
	if not result:
		result = []

	# Close the database connection
	connection.close()
	# Return the result as a dictionary
	return result
