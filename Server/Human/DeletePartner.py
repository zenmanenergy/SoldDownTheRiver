from Lib import Database

def delete_partner(HumanId, PartnerHumanId):
    # Delete the specified row from the Humans table
    query = "DELETE FROM Partners WHERE HumanId = %s and PartnerHumanId = %s"
    values = (HumanId, PartnerHumanId)
    cursor, connection = Database.ConnectToDatabase()
    cursor.execute(query, values)
    connection.commit()
    query = "DELETE FROM Partners WHERE HumanId = %s and PartnerHumanId = %s"
    values = (PartnerHumanId,HumanId)
    cursor, connection = Database.ConnectToDatabase()
    cursor.execute(query, values)
    connection.commit()

    connection.close()

    return {'success': True,'message': f'Human with ID {HumanId} deleted successfully.'}
