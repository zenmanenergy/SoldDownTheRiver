
from _Lib import Database

def get_SlaveTraders():
	# Connect to the database
	cursor, connection = Database.ConnectToDatabase()

	# Construct the SQL sql
	sql = f"SELECT * "
	sql += f"  from humans join humanroles on humans.HumanId=humanroles.HumanId where humanroles.RoleId='SlaveTrader'"
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
