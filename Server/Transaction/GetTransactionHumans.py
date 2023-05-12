from Lib import Database

def get_transactionHumans(TransactionId):
  

    # Connect to the database
    cursor, connection = Database.ConnectToDatabase()

    # Construct the SQL query
    query = "SELECT Humans.*, TransactionHumans.*,TransactionHumans.notes as TransactionNotes FROM Humans join TransactionHumans on Humans.HumanId=TransactionHumans.HumanId where TransactionHumans.TransactionId=%s order by Firstname, Lastname"
    values = (TransactionId,)
    # Execute the query and get the results

    # print(query % values)
    cursor.execute(query, values)
    result = cursor.fetchall()
    if not result:
        result = []

    # Close the database connection
    connection.close()
    # Return the result as a dictionary
    return result
