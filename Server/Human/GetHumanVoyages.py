from _Lib import Database

def get_human_voyages(HumanId):
    if not HumanId:
        HumanId = "-1"

    # Connect to the database
    cursor, connection = Database.ConnectToDatabase()

    # Construct the SQL query
    query = """
        SELECT 
            voyagehumans.VoyageId,
            voyagehumans.HumanId,
            voyagehumans.Role,
            voyages.Date,
            voyages.Location
        FROM 
            voyagehumans
        INNER JOIN 
            voyages ON voyagehumans.VoyageId = voyages.VoyageId
        WHERE 
            voyagehumans.HumanId = %s
    """

    # Print the SQL query with the actual HumanId value
    print(query)

    # Execute the query and get the results
    cursor.execute(query, (HumanId,))
    result = cursor.fetchall()
    if not result:
        result = []

    # Close the database connection
    connection.close()

    # Return the result as a dictionary
    return result
