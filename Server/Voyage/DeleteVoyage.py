from Lib import Database

def delete_voyage(voyage_id):
    # Delete the specified row from the Voyages table
    query = f"DELETE FROM Voyages WHERE VoyageId = '{voyage_id}'"
    cursor, connection = Database.ConnectToDatabase()
    cursor.execute(query)
    connection.commit()
    connection.close()

    return {'success': True, 'message': f'Voyage with ID {voyage_id} deleted successfully.'}
