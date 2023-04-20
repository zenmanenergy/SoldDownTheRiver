from Lib import Database

def get_possible_partners(HumanId):
    # Connect to the database
    cursor, connection = Database.ConnectToDatabase()

    # Construct the SQL query
    query = "SELECT * FROM Humans where humanId=%s and humanId not in (select partnerHumanId from partners where partners.humanId=humans.humanId) order by LastName, FirstName"
    values = (HumanId)

    # Execute the query and get the results
    cursor.execute(query, values)
    result = cursor.fetchall()
    if not result:
        result=[]
        
    # Close the database connection
    connection.close()

    # Return the result as a dictionary
    return result