from Lib import Database

def delete_Voyage(Voyage_id):
    # Delete the specified row from the Voyages table
    query = f"DELETE FROM Voyages WHERE VoyageId = '{Voyage_id}'"
    cursor, connection = Database.ConnectToDatabase()
    cursor.execute(query)
    connection.commit()
    connection.close()

    return {'success': True, 'message': f'Voyage with ID {Voyage_id} deleted successfully.'}
