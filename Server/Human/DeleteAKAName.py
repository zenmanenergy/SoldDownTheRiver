from Lib import Database

def delete_aka(AKAHumanId):
    # Delete the specified row from the Humans table
    query = f"DELETE FROM HumansAKA WHERE AKAHumanId = '{AKAHumanId}'"
    cursor, connection = Database.ConnectToDatabase()
    cursor.execute(query)
    connection.commit()
    connection.close()


    return {'success': True, 'AKAHumanId': AKAHumanId}
