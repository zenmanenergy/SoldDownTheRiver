from Lib import Database

def get_VoyageHumans(VoyageId):
  

    # Connect to the database
    cursor, connection = Database.ConnectToDatabase()

    # Construct the SQL query
    query = "SELECT Humans.*, VoyageHumans.*,VoyageHumans.notes as VoyageNotes FROM Humans join VoyageHumans on Humans.HumanId=VoyageHumans.HumanId where VoyageHumans.VoyageId=%s order by Firstname, Lastname"
    values = (VoyageId,)
    # Execute the query and get the results

    # print(query % values)
    cursor.execute(query, values)
    result = cursor.fetchall()
    if not result:
        result = []

    # Close the database connection
    connection.close()
    # Return the result as a dictionary
    return result
