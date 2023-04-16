import uuid
from Lib import Database

def save_location(LocationId, City, State, Country, Latitude, Longitude):
    # Connect to the database
    cursor, connection = Database.ConnectToDatabase()

    # Check if the LocationId is present
    if LocationId:
        # If the LocationId is present, update the existing location
        query = "UPDATE Locations SET City = %s, State = %s, Country = %s, Latitude = %s, Longitude = %s WHERE LocationId = %s"
        values = (City, State, Country, Latitude, Longitude, LocationId)
    else:
        # If the LocationId is not present, create a new location
        LocationId = str(uuid.uuid4())
        query = "INSERT INTO Locations (LocationId, City, State, Country, Latitude, Longitude) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (LocationId, City, State, Country, Latitude, Longitude)

    # Execute the query and commit the changes
    cursor.execute(query, values)
    connection.commit()

    # Close the database connection
    connection.close()

    # Return the LocationId as a JSON response
    return {'success': True, 'LocationId': LocationId}
