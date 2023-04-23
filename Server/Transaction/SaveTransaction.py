import uuid
from Lib import Database

def save_transaction(TransactionId, TransactionDate, FromHumanId, ToHumanId, TransactionType, Notes, Act, Page, NotaryHumanId, Volume, URL, UserId):
    # Connect to the database
    cursor, connection = Database.ConnectToDatabase()

    # Check if the TransactionId is present
    if TransactionId:
        # If the TransactionId is present, update the existing transaction
        query = "UPDATE Transactions SET TransactionDate = %s, FromHumanId = %s, ToHumanId = %s, TransactionType = %s, Notes = %s, Act = %s, Page = %s, NotaryHumanId = %s, Volume = %s, URL = %s, UserId = %s WHERE TransactionId = %s"
        values = (TransactionDate, FromHumanId, ToHumanId, TransactionType, Notes, Act, Page, NotaryHumanId, Volume, URL, UserId, TransactionId)
    else:
        # If the TransactionId is not present, create a new transaction
        TransactionId = "TRN"+str(uuid.uuid4())
        query = "INSERT INTO Transactions (TransactionId, TransactionDate, FromHumanId, ToHumanId, TransactionType, Notes, Act, Page, NotaryHumanId, Volume, URL, UserId) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (TransactionId, TransactionDate, FromHumanId, ToHumanId, TransactionType, Notes, Act, Page, NotaryHumanId, Volume, URL, UserId)

    # Execute the query and commit the changes
    cursor.execute(query, values)
    connection.commit()

    # Close the database connection 
    connection.close()

    # Return the TransactionId as a JSON response
    return {'success': True, 'TransactionId': TransactionId}
