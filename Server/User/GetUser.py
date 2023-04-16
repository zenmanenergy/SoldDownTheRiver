from Lib import Database

def get_user(UserId):
    if not UserId:
        UserId = "-1"
    
    # Connect to the database
    cursor, connection = Database.ConnectToDatabase()

    # Construct the SQL query
    query = "SELECT * FROM Users WHERE UserId = %s"
    values = (UserId,)

    # Execute the query and get the results
    cursor.execute(query, values)
    result = cursor.fetchone()
    if not result:
        result = {}

    # Close the database connection
    connection.close()

    # Return the result as a dictionary
    return result
