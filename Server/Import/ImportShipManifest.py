import uuid
from Lib import Database
from datetime import datetime, timedelta

def save_ship_manifest(ShipName, ShipType,VoyageId, voyageDate, spreadsheet_array):
    # Connect to the database
    cursor, connection = Database.ConnectToDatabase()
    
    ShipSize=spreadsheet_array[0]["Ship's Size (in tons)"]
    ShipHomePortCity=spreadsheet_array[0]["Ship's Home Port"].split(",")[0].strip()
    ShipHomePortState=spreadsheet_array[0]["Ship's Home Port"].split(",")[0].strip()
    

    query = "select LocationId from Locations where City = %s and State=%s and Address is null"
    values=(ShipHomePortCity,ShipHomePortState,)
    cursor.execute(query, values)
    result = cursor.fetchone()

    if result is None:
        LocationId = "LOC" + str(uuid.uuid4())
        query = "INSERT INTO Locations (LocationId, City, State) VALUES (%s, %s, %s)"
        values = (LocationId, ShipHomePortCity, ShipHomePortState,)
        cursor.execute(query, values)
        connection.commit()
    else:
        LocationId = result['LocationId']

    query = "select ShipId from Ships where ShipName = %s and ShipType=%s"
    values=(ShipName,ShipType)
    cursor.execute(query, values,)
    result = cursor.fetchone()
    if result is None:

        ShipId = "SHP" + str(uuid.uuid4())
        query = "INSERT INTO Ships (ShipId, ShipName,ShipType,Size,HomePort) VALUES (%s, %s, %s, %s, %s)"
        values = (ShipId, ShipName, ShipType,ShipSize,LocationId,)


        cursor.execute(query, values)
        connection.commit()

    else:
        ShipId = result['ShipId']

    VoyageStartDate=None
    CaptainFirstName=None
    CaptainLastName=None
    for row in spreadsheet_array:
        StartYear=row["Year of Manifest Recorded in Norfolk (yyyy)"]
        MonthAndDay=row["Month and day of Manifest Recorded in Norfolk (mm-dd)"]
        
        if len(StartYear):
            if "-" in MonthAndDay:
                sd = MonthAndDay+ "-" + StartYear
                VoyageStartDate = datetime.strptime(sd, "%m-%d-%Y")
            else:
                sd = MonthAndDay+ " " + StartYear
                VoyageStartDate = datetime.strptime(sd, "%B %d %Y")
        print("VoyageStartDate",VoyageStartDate)
        CaptainName=row["Ship Captain's Name (Last, First Middle)"]
        if len(CaptainName):
            CaptainLastName=CaptainName.split(",")[0].strip()
            CaptainFirstName=CaptainName.split(",")[1].strip()
            
    query = "select Humans.HumanId from Humans "
    query += " where Humans.FirstName = %s and Humans.LastName=%s "
    values=(CaptainFirstName, CaptainLastName,)
    
    cursor.execute(query, values)
    result = cursor.fetchone()

    if result is None:
        CaptainHumanId = "HUM" + str(uuid.uuid4())
        query = "INSERT INTO Humans(HumanId,FirstName,LastName) VALUES (%s, %s, %s) "
       
        values = (CaptainHumanId, CaptainFirstName, CaptainLastName,)
        cursor.execute(query, values)
        connection.commit()
    else:
        CaptainHumanId = result['HumanId']


    BusinessId = "BUS" + str(uuid.uuid4())
    query = "INSERT INTO Businesses(BusinessId, BusinessName) VALUES (%s, %s) "

    values = (BusinessId, ShipName,)
    cursor.execute(query, values)
    connection.commit()

    query = "INSERT INTO BusinessHumans(BusinessId, HumanId, RoleId) VALUES (%s, %s, %s) "

    values = (BusinessId, CaptainHumanId,"ROL-CAP-2da-c1cc-4100-abbb-3da1508fc827")
    cursor.execute(query, values)
    connection.commit()


    for row in spreadsheet_array:
        
        EnslavedLastName=row["Last Name"]
        EnslavedFirstName=row["First and Middle Names"]
        EnslavedGender=row["Sex"]
        EnslavedAge=row["Age"]
        if "months" in EnslavedAge :
            EnslavedAge = int(EnslavedAge.split(" ")[0])/12
        EnslavedHeightInInches=float(row["Height (feet)"])*12+fraction_to_float(row["Height (inches)"])
        EnslavedColor=row["Color"]
        bd = "January 1 "+ str(int(StartYear)-int(EnslavedAge))
        EnslavedBirthDate = datetime.strptime(bd, "%B %d %Y")

        OwnerName=row["Owner's Name (Last, First Middle)"]
        if len(OwnerName) and "," in OwnerName:
            OwnerFirstName=OwnerName.split(",")[1].strip()
            OwnerLastName=OwnerName.split(",")[0].strip()

        OwnerLocation=row["Owner's Location (Locality, State)"]
        OwnerLocationId=None
        if len(OwnerLocation) and "," in OwnerLocation:
            OwnerCity=OwnerLocation.split(",")[0].strip()
            OwnerState=OwnerLocation.split(",")[1].strip()
        else:
            OwnerCity=OwnerLocation.split(" ")[0].strip()
            OwnerState=OwnerLocation.split(" ")[1].strip()

        query = "select LocationId from Locations where City = %s and State=%s and Address is null"
        values=(OwnerCity,OwnerState,)
        
        cursor.execute(query, values)
        result = cursor.fetchone()
        if result is None:
            OwnerLocationId = "LOC" + str(uuid.uuid4())
            query = "INSERT INTO Locations(LocationId, City, State) VALUES (%s, %s, %s) "
        
            values = (OwnerLocationId, OwnerCity, OwnerState,)
            cursor.execute(query, values)
            connection.commit()
        else:
            OwnerLocationId = result['LocationId']

        ShippingAgentName=row["Shipping Agent (Last Name, First and Middle)"]
        ShippingAgentFirstName=None
        ShippingAgentLastName=None
        if len(ShippingAgentName) and "," in ShippingAgentName :
            ShippingAgentFirstName=ShippingAgentName.split(",")[1].strip()
            ShippingAgentLastName=ShippingAgentName.split(",")[0].strip()

        OwnerAgentName=row["Owner/Agent 2 Location (Locality, State)"]
        OwnerAgentFirstName=None
        OwnerAgentLastName=None
        if len(OwnerAgentName) and "," in OwnerAgentName:
            OwnerAgentFirstName=OwnerAgentName.split(",")[1].strip()
            OwnerAgentLastName=OwnerAgentName.split(",")[0].strip()

        query = "select Humans.HumanId from Humans join HumanOwners on Humans.HumanId=HumanOwners.HumanId "
        query += " join Businesses on Businesses.BusinessId=HumanOwners.OwnerBusinessId "
        query += " join BusinessHumans on BusinessHumans.BusinessId=Businesses.BusinessId "
        query += " join Humans Owners on Owners.HumanId = BusinessHumans.HumanId "
        query += " where Humans.FirstName = %s and Humans.LastName=%s and Owners.FirstName = %s and Owners.LastName=%s"
        values=(EnslavedFirstName,EnslavedLastName,OwnerFirstName,OwnerLastName,)
        
        cursor.execute(query, values)
        result = cursor.fetchone()

        if result is None:
            HumanId = "HUM" + str(uuid.uuid4())
            query = "INSERT INTO Humans(HumanId,FirstName,LastName, BirthDate, Gender, HeightInInches, RaceId) VALUES (%s, %s, %s, %s, %s, %s, %s) "
            query += "ON DUPLICATE KEY UPDATE FirstName=values(FirstName),LastName=values(LastName),BirthDate=values(BirthDate),HeightInInches=values(HeightInInches),RaceId=values(RaceId)"
        
            values = (HumanId, EnslavedFirstName, EnslavedLastName, EnslavedBirthDate, EnslavedGender, float(EnslavedHeightInInches), EnslavedColor,)
            cursor.execute(query, values)
            connection.commit()
        else:
            HumanId = result['HumanId']

        query = "select Humans.HumanId from Humans "
        query += " join BusinessHumans on BusinessHumans.HumanId=Humans.HumanId "
        query += " join HumanOwners on HumanOwners.OwnerBusinessId=BusinessHumans.BusinessId "

        query += " where Humans.FirstName = %s and Humans.LastName=%s"
        values=(OwnerFirstName,OwnerLastName,)
        
        cursor.execute(query, values)
        result = cursor.fetchone()

        if result is None:
            OwnerHumanId = "HUM" + str(uuid.uuid4())
            query = "INSERT INTO Humans(HumanId,FirstName,LastName) VALUES (%s, %s, %s) "
            query += "ON DUPLICATE KEY UPDATE FirstName=values(FirstName),LastName=values(LastName),BirthDate=values(BirthDate),HeightInInches=values(HeightInInches),RaceId=values(RaceId)"
        
            values = (OwnerHumanId, OwnerFirstName, OwnerLastName,)
            cursor.execute(query, values)
            connection.commit()




            BusinessId = "BUS" + str(uuid.uuid4())
            query = "INSERT INTO Businesses(BusinessId, BusinessName, LocationId) VALUES (%s, %s, %s) "
        
            values = (BusinessId, OwnerFirstName+" "+OwnerLastName,OwnerLocationId,)
            cursor.execute(query, values)
            connection.commit()

            query = "INSERT INTO BusinessHumans(BusinessId, HumanId, RoleId) VALUES (%s, %s, %s) "
        
            values = (BusinessId, OwnerHumanId,"ROL-SLV-OWN-8f-82-49b-8aee-1b5b6e696ca9")
            cursor.execute(query, values)
            connection.commit()

            query = "INSERT INTO HumanOwners(HumanId, OwnerBusinessId, OwnDate) VALUES (%s, %s, %s) "
        
            values = (HumanId, BusinessId,VoyageStartDate)
            cursor.execute(query, values)
            connection.commit()
        else:
            OwnerHumanId = result['HumanId']

    connection.close()
    
    print("ShipId", ShipId)

    # Return the HumanId as a JSON response
    return {'success': True}


def fraction_to_float(fraction_string):
    parts = fraction_string.split()
    if len(parts) == 1:
        # The string represents a whole number or simple fraction
        if '/' in parts[0]:
            # The string represents a simple fraction
            numerator, denominator = parts[0].split('/')
            return float(numerator) / float(denominator)
        else:
            # The string represents a whole number
            return float(parts[0])
    elif len(parts) == 2:
        # The string represents a mixed fraction
        whole = float(parts[0])
        numerator, denominator = parts[1].split('/')
        fraction = float(numerator) / float(denominator)
        return whole + fraction
    else:
        raise ValueError("Invalid fraction format")