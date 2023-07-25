from Lib import Database

def get_transactions():
    
    # Connect to the database
    cursor, connection = Database.ConnectToDatabase()

    # Construct the SQL query
    query = "SELECT Transactions.*, FromBusiness.BusinessName FromBusinessName, ToBusinesses.BusinessName ToBusinessName, (select max(dateAdded) from History where History.KeyValue=Transactions.TransactionId  and History.TableName='Transactions' and History.KeyName='TransactionId') LastModified"
    query +=" FROM Transactions join Businesses FromBusiness on Transactions.FromBusinessId=FromBusiness.BusinessId"
    query +=" join Businesses ToBusinesses on Transactions.ToBusinessId=ToBusinesses.BusinessId"
    query +=" ORDER BY TransactionDate DESC"
    query +=" limit 50"
    values = ()

    print(query % values)
    # Execute the query and get the results
    cursor.execute(query, values)
    result = cursor.fetchall()
    if not result:
        result = []

    # Close the database connection
    connection.close()

    # Return the result as a list of dictionaries
    return result
 