import uuid
from Lib import Database
from datetime import datetime, timedelta
from dateutil import parser
from dateutil.relativedelta import relativedelta


def Extract_ShipManifest(ShipName,ShipType, VoyageId, VoyageDate,spreadsheet_array):
    # Connect to the database
    cursor, connection = Database.ConnectToDatabase()
    ShipSize=spreadsheet_array[0]["Ship's Size (in tons)"]
    ShipHomePortCity=spreadsheet_array[0]["Ship's Home Port"].split(",")[0].strip()
    ShipHomePortState=spreadsheet_array[0]["Ship's Home Port"].split(",")[0].strip()

    ShipManifest=[]
    
    VoyageStartDate=None
    CaptainFirstName=None
    CaptainLastName=None
    ShipInfo={}
    for row in spreadsheet_array:
        
        ShipInfo['VoyageId']=row["Ship Voyage ID #:"]
        ShipInfo['ShipName']=row["Ship's Name"]
        ShipInfo['ShipSize']=row["Ship's Size (in tons)"]
        ShipInfo['ShipType']=row["Ship's Type"]
        ShipInfo['ShipHomePort']=row["Ship's Home Port"]
        ShipInfo['ShipHomePortCity']=row["Ship's Home Port"].split(",")[0].strip()
        ShipInfo['ShipHomePortState']=row["Ship's Home Port"].split(",")[1].strip()
        CaptainName=row["Ship Captain's Name (Last, First Middle)"]
        if len(CaptainName):
            ShipInfo['CaptainLastName']=CaptainName.split(",")[0].strip()
            ShipInfo['CaptainFirstName']=CaptainName.split(",")[1].strip()
        



        StartYear=row["Year of Manifest Recorded in Norfolk (yyyy)"]
        StartMonthAndDay=row["Month and day of Manifest Recorded in Norfolk (mm-dd)"]

        if len(StartYear):
            if "-" in StartMonthAndDay:
                sd = StartMonthAndDay+ "-" + StartYear
                # VoyageStartDate = datetime.strptime(sd, "%m-%d-%Y")
            else:
                sd = StartMonthAndDay+ " " + StartYear
                # VoyageStartDate = datetime.strptime(sd, "%B %d %Y")

            try:
                ShipInfo['VoyageStartDate'] = parser.parse(sd)
            except Exception as e:
                print("EXCEPTION!",e)
                ShipInfo['VoyageStartDate']=None

        EndYear=row["Year of Manifest Recorded in New Orleans (yyyy)"]
        EndMonthAndDay=row["Month and day of Manifest Recorded in New Orleans (mm-dd)"]

        if len(EndYear):
            if "-" in EndMonthAndDay:
                sd = EndMonthAndDay+ "-" + EndYear
            else:
                sd = EndMonthAndDay+ " " + EndYear

            try:
                ShipInfo['VoyageEndDate'] = parser.parse(sd)
            except Exception as e:
                print("EXCEPTION!",e)
                ShipInfo['VoyageEndDate']=None


    for row in spreadsheet_array:
        ManifestData={}
        ManifestData['EnslavedLastName']=row["Last Name"]
        ManifestData['EnslavedFirstName']=row["First and Middle Names"]
        ManifestData['EnslavedGender']=row["Sex"]
        ManifestData['EnslavedHeightInInches']=float(row["Height (feet)"])*12+fraction_to_float(row["Height (inches)"])
        ManifestData['EnslavedColor']=row["Color"]
        EnslavedAge=row["Age"]
        if "months" in EnslavedAge :
            EnslavedAge = int(EnslavedAge.split(" ")[0])
            ManifestData['EnslavedBirthDateAccuracy']="Month"
        elif EnslavedAge == 0:
            EnslavedAge=1
            ManifestData['EnslavedBirthDateAccuracy']="Month"
        elif len(EnslavedAge):
            ManifestData['EnslavedBirthDateAccuracy']="Year"
        else:
            ManifestData['EnslavedBirthDateAccuracy']=None

        ManifestData['EnslavedBirthDate']=None

        if ManifestData['EnslavedBirthDateAccuracy']=="Year":
            EnslavedAge = int(EnslavedAge)
            ManifestData['EnslavedBirthDate'] = ShipInfo['VoyageStartDate'] - relativedelta(years=EnslavedAge)
        elif ManifestData['EnslavedBirthDateAccuracy']=="Month":
            EnslavedAge = int(EnslavedAge)
            ManifestData['EnslavedBirthDate'] = ShipInfo['VoyageStartDate'] - relativedelta(months=EnslavedAge)

        # print("------------------------")
        # print("original",row["Age"])
        # print("ManifestData['VoyageStartDate']",ManifestData['VoyageStartDate'])
        # print("EnslavedAge",EnslavedAge)
        # print("ManifestData['EnslavedBirthDate']",ManifestData['EnslavedBirthDate'])
        # print("ManifestData['EnslavedBirthDateAccuracy']",ManifestData['EnslavedBirthDateAccuracy'])
        
        OwnerName=row["Owner's Name (Last, First Middle)"]
        ManifestData['OwnerStartFirstName']=""
        ManifestData['OwnerStartLastName']=""
        if len(OwnerName) and "," in OwnerName:
            ManifestData['OwnerStartFirstName']=OwnerName.split(",")[1].strip()
            ManifestData['OwnerStartLastName']=OwnerName.split(",")[0].strip()

        OwnerLocation=row["Owner's Location (Locality, State)"]
        ManifestData['OwnerStartCity']=""
        ManifestData['OwnerStartState']=""
        if len(OwnerLocation) and "," in OwnerLocation:
            ManifestData['OwnerStartCity']=OwnerLocation.split(",")[0].strip()
            ManifestData['OwnerStartState']=OwnerLocation.split(",")[1].strip()
        elif len(OwnerLocation) and " " in OwnerLocation:
            ManifestData['OwnerStartCity']=OwnerLocation.split(" ")[0].strip()
            ManifestData['OwnerStartState']=OwnerLocation.split(" ")[1].strip()

        ShippingAgentName=row["Shipping Agent (Last Name, First and Middle)"]
        ManifestData['ShippingAgentFirstName']=None
        ManifestData['ShippingAgentLastName']=None
        if len(ShippingAgentName) and "," in ShippingAgentName :
            ManifestData['ShippingAgentFirstName']=ShippingAgentName.split(",")[1].strip()
            ManifestData['ShippingAgentLastName']=ShippingAgentName.split(",")[0].strip()

        OwnerEndName=row["Owner/Agent 2 Location (Locality, State)"]
        ManifestData['OwnerEndFirstName']=""
        ManifestData['OwnerEndLastName']=""
        ManifestData['OwnerEndCity']=""
        ManifestData['OwnerEndState']=""
        if len(OwnerEndName) and "," in OwnerEndName:
            ManifestData['OwnerEndFirstName']=OwnerEndName.split(",")[1].strip()
            ManifestData['OwnerEndLastName']=OwnerEndName.split(",")[0].strip()
        ManifestData['Notes']=row["Notes: (I think it is…)"]

        ManifestData['Transcriber']=row["Transcribers:"]
        ShipManifest.append(ManifestData)
        
    return ShipInfo, ShipManifest





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