from flask import Blueprint, request
from flask_cors import CORS, cross_origin
from .SaveVoyage import save_Voyage
from .DeleteVoyage import delete_Voyage
from .GetVoyage import get_Voyage
from Lib import Database
from Lib import History
from .GetShips import get_Ships
from .GetHumans import get_Humans
from .SaveVoyageHuman import save_VoyageHuman
from .GetVoyageHumans import get_VoyageHumans
from .DeleteVoyageHuman import delete_VoyageHuman
from .GetRoles import get_roles
from .GetLocations import get_locations

blueprint = Blueprint('Voyage', __name__)

@blueprint.route("/Voyage/SaveVoyage", methods=['GET'])
@cross_origin()
def SaveVoyage():
    Voyage_data = request.args.to_dict()

    # Extract the VoyageId, ShipId, StartLocationId, EndLocationId, StartDate, EndDate, and Notes from the Voyage_data
    VoyageId = Voyage_data.get('VoyageId', None)
    ShipId = Voyage_data.get('ShipId', None)
    StartLocationId = Voyage_data.get('StartLocationId', None)
    EndLocationId = Voyage_data.get('EndLocationId', None)
    StartDate = Voyage_data.get('StartDate', None)
    EndDate = Voyage_data.get('EndDate', None)
    Notes = Voyage_data.get('Notes', None)

    # Call the save_Voyage function from SaveVoyage.py with the extracted data
    result = save_Voyage(VoyageId, ShipId, StartLocationId, EndLocationId, StartDate, EndDate, Notes)
    History.SaveHistory(Voyage_data, "Voyages", "VoyageId", result["VoyageId"])

    return result

@blueprint.route("/Voyage/DeleteVoyage", methods=['GET'])
@cross_origin()
def DeleteVoyage():
    Voyage_data = request.args.to_dict()

    # Get the VoyageId from the request data
    VoyageId = Voyage_data.get('VoyageId')

    # Call the delete_Voyage function from DeleteVoyage.py
    result = delete_Voyage(VoyageId)
    History.SaveHistory(Voyage_data, "Voyages", "VoyageId", VoyageId)

    return result

@blueprint.route("/Voyage/GetVoyage", methods=['GET'])
@cross_origin()
def GetVoyage():
    Voyage_data = request.args.to_dict()

    # Get the VoyageId from the request data
    VoyageId = Voyage_data.get('VoyageId')

    # Call the get_Voyage function from GetVoyage.py
    result = get_Voyage(VoyageId)

    return result

@blueprint.route("/Voyage/GetShips", methods=['GET'])
@cross_origin()
def GetShips():
    # Get the user data from the request
    Voyage_data = request.args.to_dict()

    # Call the get_Ships function from GetShips.py
    result = get_Ships()
    return result

@blueprint.route("/Voyage/GetHumans", methods=['GET'])
@cross_origin()
def GetHumans():
    # Get the user data from the request
    Voyage_data = request.args.to_dict()
    VoyageId = Voyage_data.get('VoyageId')

    # Call the get_Ships function from GetShips.py
    result = get_Humans(VoyageId)
    return result

    
@blueprint.route("/Voyage/SaveVoyageHuman", methods=['GET'])
@cross_origin()
def SaveVoyageHuman():
    Voyage_data = request.args.to_dict()

    # Extract the VoyageId, ShipId, StartLocationId, EndLocationId, StartDate, EndDate, and Notes from the Voyage_data
    VoyageId = Voyage_data.get('VoyageId', None)
    HumanId = Voyage_data.get('HumanId', None)
    HumanRoleId = Voyage_data.get('VoyageHumanRoleId', None)
    HumanNotes = Voyage_data.get('VoyageHumanNotes', None)

    # Call the save_Voyage function from SaveVoyage.py with the extracted data
    result = save_VoyageHuman(VoyageId, HumanId, HumanRoleId, HumanNotes)
    History.SaveHistory(Voyage_data, "VoyageHumans", "VoyageId:HumanId", VoyageId+": "+HumanId)

    return result


    
@blueprint.route("/Voyage/GetVoyageHumans", methods=['GET'])
@cross_origin()
def GetVoyageHumans():
    # Get the user data from the request
    Voyage_data = request.args.to_dict()
    VoyageId = Voyage_data.get('VoyageId')

    # Call the get_Ships function from GetShips.py
    result = get_VoyageHumans(VoyageId)
    return result


    
@blueprint.route("/Voyage/DeleteVoyageHuman", methods=['GET'])
@cross_origin()
def DeleteVoyageHumans():
    # Get the user data from the request
    Voyage_data = request.args.to_dict()
    VoyageId = Voyage_data.get('VoyageId')
    HumanId = Voyage_data.get('HumanId')

    # Call the get_Ships function from GetShips.py
    result = delete_VoyageHuman(VoyageId, HumanId)
    History.SaveHistory(Voyage_data, "VoyageHumans", "VoyageId:HumanId", VoyageId+": "+HumanId)
    return result


@blueprint.route("/Voyage/GetRoles", methods=['GET'])
@cross_origin()
def GetRoles():
    # Get the user data from the request
    Voyage_data = request.args.to_dict()
    VoyageId = Voyage_data.get('VoyageId')

    # Call the get_Ships function from GetShips.py
    result = get_roles(VoyageId)
    return result

@blueprint.route("/Voyage/GetLocations", methods=['GET'])
@cross_origin()
def GetLocations():
    # Call the get_locations function to retrieve location data
    result = get_locations()
    return result
