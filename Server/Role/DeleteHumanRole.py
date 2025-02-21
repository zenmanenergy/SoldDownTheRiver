from _Lib import Database

def delete_HumanRole(HumanId,RoleId):
	# Delet
	# e the specified row from the Roles table
	sql = f"DELETE from humanroles WHERE RoleId = '{RoleId}' and HumanId='{HumanId}'"
	cursor, connection = Database.ConnectToDatabase()
	print(sql)
	cursor.execute(sql)
	connection.commit()

	
	connection.close()

	return {'success': True,'message': f'Role "{RoleId}" deleted successfully.'}
