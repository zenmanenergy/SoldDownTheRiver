from Lib import Database

def get_transaction(transaction_id):
    if not transaction_id:
        transaction_id = "-1"

    # Connect to the database
    cursor, connection = Database.ConnectToDatabase()

    # Construct the SQL query
    query = "SELECT *, (select max(dateAdded) from History where History.KeyValue=Transactions.TransactionId  and History.TableName='Transactions' and History.KeyName='TransactionId') LastModified"
    query +=" FROM Transactions WHERE TransactionId = %s"
    values = (transaction_id,)

    # Execute the query and get the results
    cursor.execute(query, values)
    result = cursor.fetchone()
    if not result:
        result = {}

    # Close the database connection
    connection.close()

    # Return the result as a dictionary
    return result
