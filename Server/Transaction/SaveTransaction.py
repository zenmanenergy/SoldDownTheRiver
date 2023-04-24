import uuid
from Lib import Database
import datetime

def save_transaction(TransactionId, TransactionDate, FromHumanId, ToHumanId, TransactionType, Notes, Act, Page, NotaryHumanId, Volume, URL):
    # Connect to the database
    cursor, connection = Database.ConnectToDatabase()

    # Convert the TransactionDate string into a datetime object
    TransactionDate = datetime.datetime.strptime(TransactionDate, '%a, %d %b %Y %H:%M:%S %Z')

    # Format the datetime object into a string in the format that MySQL expects
    TransactionDate_str = TransactionDate.strftime('%Y-%m-%d %H:%M:%S')

    # Check if the TransactionId is present
    if TransactionId:
        # If the TransactionId is present, update the existing transaction
        query = "UPDATE Transactions SET TransactionDate = %s, FromHumanId = %s, ToHumanId = %s, TransactionType = %s, Notes = %s, Act = %s, Page = %s, NotaryHumanId = %s, Volume = %s, URL = %s WHERE TransactionId = %s"
        values = (TransactionDate_str, FromHumanId, ToHumanId, TransactionType, Notes, Act, Page, NotaryHumanId, Volume, URL, TransactionId)
    else:
        # If the TransactionId is not present, create a new transaction
        TransactionId = "TRN"+str(uuid.uuid4())
        query = "INSERT INTO Transactions (TransactionId, TransactionDate, FromHumanId, ToHumanId, TransactionType, Notes, Act, Page, NotaryHumanId, Volume, URL) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (TransactionId, TransactionDate_str, FromHumanId, ToHumanId, TransactionType, Notes, Act, Page, NotaryHumanId, Volume, URL)

    # Execute the query and commit the changes
    cursor.execute(query, values)
    connection.commit()

    # Close the database connection 
    connection.close()

    # Return the TransactionId as a JSON response
    return {'success': True, 'TransactionId': TransactionId}
