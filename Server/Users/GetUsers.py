from Lib import Database

def get_users():
    
    # Connect to the database
    cursor, connection = Database.ConnectToDatabase()

    # Construct the SQL query
    query = "SELECT * FROM Users ORDER BY LastName, FirstName"
    values = ()

    # Execute the query and get the results
    cursor.execute(query, values)
    result = cursor.fetchall()
    if not result:
        result = []

    # Close the database connection
    connection.close()

    # Return the result
    return result
