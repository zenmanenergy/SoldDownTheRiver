import uuid
from Lib import Database

def save_partner(HumanId, PartnerHumanId):
    # Connect to the database
    cursor, connection = Database.ConnectToDatabase()

    # Check if the HumanId is present
    query = "INSERT INTO Partners (HumanId, PartnerHumanId) VALUES (%s, %s) ON DUPLICATE KEY UPDATE PartnerHumanId=values(PartnerHumanId),HumanId=values(HumanId)"
    values = (HumanId, PartnerHumanId)

    # Execute the query and commit the changes
    cursor.execute(query, values)
    connection.commit()

    # Check if the HumanId is present
    query = "INSERT INTO Partners (HumanId, PartnerHumanId) VALUES (%s, %s) ON DUPLICATE KEY UPDATE PartnerHumanId=values(PartnerHumanId),HumanId=values(HumanId)"
    values = (PartnerHumanId,HumanId)

    # Execute the query and commit the changes
    cursor.execute(query, values)
    connection.commit()

    # Close the database connection
    connection.close()

    # Return the HumanId as a JSON response
    return {'success': True, 'HumanId': HumanId}
