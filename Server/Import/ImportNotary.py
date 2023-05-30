import uuid
from Lib import Database
from datetime import datetime, timedelta
from dateutil import parser


def import_Notary( Notary):
    cursor, connection = Database.ConnectToDatabase()
    

    NotaryHumanId = "HUM" + str(uuid.uuid4())
    query = "INSERT INTO Humans(HumanId,FirstName,LastName) VALUES (%s, %s, %s) "
    query += "ON DUPLICATE KEY UPDATE FirstName=values(FirstName),LastName=values(LastName)"

    values = (NotaryHumanId, Notary[0]['NotaryFirstName'], Notary[0]['NotaryLastName'],)
    cursor.execute(query, values)
    connection.commit()

    NotaryBusinessId = "BUS" + str(uuid.uuid4())
    query = "INSERT INTO Businesses(BusinessId, BusinessName) VALUES (%s, %s) "

    values = (NotaryBusinessId, Notary[0]['NotaryFirstName']+" "+Notary[0]['NotaryLastName'],)
    cursor.execute(query, values)
    connection.commit()

    query = "INSERT INTO BusinessHumans(BusinessId, HumanId, RoleId) VALUES (%s, %s, %s) "

    values = (NotaryBusinessId, NotaryHumanId,"ROL-NOT-d66-db51-46a9-b699-169789a3d9df")
    cursor.execute(query, values)
    connection.commit()

    # ['FromHumans', 'FromCity', 'FromState', 'ToHumans', 'ToCity', 'ToState', 'TransactionType', 'TransactionDate', 'Act', 'Page', 'NotaryFirstName', 'NotaryLastName', 'Notes', 'url', 'Transcriber']
    #  'FromCity', 'FromState',  'ToCity', 'ToState', 'TransactionType', 'TransactionDate', 'Act', 'Page', 'Notes', 'url', 'TranscriberFirstName 'TranscriberLastName']
    # 

    for row in Notary:
        
        FromBusinessId = "BUS" + str(uuid.uuid4())
        query = "INSERT INTO Businesses(BusinessId, BusinessName) VALUES (%s, %s) "

        values = (FromBusinessId, row['FromParty'],)
        cursor.execute(query, values)
        connection.commit()

        for FromHuman in row['FromHumans']:
            
            FromHumanId = "HUM" + str(uuid.uuid4())
            query = "INSERT INTO Humans(HumanId,FirstName,LastName) VALUES (%s, %s, %s) "
            query += "ON DUPLICATE KEY UPDATE FirstName=values(FirstName),LastName=values(LastName)"

            values = (FromHumanId, FromHuman['FirstName'], FromHuman['LastName'],)
            cursor.execute(query, values)
            connection.commit()

            query = "INSERT INTO BusinessHumans(BusinessId, HumanId, RoleId) VALUES (%s, %s, %s) "

            values = (FromBusinessId, FromHumanId,"ROL-SLV-OWN-8f-82-49b-8aee-1b5b6e696ca9")
            cursor.execute(query, values)
            connection.commit()
        

        ToBusinessId = "BUS" + str(uuid.uuid4())
        query = "INSERT INTO Businesses(BusinessId, BusinessName) VALUES (%s, %s) "

        values = (ToBusinessId, row['ToParty'],)
        cursor.execute(query, values)
        connection.commit()

        for ToHuman in row['ToHumans']:
            # names = list(ToHuman.keys())
            # print(names)
            ToHumanId = "HUM" + str(uuid.uuid4())
            query = "INSERT INTO Humans(HumanId,FirstName,LastName) VALUES (%s, %s, %s) "
            query += "ON DUPLICATE KEY UPDATE FirstName=values(FirstName),LastName=values(LastName)"

            values = (ToHumanId, ToHuman['FirstName'], ToHuman['LastName'],)
            cursor.execute(query, values)
            connection.commit()

            query = "INSERT INTO BusinessHumans(BusinessId, HumanId, RoleId) VALUES (%s, %s, %s) "

            values = (ToBusinessId, ToHumanId,"ROL-SLV-OWN-8f-82-49b-8aee-1b5b6e696ca9")
            cursor.execute(query, values)
            connection.commit()

        query = "Select UserId from Users where FirstName=%s and LastName=%s"
        values = ( row['TranscriberFirstName'], row['TranscriberLastName'], )
        cursor.execute(query, values)
        result = cursor.fetchone()
        if result is None:

            TranscriberUserId = "USR" + str(uuid.uuid4())
            query = "INSERT INTO Users(UserId,FirstName,LastName, UserType) VALUES (%s, %s, %s, %s) "
            query += "ON DUPLICATE KEY UPDATE FirstName=values(FirstName),LastName=values(LastName)"

            values = (TranscriberUserId, row['TranscriberFirstName'], row['TranscriberLastName'],"Transcriber", )
            cursor.execute(query, values)
            connection.commit()
        else:
            TranscriberUserId=result['UserId']

        TransactionId = "TRN" + str(uuid.uuid4())
        query = "INSERT INTO Transactions(TransactionId, TransactionDate, FromBusinessId, FromCity, FromState, ToBusinessId, ToCity, ToState, TransactionType, Notes, Act, Page,Volume, URL, NotaryBusinessId, TranscriberUserId, NeedsReview ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) "
        
        values = (TransactionId, row['TransactionDate'],FromBusinessId, row['FromCity'],row['FromState'],ToBusinessId,row['ToCity'],row['ToState'],row['TransactionType'],row['Notes'],row['Act'],row['Page'],row['Volume'],row['URL'],NotaryBusinessId,TranscriberUserId, 1)
        # print(query%values)
        cursor.execute(query, values)
        connection.commit()

    return True


