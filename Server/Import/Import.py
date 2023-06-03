
from Lib import Database
from flask import Blueprint, request, jsonify
from flask_cors import CORS, cross_origin
from .ExtractShipManifest import Extract_ShipManifest
from .ImportShipManifest import save_ship_manifest
from .ExtractNotary import extract_Notary
from .ImportNotary import import_Notary

blueprint = Blueprint('Import', __name__)

@blueprint.route("/Import/ImportData", methods=['POST'])
@cross_origin()
def ImportData():
    sessionData={}
    import_data = request.get_json()
    
    sessionData['SessionId']=import_data['SessionId']
    sessionData['SpreadsheetName']=import_data['SpreadsheetName']
    spreadsheet_name = import_data['SpreadsheetName']
    spreadsheet_data = import_data['SpreadsheetData']
    
    rows = spreadsheet_data.split("\n")
    spreadsheet_array = []
    headers = rows[0].split("\t")  # Get column names from the first row
    print(headers)
    for row in rows[1:]:  # Skip the first row because it contains column names
        cells = row.split("\t")
        row_dict = dict(zip(headers, cells))  # Combine headers and cells into a dictionary
        spreadsheet_array.append(row_dict)
    if len(spreadsheet_array[0]) == 14:
        print("notary")

        Notary=extract_Notary(spreadsheet_name,spreadsheet_array)
        import_Notary(sessionData,Notary)
    elif len(spreadsheet_array[0]) == 24:
        voyage = spreadsheet_name.split(" ")
        VoyageId = voyage[0]
        VoyageDate = voyage[len(voyage)-1]
        ShipType = voyage[2:3]
        ShipType = " ".join(ShipType)


        # this removes the voyage number and date from the spreadsheet_name. 
        # There are spaces in the name. so the split messes things up.
        ShipName = voyage[3:-1]
        ShipName = " ".join(ShipName)

        
        ShipInfo,ShipManifest=Extract_ShipManifest(ShipName,ShipType, VoyageId, VoyageDate,spreadsheet_array)
        
        # save_ship_manifest(sessionData, ShipInfo,ShipManifest)
    else:
        print("NOT IMPORTED",len(spreadsheet_array[0]))

    print("IMPORT COMPLETED")
    result = {"message": "Data imported successfully"}
    return result
    
    
