import uuid
from Lib import Database
from Lib import History
from datetime import datetime, timedelta
from dateutil import parser


def import_Notary(data, Notary):
    cursor, connection = Database.ConnectToDatabase()
    

    NotaryHumanId = "HUM" + str(uuid.uuid4())
    query = "INSERT INTO Humans(HumanId,FirstName,LastName) VALUES (%s, %s, %s) "
    query += "ON DUPLICATE KEY UPDATE FirstName=values(FirstName),LastName=values(LastName)"

    values = (NotaryHumanId, Notary[0]['NotaryFirstName'], Notary[0]['NotaryLastName'],)
    cursor.execute(query, values)
    connection.commit()
    History.SaveHistory(data,"Humans", "HumanId", NotaryHumanId)

    NotaryBusinessId = "BUS" + str(uuid.uuid4())
    query = "INSERT INTO Businesses(BusinessId, BusinessName) VALUES (%s, %s) "

    values = (NotaryBusinessId, Notary[0]['NotaryFirstName']+" "+Notary[0]['NotaryLastName'],)
    cursor.execute(query, values)
    connection.commit()
    History.SaveHistory(data,"Businesses", "BusinessId", NotaryBusinessId)

    query = "INSERT INTO BusinessHumans(BusinessId, HumanId, RoleId) VALUES (%s, %s, %s) "

    values = (NotaryBusinessId, NotaryHumanId,"ROL-NOT-d66-db51-46a9-b699-169789a3d9df")
    cursor.execute(query, values)
    connection.commit()
    
    History.SaveHistory(data,"BusinessHumans", "BusinessId:HumanId", NotaryBusinessId+":"+NotaryHumanId)

    # ['FromHumans', 'FromCity', 'FromState', 'ToHumans', 'ToCity', 'ToState', 'TransactionType', 'TransactionDate', 'Act', 'Page', 'NotaryFirstName', 'NotaryLastName', 'Notes', 'url', 'Transcriber']
    #  'FromCity', 'FromState',  'ToCity', 'ToState', 'TransactionType', 'TransactionDate', 'Act', 'Page', 'Notes', 'url', 'TranscriberFirstName 'TranscriberLastName']
    # 

    for row in Notary:
        
        FromBusinessId = "BUS" + str(uuid.uuid4())
        query = "INSERT INTO Businesses(BusinessId, BusinessName) VALUES (%s, %s) "

        values = (FromBusinessId, row['FromParty'],)
        cursor.execute(query, values)
        connection.commit()
        History.SaveHistory(data,"Businesses", "BusinessId", FromBusinessId)


        for FromHuman in row['FromHumans']:
            
            FromHumanId = "HUM" + str(uuid.uuid4())
            query = "INSERT INTO Humans(HumanId,FirstName,LastName) VALUES (%s, %s, %s) "
            query += "ON DUPLICATE KEY UPDATE FirstName=values(FirstName),LastName=values(LastName)"

            values = (FromHumanId, FromHuman['FirstName'], FromHuman['LastName'],)
            cursor.execute(query, values)
            connection.commit()
            History.SaveHistory(data,"Humans", "HumanId", FromHumanId)

            query = "INSERT INTO BusinessHumans(BusinessId, HumanId, RoleId) VALUES (%s, %s, %s) "

            values = (FromBusinessId, FromHumanId,"ROL-SLV-OWN-8f-82-49b-8aee-1b5b6e696ca9")
            cursor.execute(query, values)
            connection.commit()
            History.SaveHistory(data,"BusinessHumans", "BusinessId:HumanId", FromBusinessId+":"+FromHumanId)
        

        ToBusinessId = "BUS" + str(uuid.uuid4())
        query = "INSERT INTO Businesses(BusinessId, BusinessName) VALUES (%s, %s) "

        values = (ToBusinessId, row['ToParty'],)
        cursor.execute(query, values)
        connection.commit()
        History.SaveHistory(data,"Businesses", "BusinessId", ToBusinessId)
        

        for ToHuman in row['ToHumans']:
            # names = list(ToHuman.keys())
            # print(names)
            ToHumanId = "HUM" + str(uuid.uuid4())
            query = "INSERT INTO Humans(HumanId,FirstName,LastName) VALUES (%s, %s, %s) "
            query += "ON DUPLICATE KEY UPDATE FirstName=values(FirstName),LastName=values(LastName)"

            values = (ToHumanId, ToHuman['FirstName'], ToHuman['LastName'],)
            cursor.execute(query, values)
            connection.commit()
            History.SaveHistory(data,"Humans", "HumanId", ToHumanId)

            query = "INSERT INTO BusinessHumans(BusinessId, HumanId, RoleId) VALUES (%s, %s, %s) "

            values = (ToBusinessId, ToHumanId,"ROL-SLV-OWN-8f-82-49b-8aee-1b5b6e696ca9")
            cursor.execute(query, values)
            connection.commit()
            History.SaveHistory(data,"BusinessHumans", "BusinessId:HumanId", ToBusinessId+":"+ToHumanId)

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
            History.SaveHistory(data,"Users", "UserId", TranscriberUserId)
        else:
            TranscriberUserId=result['UserId']

        query = "select LocationId from Locations where City = %s and State=%s and Address is null"
        values=(row['FromCity'],row['FromState'],)
        cursor.execute(query, values)
        result = cursor.fetchone()

        if result is None:
            FromLocationId = "LOC" + str(uuid.uuid4())
            query = "INSERT INTO Locations (LocationId, City, State) VALUES (%s, %s, %s)"
            values = (FromLocationId, row['FromCity'],row['FromState'],)
            cursor.execute(query, values)
            
        else:
            FromLocationId = result['LocationId']

        query = "select LocationId from Locations where City = %s and State=%s and Address is null"
        values=(row['ToCity'],row['ToState'],)
        cursor.execute(query, values)
        result = cursor.fetchone()

        if result is None:
            ToLocationId = "LOC" + str(uuid.uuid4())
            query = "INSERT INTO Locations (LocationId, City, State) VALUES (%s, %s, %s)"
            values = (ToLocationId, row['ToCity'],row['ToState'],)
            cursor.execute(query, values)
            
        else:
            ToLocationId = result['LocationId']

        TransactionId = "TRN" + str(uuid.uuid4())
        query = "INSERT INTO Transactions(TransactionId, TransactionDate, FromBusinessId, FromLocationId, ToLocationId, ToBusinessId, TransactionType, Notes, Act, Page,Volume, URL, NotaryBusinessId, TranscriberUserId, NeedsReview,TotalPrice ) VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) "
        
        values = (TransactionId, row['TransactionDate'],FromBusinessId, FromLocationId,ToLocationId,ToBusinessId,row['TransactionType'],row['Notes'],row['Act'],row['Page'],row['Volume'],row['URL'],NotaryBusinessId,TranscriberUserId, 1,row['TotalPrice'])
        # print(query%values)
        cursor.execute(query, values)
        connection.commit()
        History.SaveHistory(data,"Transactions", "TransactionId", TransactionId)



        for Human in row['TransactionHumans']:
            
            
            TransactionHumanId = "HUM" + str(uuid.uuid4())
            query = "INSERT INTO Humans(HumanId,FirstName,LastName,Notes, BirthDate,BirthDateAccuracy,RaceId,Gender) VALUES (%s, %s, %s,%s, %s, %s,%s, %s) "
            

            values = (TransactionHumanId, Human['EnslavedHumanFirstName'], Human['EnslavedHumanLastName'],Human['Notes'],Human['EnslavedHumanBirthDate'],Human['EnslavedHumanBirthDateAccuracy'],Human['EnslavedHumanColor'],Human['EnslavedHumanGender'])
            cursor.execute(query, values)
            connection.commit()
            History.SaveHistory(data,"Humans", "HumanId", ToHumanId)

            ToHumanId = "HUM" + str(uuid.uuid4())
            query = "INSERT INTO TransactionHumans(TransactionId,HumanId,Notes) VALUES (%s, %s, %s) "
            

            values = (TransactionId,TransactionHumanId, Human['Notes'])
            cursor.execute(query, values)
            connection.commit()
            History.SaveHistory(data,"TransactionHumans", "TransactionId:HumanId", TransactionId+":"+TransactionHumanId)
    return True


