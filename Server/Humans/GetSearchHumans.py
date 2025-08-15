from _Lib import Database
from datetime import datetime

def get_search_humans(Search=None, LastFetchTime=None):
	# Connect to the database
	cursor, connection = Database.ConnectToDatabase()

	# Construct the SQL query
	query = """
		SELECT 
			h.HumanId, 
			h.FirstName, 
			h.MiddleName, 
			h.LastName, 
			h.isCompany, 
			h.BirthDate, 
			h.BirthDateAccuracy,
			h.RacialDescriptor, 
			h.Sex, 
			h.Height_cm,
			GROUP_CONCAT(CONCAT_WS(' ', ha.AKAFirstName, ha.AKAMiddleName, ha.AKALastName) ORDER BY ha.AKAHumanId SEPARATOR ', ') AS AlsoKnownAs,
			GROUP_CONCAT(DISTINCT RoleIdAll ORDER BY RoleIdAll SEPARATOR ', ') AS Roles
		FROM humans h
		LEFT JOIN humansaka ha ON h.HumanId = ha.HumanId
		LEFT JOIN (
				SELECT HumanId, RoleId AS RoleIdAll FROM transactionhumans
				UNION
				SELECT HumanId, RoleId AS RoleIdAll FROM voyagehumans
			) roles_all ON h.HumanId = roles_all.HumanId
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
