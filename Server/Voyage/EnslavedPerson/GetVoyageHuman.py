from _Lib import Database

def get_VoyageHuman(VoyageId,HumanId):
  

	# Connect to the database
	cursor, connection = Database.ConnectToDatabase()

	# Construct the SQL sql
	sql = "SELECT humans.*, voyagehumans.*, roles.RoleId,roles.Role  "
	sql +=" from humans join voyagehumans on humans.HumanId=voyagehumans.HumanId "
	sql +=" left join roles on voyagehumans.RoleId=roles.RoleId "
	sql +=f" where voyagehumans.VoyageId='{VoyageId}' and voyagehumans.HumanId='{HumanId}' order by Firstname, Lastname"

	print(sql)
	cursor.execute(sql)
	result = cursor.fetchone()
	if not result:
		result = []

	# Close the database connection
	connection.close()
	# Return the result as a dictionary
	return result
