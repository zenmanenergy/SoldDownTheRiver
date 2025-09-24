from _Lib import Database
from datetime import datetime

def get_humans(Search=None, LastFetchTime=None):
	# Connect to the database
	cursor, connection = Database.ConnectToDatabase()

	# Construct the SQL query
	query = """
		SELECT h.HumanId, h.FirstName, h.MiddleName, h.LastName, h.isCompany, h.BirthDate, h.BirthDateAccuracy,
			   h.RacialDescriptor, h.Sex, 
			   GROUP_CONCAT(CONCAT_WS(' ', ha.AKAFirstName, ha.AKAMiddleName, ha.AKALastName) ORDER BY ha.AKAHumanId SEPARATOR ', ') AS AlsoKnownAs,
			   GROUP_CONCAT(DISTINCT AllRoles.RoleId) AS Roles
		FROM humans h
		LEFT JOIN humansaka ha ON h.HumanId = ha.HumanId
		LEFT JOIN (
			SELECT HumanId, RoleId FROM transactionhumans
			UNION
			SELECT HumanId, RoleId FROM voyagehumans
		) AllRoles ON h.HumanId = AllRoles.HumanId
		WHERE 1=1
	"""
	values = []

	# Add search filter if provided
	if Search:
		query += " AND h.FirstName = %s"
		values.append(Search)









	# Add LastFetchTime filter if provided and valid
	if LastFetchTime:
		try:
			# Convert ISO 8601 format to '%Y-%m-%d %H:%M:%S'
			LastFetchTime = datetime.fromisoformat(LastFetchTime.replace("Z", "+00:00")).strftime('%Y-%m-%d %H:%M:%S')
			query += " AND h.DateUpdated > %s"
			values.append(LastFetchTime)
		except ValueError:
			print("Invalid LastFetchTime format. Skipping filter.")

	query += """
		GROUP BY h.HumanId
		ORDER BY h.LastName, h.FirstName, h.MiddleName
		
	"""
	print(query)
	# Debugging: Print the query and values for troubleshooting
	# print("Executing query:", query)
	# print("With values:", values)

	# Execute the query
	cursor.execute(query, values)
	result = cursor.fetchall()
	if not result:
		result = []

	# Close the database connection
	connection.close()

	# Return the result as a dictionary
	return result

def search_humans(Query=None, LastFetchTime=None):
	cursor, connection = Database.ConnectToDatabase()
	query = """
		SELECT h.HumanId, h.FirstName, h.MiddleName, h.LastName, h.isCompany, h.BirthDate, h.BirthDateAccuracy,
		       h.RacialDescriptor, h.Sex, h.Height_cm,
		       GROUP_CONCAT(CONCAT_WS(' ', ha.AKAFirstName, ha.AKAMiddleName, ha.AKALastName) ORDER BY ha.AKAHumanId SEPARATOR ', ') AS AlsoKnownAs
		FROM humans h
		LEFT JOIN humansaka ha ON h.HumanId = ha.HumanId
		WHERE 1=1
		
	"""
	values = []

	if Query:
		like = f"%{Query}%"
		query += """
			AND (
				h.FirstName LIKE %s OR
				h.LastName LIKE %s OR
				h.HumanId LIKE %s OR
				h.RacialDescriptor LIKE %s OR
				h.Sex LIKE %s OR
				h.BirthDate LIKE %s OR
				h.BirthDateAccuracy LIKE %s
			)
		"""
		values.extend([like, like, like, like, like, like, like])

	if LastFetchTime:
		try:
			LastFetchTime = datetime.fromisoformat(LastFetchTime.replace("Z", "+00:00")).strftime('%Y-%m-%d %H:%M:%S')
			query += " AND h.DateUpdated > %s"
			values.append(LastFetchTime)
		except ValueError:
			print("Invalid LastFetchTime format. Skipping filter.")

	query += """
		GROUP BY h.HumanId
		ORDER BY h.LastName, h.FirstName, h.MiddleName
	"""

	# print("Executing search query:", query)
	# print("With values:", values)

	cursor.execute(query, values)
	result = cursor.fetchall()
	if not result:
		result = []

	connection.close()
	return result