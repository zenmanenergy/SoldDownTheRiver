from Lib import Database

def get_roles():
    
    # Connect to the database
    cursor, connection = Database.ConnectToDatabase()

    # Construct the SQL query
    query = "SELECT RoleId,Role, (select max(dateAdded) from History where History.KeyValue=Roles.RoleId  and History.TableName='Roles' and History.KeyName='RoleId') LastModified"
    query +=" FROM Roles ORDER BY Role"
    values = ()

    print(query)
    # Execute the query and get the results
    cursor.execute(query, values)
    result = cursor.fetchall()
    if not result:
        result = []
        
    # Close the database connection
    connection.close()
    
    # Return the result as a dictionary
    return result
