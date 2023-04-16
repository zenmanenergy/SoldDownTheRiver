from Lib import Database

def delete_business(business_id):
    # Delete the specified row from the Businesses table
    query = f"DELETE FROM Businesses WHERE BusinessId = '{business_id}'"
    cursor, connection = Database.ConnectToDatabase()
    cursor.execute(query)
    connection.commit()
    connection.close()

    return {'success': True,'message': f'Business with ID {business_id} deleted successfully.'}
