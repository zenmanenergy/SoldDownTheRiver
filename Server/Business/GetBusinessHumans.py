from Lib import Database

def get_BusinessHumans(BusinessId):

    # Connect to the database
    cursor, connection = Database.ConnectToDatabase()

    # Construct the SQL query
    query = "SELECT *, (select max(dateAdded) from History where History.KeyValue=Humans.HumanId and History.TableName='Humans' and History.KeyName='HumanId') LastModified"
    query +=" FROM Humans join BusinessHumans on Humans.HumanId=BusinessHumans.HumanId "
    query +=" join Roles on BusinessHumans.RoleId=Roles.RoleId "
    query +=" where BusinessHumans.BusinessId= %s "
    query +=" order by Humans.LastName, Humans.FirstName"
    values = (BusinessId,)

    print(query % values)
    # Execute the query and get the results
    cursor.execute(query, values)
    result = cursor.fetchall()
    if not result:
        result=[]
        
    # Close the database connection
    connection.close()

    # Return the result as a dictionary
    return result