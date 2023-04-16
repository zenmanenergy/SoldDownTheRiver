from Lib import Database

def delete_location(location_id):
    # Delete the specified row from the Locations table
    query = f"DELETE FROM Locations WHERE LocationId = '{location_id}'"
    cursor, connection = Database.ConnectToDatabase()
    cursor.execute(query)
    connection.commit()
    connection.close()

    return {'success': True,'message': f'Location with ID {location_id} deleted successfully.'}
