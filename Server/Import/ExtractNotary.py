import uuid
from Lib import Database
from datetime import datetime, timedelta
from dateutil import parser


def extract_Notary( spreadsheet_name, spreadsheet_array):
    # Connect to the database
    cursor, connection = Database.ConnectToDatabase()
    
    Notary = spreadsheet_name.split("-")[1]
    NotaryLastName= Notary.split(",")[0].strip()
    NotaryFirstName = Notary.split(",")[1]
    NotaryFirstName = NotaryFirstName.split("(")[0].strip()
    

    


    rows=[]
    for row in spreadsheet_array:
        rowData={}
        FromParty=row["First Party (From) - [Last Name, First and Middle Names]  Be sure to add connections to this person especially if they are acting as an agent for someone else."]
        
        rowData['FromParty']=FromParty
        FromParty=FromParty.split("and")
        rowData['FromHumans']=[]
        rowData['FromCity']=""
        rowData['FromState']=""
        rowData['ToCity']=""
        rowData['ToState']=""
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
                From['LastName']=""
                if len(party.split(" ")) > 1:
                    From['LastName']= party.split(" ")[1].strip()
            rowData['FromHumans'].append(From)

        

        FromLocation=row['Location of First Party [Locality, State]'].split(",")
        if len(FromLocation) > 0:
            rowData['FromCity']=FromLocation[0].strip()
        if len(FromLocation) > 1:
            rowData['FromState']=FromLocation[1].strip()





        ToParty=row["Second Party (To) - [Last Name, First and Middle Names]"]
        rowData['ToParty']=ToParty
        ToParty=ToParty.split("and")
        
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
                To['LastName']=""
                if len(party.split(" ")) > 1:
                    To['LastName']= party.split(" ")[1].strip()
            rowData['ToHumans'].append(To)


        
        

        ToLocation=row['Location of Second Party [Locality, State]'].split(",")
        if len(ToLocation) > 0:
            rowData['ToCity']=ToLocation[0].strip()
        if len(ToLocation) > 1:
            rowData['ToState']=ToLocation[1].strip()

        
        rowData['TransactionType']=row['Type of Transaction']
        rowData['TransactionDate']=row['Date (yyyy-mm-dd) - [ex. 1825-05-05]']
        
        
        try:
            rowData['TransactionDate'] = parser.parse(rowData['TransactionDate'])
        except Exception as e:
            rowData['TransactionDate']=None


        rowData['Act']=row['Act']
        rowData['Page']=row['Page/Folio']
        rowData['Volume']=row['Volume # ']
        rowData['NotaryFirstName']=NotaryFirstName
        rowData['NotaryLastName']=NotaryLastName
        
        rowData['Notes']=row['Notes (Be sure to add total sale\'s price, name of slave,  ethnicity, gender, age, and sale\'s price.)   [Ex.  Total sales price - $ 1,200.  Tom, negro boy aged 12 years old  who was sold for $ 600. Jane, mulatto woman aged 23 years old who was sold for $ 600.] ']
        
        if 'Paste the Web address (URL)' in row:
            rowData['URL']=row['Paste the Web address (URL)']
        else:
            rowData['URL']=""

        try:
            Transcriber=row['Name of Transcriber, School Initials, Semester Year (ex. John Smith, NSU, Spring 2022)']
        except KeyError:
            print("Key 'Name of Transcriber' not found in row.")
            Transcriber=""
        except Exception as e:
            Transcriber=""
            print("An error occurred:", str(e))
        rowData['TranscriberFirstName']=Transcriber.split(" ")[0]
        rowData['TranscriberLastName']=Transcriber.split(" ")[1:]
        rowData['TranscriberLastName']=' '.join(rowData['TranscriberLastName'])
        rows.append(rowData)
        

    return rows