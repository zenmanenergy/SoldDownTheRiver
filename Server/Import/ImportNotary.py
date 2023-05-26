import uuid
from Lib import Database
from datetime import datetime, timedelta
from dateutil import parser


def save_Notary( spreadsheet_name, spreadsheet_array):
    # Connect to the database
    cursor, connection = Database.ConnectToDatabase()
    
    Notary = spreadsheet_name.split("-")[1]
    NotaryLastName= Notary.split(",")[0].strip()
    NotaryFirstName = Notary.split(",")[1]
    NotaryFirstName = NotaryFirstName.split("(")[0].strip()
    

    NotaryHumanId = "HUM" + str(uuid.uuid4())
    query = "INSERT INTO Humans(HumanId,FirstName,LastName) VALUES (%s, %s, %s) "
    query += "ON DUPLICATE KEY UPDATE FirstName=values(FirstName),LastName=values(LastName)"

    values = (NotaryHumanId, NotaryFirstName, NotaryLastName,)
    cursor.execute(query, values)
    connection.commit()

    BusinessId = "BUS" + str(uuid.uuid4())
    query = "INSERT INTO Businesses(BusinessId, BusinessName) VALUES (%s, %s) "

    values = (BusinessId, NotaryFirstName+" "+NotaryLastName,)
    cursor.execute(query, values)
    connection.commit()

    query = "INSERT INTO BusinessHumans(BusinessId, HumanId, RoleId) VALUES (%s, %s, %s) "

    values = (BusinessId, NotaryHumanId,"ROL-NOT-d66-db51-46a9-b699-169789a3d9df")
    cursor.execute(query, values)
    connection.commit()


    rows=[]
    for row in spreadsheet_array:
        rowData={}
        FromParty=row["First Party (From) - [Last Name, First and Middle Names]  Be sure to add connections to this person especially if they are acting as an agent for someone else."].split("and")
        rowData['FromHumans']=[]
        for party in FromParty:
            party=party.replace("Mr.", "").strip()
            From={}
            if ',' in party:
                From['FirstName']= party.split(",")[1].strip()
                From['LastName']=""
                if len(party.split(",")[0].strip()) > 1:
                    From['LastName']= party.split(",")[0].strip()

            else:
                
                From['FirstName']= party.split(" ")[0].strip()
                if len(party.split(" ")) > 1:
                    From['LastName']= party.split(" ")[1].strip()
            rowData['FromHumans'].append(From)

        rowData['FromCity']=""
        rowData['FromState']=""

        FromLocation=row['Location of First Party [Locality, State]'].split(",")
        if len(FromLocation) > 0:
            rowData['FromCity']=FromLocation[0].strip()
        if len(FromLocation) > 1:
            rowData['FromState']=FromLocation[1].strip()





        ToParty=row["Second Party (To) - [Last Name, First and Middle Names]"].split("and")
        rowData['ToHumans']=[]
       
        for party in ToParty:
            party=party.replace("Mr.", "").strip()
            To={}
            if ',' in party:
                To['FirstName']= party.split(",")[1].strip()
                To['LastName']=""
                if len(party.split(",")[0].strip()) > 1:
                    To['LastName']= party.split(",")[0].strip()

            else:
                
                To['FirstName']= party.split(" ")[0].strip()
                if len(party.split(" ")) > 1:
                    To['LastName']= party.split(" ")[1].strip()
            rowData['ToHumans'].append(To)


        
        rowData['ToCity']=""
        rowData['ToState']=""

        ToLocation=row['Location of Second Party [Locality, State]'].split(",")
        if len(ToLocation) > 0:
            rowData['ToCity']=ToLocation[0].strip()
        if len(ToLocation) > 1:
            rowData['ToState']=ToLocation[1].strip()

        
        rowData['TransactionType']=row['Type of Transaction']
        rowData['TransactionDate']=row['Date (yyyy-mm-dd) - [ex. 1825-05-05]']
        rowData['TransactionDate']=parser.parse(rowData['TransactionDate'])
        rows.append(rowData)
        print(rowData['TransactionDate'])
    # print(rows)

    return {'success': True}