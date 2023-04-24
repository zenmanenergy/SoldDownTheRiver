from Lib import Database

def get_to_humans():
  

    # Connect to the database
    cursor, connection = Database.ConnectToDatabase()

    # Construct the SQL query
    query = "SELECT * FROM Humans order by Firstname, lastname"

    # Execute the query and get the results
    cursor.execute(query)
    result = cursor.fetchall()

    # Close the database connection
    connection.close()

    # Return the result as a dictionary
    return result
