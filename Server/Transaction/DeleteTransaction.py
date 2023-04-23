from Lib import Database

def delete_transaction(transaction_id):
    # Delete the specified row from the Transactions table
    query = f"DELETE FROM Transactions WHERE TransactionId = '{transaction_id}'"
    cursor, connection = Database.ConnectToDatabase()
    cursor.execute(query)
    connection.commit()
    connection.close()

    return {'success': True,'message': f'Transaction with ID {transaction_id} deleted successfully.'}
