from _Lib import Database

def get_humans(Search):

	# Connect to the database
	cursor, connection = Database.ConnectToDatabase()

	# Construct the SQL query
	query = f"SELECT h.HumanId, h.FirstName, h.MiddleName, h.LastName, h.BirthDate, h.BirthDateAccuracy, "
	query += f" h.RacialDescriptor, h.Sex, h.Height_cm,  "
	query += f" GROUP_CONCAT(r.Role ORDER BY r.Role SEPARATOR ', ') AS Roles "
	query += f" FROM humans h "
	query += f" LEFT JOIN humanroles hr ON h.HumanId = hr.HumanId "
	query += f" LEFT JOIN roles r ON hr.RoleId = r.RoleId "
	
	query +=f" where 1=1 "
	if Search:
		query +=f" and FirstName='{Search}'"
	query += f" GROUP BY h.HumanId; "

	
	query += f" order by LastName, FirstName, MiddleName"
	

	cursor.execute(query)
	result = cursor.fetchall()
	if not result:
		result=[]
		
	# Close the database connection
	connection.close()

	# Return the result as a dictionary
	return result