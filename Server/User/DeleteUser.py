from _Lib import Database

def delete_user(user_id):
	# Delete the specified row from the Users table
	query = f"DELETE from users WHERE UserId = '{user_id}'"
	cursor, connection = Database.ConnectToDatabase()
	cursor.execute(query)
	connection.commit()
	connection.close()

	return {'success': True,'message': f'User with ID {user_id} deleted successfully.'}
