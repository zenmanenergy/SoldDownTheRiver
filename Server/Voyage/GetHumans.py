
from Lib import Database

def get_Humans(VoyageId):
    # Connect to the database
    cursor, connection = Database.ConnectToDatabase()

    # Construct the SQL query
    query = "SELECT * "
    query += "  FROM Humans where Humans.HumanId not in (select HumanId from VoyageHumans where VoyageHumans.VoyageId=%s ) "
    query += " ORDER BY FirstName, LastName"
    values = (VoyageId, )

    # Execute the query and get the results
    cursor.execute(query, values)
    result = cursor.fetchall()
    if not result:
        result = []

    # Close the database connection
    connection.close()

    # Return the result
    return result
