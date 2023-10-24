
from Lib import Database

def get_SlaveTraders():
	# Connect to the database
	cursor, connection = Database.ConnectToDatabase()

	# Construct the SQL sql
	sql = f"SELECT * "
	sql += f"  FROM Humans join HumanRoles on Humans.HumanId=HumanRoles.HumanId where HumanRoles.RoleId='SlaveTrader'"
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
