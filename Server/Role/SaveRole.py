import uuid
from Lib import Database
from icecream import ic

def save_role(RoleId,Role):
	# Connect to the database
	cursor, connection = Database.ConnectToDatabase()

	
	ic(RoleId,Role)
	sql=""
	
	# If the role doesn't exist, create a new row with a new role ID
	sql = f"INSERT INTO Roles (RoleId, Role) VALUES ('{RoleId}','{Role}')"
	sql +=" ON DUPLICATE KEY UPDATE RoleId=values(RoleId),Role=values(Role) "


	ic(sql)
	# Execute the sql and commit the changes
	cursor.execute(sql)
	connection.commit()

	# Close the database connection
	connection.close()

	# Return the role as a JSON response
	return {'success': True, 'RoleId': RoleId}
