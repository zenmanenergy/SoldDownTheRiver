
# Add a comment
from .Database import ConnectToDatabase
import json
import uuid
import pymysql
import pymysql.cursors
from pymysql.constants import CLIENT
import datetime



def SaveHistory(Data, Table, PKName,PKValue ):
    # Add a comment
    Cursor,Connection=ConnectToDatabase()
    
    if not PKValue:
        PKValue=Data['PKName']

    # Construct the SQL query
    query = "SELECT UserId FROM UserSessions WHERE SessionId = %s"
    values = (Data["SessionId"])


    # Execute the query and get the results
    Cursor.execute(query, values)
    result = Cursor.fetchone()

    if not result:
        return False

    # Convert the TransactionDate string into a datetime object
    now = datetime.datetime.now()
    now_str = now.strftime('%Y-%m-%d %H:%M:%S')
    HistoryId="HIS"+str(uuid.uuid4())
    query="INSERT INTO History (HistoryId, TableName, PKName, PKValue,UserId,  Data,DateAdded) VALUES (%s,%s,%s,%s,%s,%s,%s)"
    values=(HistoryId, Table, PKName, PKValue, PKValue, json.dumps(Data),now_str)
    print(query % tuple(map(repr, values)))
    # Add a comment
    Cursor.execute(query,values)
    
    # Add a comment
    Connection.commit()
    
    # Add a comment
    Cursor.close()
    
    # Add a comment
    Connection.close()
    
    # Add a comment
    return True
    