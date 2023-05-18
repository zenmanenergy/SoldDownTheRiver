import uuid
from Lib import Database
import datetime

def save_VoyageHuman(VoyageId, HumanId, RoleId, Notes):
    
    # Connect to the database
    cursor, connection = Database.ConnectToDatabase()
    


    
    query = "INSERT INTO VoyageHumans (VoyageId, HumanId, RoleId, Notes) VALUES (%s, %s,%s, %s)"
    query +=" ON DUPLICATE KEY UPDATE VoyageId=values(VoyageId),HumanId=values(HumanId) ,RoleId=values(RoleId), Notes=values(Notes)"
        
    values = (VoyageId, HumanId,RoleId, Notes,)

    print(query % values)

    # Execute the query and commit the changes
    cursor.execute(query, values)
    connection.commit()

    # Close the database connection 
    connection.close()

    # Return the VoyageId as a JSON response
    return {'success': True, 'VoyageId:HumanId': VoyageId+":"+HumanId}
