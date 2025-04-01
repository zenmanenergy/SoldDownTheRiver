from _Lib import Database

def get_VoyageHumans(VoyageId):
  

	# Connect to the database
	cursor, connection = Database.ConnectToDatabase()

	# Construct the SQL sql
	sql = "SELECT humans.*, voyagehumans.*,voyagehumans.notes as VoyageNotes, roles.RoleId,roles.Role  "
	sql +=" from humans join voyagehumans on humans.HumanId=voyagehumans.HumanId "
	sql +=" left join roles on voyagehumans.RoleId=roles.RoleId "
	sql +=f" where voyagehumans.VoyageId='{VoyageId}' order by Firstname, Lastname"

	print(sql)
	cursor.execute(sql)
	result = cursor.fetchall()
	if not result:
		result = []

	# Close the database connection
	connection.close()
	# Return the result as a dictionary
	return result
