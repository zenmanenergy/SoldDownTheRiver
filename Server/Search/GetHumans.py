from Lib import Database

def get_humans(FirstName, LastName):
    
    
    # Connect to the database
    cursor, connection = Database.ConnectToDatabase()

    # Construct the SQL query
    query = "SELECT *"
    query += " FROM Humans WHERE FirstName like %s and LastName like %s"
    values = (FirstName + '%', LastName + '%')


    # Execute the query and get the results
    cursor.execute(query, values)
    result = cursor.fetchall()
    if not result:
        result=[]
        
    # Close the database connection
    connection.close()
    
    # Return the result as a dictionary
    return result
