from Lib import Database

def delete_human(HumanId):
    # Delete the specified row from the Humans table
    query = f"DELETE FROM Humans WHERE HumanId = '{HumanId}'"
    cursor, connection = Database.ConnectToDatabase()
    cursor.execute(query)
    connection.commit()
    connection.close()

    return {'success': True,'message': f'Human with ID {HumanId} deleted successfully.'}
