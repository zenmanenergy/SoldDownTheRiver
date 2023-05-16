import uuid
from Lib import Database
import datetime

def save_VoyageHuman(VoyageId, HumanId):
    
    # Connect to the database
    cursor, connection = Database.ConnectToDatabase()
    


    
    query = "INSERT INTO VoyageHumans (VoyageId, HumanId) VALUES (%s, %s)"
    query +=" ON DUPLICATE KEY UPDATE VoyageId=values(VoyageId),HumanId=values(HumanId)"
        
    values = (VoyageId, HumanId,)

    print(query % values)

    # Execute the query and commit the changes
    cursor.execute(query, values)
    connection.commit()

    # Close the database connection 
    connection.close()

    # Return the VoyageId as a JSON response
    return {'success': True, 'VoyageId:HumanId': VoyageId+":"+HumanId}
