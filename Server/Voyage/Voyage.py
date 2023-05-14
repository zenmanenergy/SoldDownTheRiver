from flask import Blueprint, request
from flask_cors import CORS, cross_origin
from .SaveVoyage import save_voyage
from .DeleteVoyage import delete_voyage
from .GetVoyage import get_voyage
from Lib import Database
from Lib import History

blueprint = Blueprint('Voyage', __name__)

@blueprint.route("/Voyage/SaveVoyage", methods=['GET'])
@cross_origin()
def SaveVoyage():
    voyage_data = request.args.to_dict()

    # Extract the VoyageId, ShipId, StartLocationId, EndLocationId, StartDate, EndDate, and Notes from the voyage_data
    VoyageId = voyage_data.get('VoyageId', None)
    ShipId = voyage_data.get('ShipId', None)
    StartLocationId = voyage_data.get('StartLocationId', None)
    EndLocationId = voyage_data.get('EndLocationId', None)
    StartDate = voyage_data.get('StartDate', None)
    EndDate = voyage_data.get('EndDate', None)
    Notes = voyage_data.get('Notes', None)

    # Call the save_voyage function from SaveVoyage.py with the extracted data
    result = save_voyage(VoyageId, ShipId, StartLocationId, EndLocationId, StartDate, EndDate, Notes)
    History.SaveHistory(voyage_data, "Voyages", "VoyageId", result["VoyageId"])

    return result

@blueprint.route("/Voyage/DeleteVoyage", methods=['GET'])
@cross_origin()
def DeleteVoyage():
    voyage_data = request.args.to_dict()

    # Get the VoyageId from the request data
    VoyageId = voyage_data.get('VoyageId')

    # Call the delete_voyage function from DeleteVoyage.py
    result = delete_voyage(VoyageId)
    History.SaveHistory(voyage_data, "Voyages", "VoyageId", VoyageId)

    return result

@blueprint.route("/Voyage/GetVoyage", methods=['GET'])
@cross_origin()
def GetVoyage():
    voyage_data = request.args.to_dict()

    # Get the VoyageId from the request data
    VoyageId = voyage_data.get('VoyageId')

    # Call the get_voyage function from GetVoyage.py
    result = get_voyage(VoyageId)

    return result
