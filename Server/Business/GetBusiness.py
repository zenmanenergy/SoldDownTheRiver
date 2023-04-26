from Lib import Database

def get_business(BusinessId):
    if not BusinessId:
        BusinessId="-1"
    
    # Connect to the database
    cursor, connection = Database.ConnectToDatabase()

    # Construct the SQL query
    query = "SELECT *, (select max(dateAdded) from History where History.KeyValue=Businesses.BusinessId and History.TableName='Business' and History.KeyName='BusinessId') LastModified"
    query += " FROM Businesses WHERE BusinessId = %s"
    values = (BusinessId,)


    # Execute the query and get the results
    cursor.execute(query, values)
    result = cursor.fetchone()
    if not result:
        result={}
        
    # Close the database connection
    connection.close()
    
    # Return the result as a dictionary
    return result
