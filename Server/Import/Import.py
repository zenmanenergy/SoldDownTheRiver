
from Lib import Database
from flask import Blueprint, request, jsonify
from flask_cors import CORS, cross_origin
from .ImportShipManifest import save_ship_manifest
from .ImportNotary import save_Notary

blueprint = Blueprint('Import', __name__)

@blueprint.route("/Import/ImportData", methods=['POST'])
@cross_origin()
def ImportData():
    import_data = request.get_json()
    
    spreadsheet_name = import_data['SpreadsheetName']
    spreadsheet_data = import_data['SpreadsheetData']
    
    rows = spreadsheet_data.split("\n")
    spreadsheet_array = []
    headers = rows[0].split("\t")  # Get column names from the first row

    for row in rows[1:]:  # Skip the first row because it contains column names
        cells = row.split("\t")
        row_dict = dict(zip(headers, cells))  # Combine headers and cells into a dictionary
        spreadsheet_array.append(row_dict)
    print(len(spreadsheet_array[0]))
    if len(spreadsheet_array[0]) == 14:
        print("notary")

        save_Notary(spreadsheet_name,spreadsheet_array)

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

        
        
        save_ship_manifest( ShipName,ShipType, VoyageId, VoyageDate, spreadsheet_array)

    result = {"message": "Data imported successfully"}
    return result
    
    
