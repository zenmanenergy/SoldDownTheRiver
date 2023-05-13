from Lib import Database

def delete_ship(ship_id):
    # Delete the specified row from the Ships table
    query = f"DELETE FROM Ships WHERE ShipId = '{ship_id}'"
    cursor, connection = Database.ConnectToDatabase()
    cursor.execute(query)
    connection.commit()
    connection.close()

    return {'success': True, 'message': f'Ship with ID {ship_id} deleted successfully.'}
