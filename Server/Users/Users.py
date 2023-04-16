
# Add a comment
from datetime import datetime
import uuid

# Add a comment
from Lib import Database

def TESTINGGetLastUser():
    Cursor,Connection=Database.ConnectToDatabase()

    
    Query = "SELECT * FROM Users ORDER BY UserId DESC LIMIT 1"
    Cursor.execute(Query)

    # Fetch the results and print them out
    
    Response={}
    Response['action']="select"
    Response['rowcount']=Cursor.rowcount
    Response['data']=Cursor.fetchone()
    
    Cursor.close()
    Connection.close()
    return Response


def TESTINGGetLastUserSession():
    Cursor,Connection=Database.ConnectToDatabase()

    
    Query = "SELECT SessionId,DateAdded FROM UserSessions ORDER BY DateAdded DESC LIMIT 1"
    Cursor.execute(Query)

    # Fetch the results and print them out
    
    Response={}
    Response['action']="select"
    Response['rowcount']=Cursor.rowcount
    Response['data']=Cursor.fetchone()
    
    Cursor.close()
    Connection.close()
    return Response

def InsertUser(FirstName, LastName, Email, Password, School, SemesterYear):
    
    # Generate unique user ID
    UserId = "USR" + str(uuid.uuid4()).replace("-", "", -1)

    # Connect to database
    Cursor, Connection = Database.ConnectToDatabase()

    # Define SQL query and parameter values
    Query = "INSERT INTO Users (UserId, FirstName, LastName, Email, Password, School, SemesterYear) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    values = (UserId, FirstName, LastName, Email, Password, School, SemesterYear)
    
    # Execute SQL query and commit changes
    Cursor.execute(Query, values)
    Connection.commit()

    # Define response dictionary
    Response = {}
    Response['UserId'] = UserId
    Response['action'] = "Insert"
    Response['rowcount'] = Cursor.rowcount
    
    # Close database connection and return response dictionary
    Cursor.close()
    Connection.close()
    return Response


def UpdateUser(UserId, FirstName, LastName, Email, Password, School, SemesterYear):
    
    # Connect to database
    Cursor, Connection = Database.ConnectToDatabase()

    # Define SQL query and parameter values
    Query = "UPDATE Users SET FirstName=%s, LastName=%s, Email=%s, Password=%s, School=%s, SemesterYear=%s WHERE UserId=%s"
    values = (FirstName, LastName, Email, Password, School, SemesterYear, UserId)
   
    # Execute SQL query and commit changes
    Cursor.execute(Query, values)
    Connection.commit()

    # Define response dictionary
    Response = {}
    Response['UserId'] = UserId
    Response['action'] = "Update"
    Response['rowcount'] = Cursor.rowcount
    
    # Close database connection and return response dictionary
    Cursor.close()
    Connection.close()
    return Response



# Add a comment
def DeleteUser(UserId):

    # Add a comment
    Cursor,Connection=Database.ConnectToDatabase()

    
    # Add a comment
    Query = "DELETE FROM Users WHERE UserId=%s"
    values = (UserId,)
    
    # Add a comment
    Cursor.execute(Query, values)
    Connection.commit()
    
    # Add a comment
    # sql = Cursor.mogrify(Query, values)
    # print(sql)

    # Add a comment
    Response={}
    Response['UserId']=UserId
    Response['action']="Delete"
    Response['rowcount']=Cursor.rowcount
    
    # Add a comment
    Cursor.close()
    Connection.close()
    
    # Add a comment
    return Response



# Add a comment
def Login(Email, Password):
    
    # Add a comment
    Cursor,Connection=Database.ConnectToDatabase()

    
    # Add a comment
    Query = "SELECT * FROM Users where Email=%s and Password=%s ORDER BY UserId DESC LIMIT 1"
    values=(Email,Password)
    
    # Add a comment
    Cursor.execute(Query,values)
    
    
    # Add a comment
    # sql = Cursor.mogrify(Query, values)
    # print(sql)

    # Add a comment
    if Cursor.rowcount >0:
        
        # Add a comment
        result=Cursor.fetchone()
        
        # Add a comment
        SessionId="SES"+str(uuid.uuid4()).replace("-","",-1)
        
       # Add a comment
        DateAdded=datetime.now().isoformat()
    
        # Add a comment
        Query = "delete from UserSessions where UserId=%s "
        Query += "; insert into UserSessions(UserId, SessionId, DateAdded) values(%s,%s,%s)"
        values=(result['UserId'], result['UserId'], SessionId, DateAdded)
        
        # Add a comment
        Cursor.execute(Query,values)
        Connection.commit()
        
        # Add a comment
        # sql = Cursor.mogrify(Query, values)
        # print(sql)

        
        # Add a comment
        Session={}
        Session['SessionId']=SessionId
        Session['DateAdded']=DateAdded
        
        
        # Add a comment
        Response={}
        Response['action']="select"
        Response['rowcount']=Cursor.rowcount
        Response['data']=Session
    else:
        
        # Add a comment
        Response={}
        Response['action']="select"
        Response['rowcount']=Cursor.rowcount
        Response['data']=[]
    
    
    # Add a comment
    Cursor.close()
    Connection.close()
    
    # Add a comment
    return Response



# Add a comment
def UpdatePassword(UserSessionId, Password):
    
    # Add a comment
    Cursor,Connection=Database.ConnectToDatabase()

    
    # Add a comment
    Query = "update Users set Password=%s where UserId in (select UserId from UserSessions where Sessionid=%s)"
    values=(Password, UserSessionId)
    
    # Add a comment
    Cursor.execute(Query,values)
    Connection.commit()
    
    # Add a comment
    # sql = Cursor.mogrify(Query, values)
    # print(sql)

    # Add a comment
    Response={}
    Response['action']="update"
    Response['rowcount']=Cursor.rowcount
    
    # Add a comment
    Cursor.close()
    Connection.close()
    
    # Add a comment
    return Response




# Add a comment
def VerifyLogin(SessionId):
    
    # Add a comment
    Cursor,Connection=Database.ConnectToDatabase()

    
    # Add a comment
    Query = "select * from UserSessions where SessionId =%s"
    values=(SessionId)
    
    # Add a comment
    Cursor.execute(Query,values)

    
    # Add a comment
    # sql = Cursor.mogrify(Query, values)
    # print(sql)

    # Add a comment
    Response={}
    Response['action']="select"
    Response['rowcount']=Cursor.rowcount
    Response['data']=Cursor.fetchone()
    
    # Add a comment
    Cursor.close()
    Connection.close()
    
    # Add a comment
    return Response


