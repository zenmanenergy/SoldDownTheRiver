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
            voyagehumans.RoleId,
            voyages.StartDate,
            voyages.EndDate,
            locations.city, locations.State,
            endLocations.City AS EndCity,
            endLocations.State AS EndState,
            ships.ShipName
        FROM 
            voyagehumans
        JOIN 
            voyages ON voyagehumans.VoyageId = voyages.VoyageId
        JOIN locations ON locations.LocationId = voyages.StartLocationId
        JOIN locations AS endLocations ON endLocations.LocationId = voyages.EndLocationId
        JOIN ships ON ships.ShipId = voyages.ShipId
        WHERE 
            voyagehumans.HumanId = %s
    """

    # Print the SQL query with the actual HumanId value
    # print(query)

    # Execute the query and get the results
    cursor.execute(query, (HumanId,))
    result = cursor.fetchall()
    if not result:
        result = []

    # Close the database connection
    connection.close()

    # Return the result as a dictionary
    return result
