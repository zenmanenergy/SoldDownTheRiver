from _Lib import Database

def delete_role(RoleId):
	# Delete the specified row from the Roles table
	query = f"DELETE from roles WHERE RoleId = '{RoleId}'"
	cursor, connection = Database.ConnectToDatabase()
	cursor.execute(query)
	connection.commit()

	
	connection.close()

	return {'success': True,'message': f'Role "{RoleId}" deleted successfully.'}
