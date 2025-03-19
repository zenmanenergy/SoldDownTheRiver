
from _Lib import Database

def get_Captains():
	# Connect to the database
	cursor, connection = Database.ConnectToDatabase()

	# Construct the SQL sql
	sql = f"SELECT distinct * "
	sql += f" from humans join voyages on humans.HumanId=voyages.CaptainHumanId "
	sql += f" ORDER BY FirstName, LastName"
	print(sql)
	# Execute the sql and get the results
	cursor.execute(sql)
	result = cursor.fetchall()
	if not result:
		result = []

	# Close the database connection
	connection.close()

	# Return the result
	return result
