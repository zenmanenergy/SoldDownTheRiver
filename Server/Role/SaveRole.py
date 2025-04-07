import uuid
from _Lib import Database

def save_role(RoleId, Role):
	# Remove spaces from Role if RoleId is empty
	if not RoleId.strip():
		RoleId = Role.replace(" ", "")

	# Connect to the database
	cursor, connection = Database.ConnectToDatabase()

	# SQL statement for insert or update
	sql = f"""
		INSERT into roles (RoleId, Role, DateUpdated)
		VALUES ('{RoleId}', '{Role}', NOW())
		ON DUPLICATE KEY update Role=VALUES(Role), DateUpdated=NOW()
	"""
	
	# Execute the SQL and commit the changes
	cursor.execute(sql)
	connection.commit()

	# Close the database connection
	connection.close()

	# Return the role as a JSON response
	return {'success': True, 'RoleId': RoleId}
