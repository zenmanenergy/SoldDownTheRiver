from Lib import Database

def get_business(BusinessName):
    if not BusinessName:
        BusinessName="-1"
    
    # Connect to the database
    cursor, connection = Database.ConnectToDatabase()

    # Construct the SQL query
    query = "SELECT *"
    query += " FROM Businesses WHERE BusinessName like '"+BusinessName+"%'"
    values = ()

    print(query)

    # Execute the query and get the results
    cursor.execute(query)
    result = cursor.fetchall()
    if not result:
        result=[]
        
    # Close the database connection
    connection.close()
    
    # Return the result as a dictionary
    return result
