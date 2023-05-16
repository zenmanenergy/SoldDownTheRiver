from Lib import Database

def get_Voyage(VoyageId):
    if not VoyageId:
        VoyageId = "-1"
    
    # Connect to the database
    cursor, connection = Database.ConnectToDatabase()

    # Construct the SQL query
    query = "SELECT *, (SELECT MAX(dateAdded) FROM History WHERE History.KeyValue = Voyages.VoyageId AND History.TableName = 'Voyages' AND History.KeyName = 'VoyageId') AS LastModified"
    query += " FROM Voyages WHERE VoyageId = %s"
    values = (VoyageId,)

    # Execute the query and get the results
    cursor.execute(query, values)
    result = cursor.fetchone()
    if not result:
        result = {}

    # Close the database connection
    connection.close()

    # Return the result as a dictionary
    return result
