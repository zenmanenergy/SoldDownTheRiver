from Lib import Database

def get_humans(FirstName, MiddleName, LastName):
    
    
    # Connect to the database
    cursor, connection = Database.ConnectToDatabase()

    # Construct the SQL query
    query = "SELECT *"
    query += " FROM Humans WHERE FirstName like %s and MiddleName like %s and LastName like %s"
    values = (FirstName + '%', MiddleName + '%', LastName + '%')


    # Execute the query and get the results
    cursor.execute(query, values)
    result = cursor.fetchall()
    if not result:
        result=[]
        
    # Close the database connection
    connection.close()
    
    # Return the result as a dictionary
    return result
