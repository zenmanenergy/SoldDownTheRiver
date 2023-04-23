from Lib import Database

def get_login(Email, Password):
    if not Email or not Password:
        Email="-1"
    
    # Connect to the database
    cursor, connection = Database.ConnectToDatabase()

    # Construct the SQL query
    query = "SELECT * FROM Users WHERE Email = %s and Password = %s"
    values = (Email, Password,)


    # Execute the query and get the results
    cursor.execute(query, values)
    result = cursor.fetchone()
    if not result:
        result={}
        
    # Close the database connection
    connection.close()
    
    # Return the result as a dictionary
    return result
