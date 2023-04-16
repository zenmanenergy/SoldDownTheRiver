from Lib import Database

def get_businesses():
    
    # Connect to the database
    cursor, connection = Database.ConnectToDatabase()

    # Construct the SQL query
    query = "SELECT * FROM Businesses order by BusinessName"
    values = ()


    # Execute the query and get the results
    cursor.execute(query, values)
    result = cursor.fetchall()
    if not result:
        result=[]
        
    # Close the database connection
    connection.close()
    
    # Return the result as a dictionary
    return result