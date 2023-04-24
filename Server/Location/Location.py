from Lib import Database
from Lib import History
from flask import Blueprint, request
from flask_cors import CORS, cross_origin
from .SaveLocation import save_location
from .DeleteLocation import delete_location
from .GetLocation import get_location

blueprint = Blueprint('Location', __name__)

@blueprint.route("/Location/SaveLocation", methods=['GET'])
@cross_origin()
def SaveLocation():
    location_data = request.args.to_dict()

    # Extract the location information from the location_data
    LocationId = location_data.get('LocationId', None)
    City = location_data.get('City', None)
    State = location_data.get('State', None)
    Country = location_data.get('Country', None)
    Latitude = location_data.get('Latitude', None)
    Longitude = location_data.get('Longitude', None)

    # Call the save_location function from SaveLocation.py with the extracted data
    result = save_location(LocationId, City, State, Country, Latitude, Longitude)
    History.SaveHistory(location_data,"Locations", "LocationId", result["LocationId"])

    return result
    
    

@blueprint.route("/Location/DeleteLocation", methods=['GET'])
@cross_origin()
def DeleteLocation():
    # Get the location information from the request
    location_data = request.args.to_dict()

    # Get the location ID from the request
    LocationId = location_data.get('LocationId')
    # Call the delete_location function from DeleteLocation.py
    result = delete_location(LocationId)
    History.SaveHistory(location_data,"Locations", "LocationId", LocationId)
    return result

@blueprint.route("/Location/GetLocation", methods=['GET'])
@cross_origin()
def GetLocation():
    # Get the location information from the request
    location_data = request.args.to_dict()

    # Get the location ID from the request
    LocationId = location_data.get('LocationId')
    # Call the get_location function from GetLocation.py
    result = get_location(LocationId)
    return result
