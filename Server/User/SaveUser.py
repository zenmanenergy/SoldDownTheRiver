import uuid
from _Lib import Database

def save_user(UserId, FirstName, LastName, Email, Phone, Password, School, SemesterYear,UserType):
	# Connect to the database
	cursor, connection = Database.ConnectToDatabase()

	# Check if the UserId is present
	if UserId:
		# If the UserId is present, update the existing user
		query = "update users SET FirstName = %s, LastName = %s, Email = %s, Phone = %s, Password = %s, School = %s, SemesterYear = %s, UserType = %s, DateUpdated = NOW() WHERE UserId = %s"
		values = (FirstName, LastName, Email, Phone, Password, School, SemesterYear, UserType, UserId)
	else:
		# If the UserId is not present, create a new user
		UserId = "USR"+str(uuid.uuid4())
		query = "INSERT into users (UserId, FirstName, LastName, Email, Phone, Password, School, SemesterYear, UserType, DateUpdated) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())"
		values = (UserId, FirstName, LastName, Email, Phone, Password, School, SemesterYear, UserType)

	# Execute the query and commit the changes
	print(query, values)
	cursor.execute(query, values)
	connection.commit()

	# Close the database connection
	connection.close()

	# Return the UserId as a JSON response
	return {'success': True, 'UserId': UserId}
