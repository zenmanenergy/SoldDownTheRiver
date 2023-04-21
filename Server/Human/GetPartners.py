from Lib import Database

def get_partners(HumanId):
    if not HumanId:
        HumanId="-1"
    
    # Connect to the database
    cursor, connection = Database.ConnectToDatabase()

    # Construct the SQL query
    query = "SELECT * FROM Partners join Humans on Humans.HumanId=Partners.PartnerHumanId WHERE Partners.HumanId = %s"
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
