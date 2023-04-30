from Lib import Database

def get_Familys(HumanId):
    if not HumanId:
        HumanId="-1"
    
    # Connect to the database
    cursor, connection = Database.ConnectToDatabase()

    # Construct the SQL query
    query = "SELECT * FROM Familys join Humans on Humans.HumanId=Familys.FamilyHumanId WHERE Familys.HumanId = %s"
    values = (HumanId,)
    print(query, values)
    # Execute the query and get the results
    cursor.execute(query, values)
    result = cursor.fetchall()
    if not result:
        result={}
        
    # Close the database connection
    connection.close()
    
    # Return the result as a dictionary
    return result
