import uuid
from Lib import Database

def save_business(BusinessId, BusinessName, LocationId):
    # Connect to the database
    cursor, connection = Database.ConnectToDatabase()

    # Check if the BusinessId is present
    if BusinessId:
        # If the BusinessId is present, update the existing business
        query = "UPDATE Businesses SET BusinessName = %s, LocationId=%s WHERE BusinessId = %s "
        values = (BusinessName, LocationId, BusinessId)
    else:
        # If the BusinessId is not present, create a new business
        BusinessId = "BUS"+str(uuid.uuid4())
        query = "INSERT INTO Businesses (BusinessId, LocationId, BusinessName) VALUES (%s, %s, %s)"
        values = (BusinessId, LocationId, BusinessName)

    # Execute the query and commit the changes
    cursor.execute(query, values)
    connection.commit()

    # Close the database connection
    connection.close()

    # Return the BusinessId as a JSON response
    return {'success': True, 'BusinessId': BusinessId}