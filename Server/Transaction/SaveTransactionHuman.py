import uuid
from Lib import Database
import datetime

def save_transactionhuman(TransactionId, HumanId):
    
    # Connect to the database
    cursor, connection = Database.ConnectToDatabase()
    


    
    query = "INSERT INTO TransactionHumans (TransactionId, HumanId) VALUES (%s, %s)"
    values = (TransactionId, HumanId)

    print(query.format(*values))

    # Execute the query and commit the changes
    cursor.execute(query, values)
    connection.commit()

    # Close the database connection 
    connection.close()

    # Return the TransactionId as a JSON response
    return {'success': True, 'TransactionId:HumanId': TransactionId+": "+HumanId}
