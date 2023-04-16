from Lib import Database
from flask import Blueprint, request
from flask_cors import CORS, cross_origin
from .SaveHuman import save_human
from .DeleteHuman import delete_human
from .GetHuman import get_human

blueprint = Blueprint('Human', __name__)

@blueprint.route("/SaveHuman", methods=['GET'])
@cross_origin()
def SaveHuman():
    human_data = request.args.to_dict()

    # Extract the HumanId and HumanName from the human_data
    HumanId = human_data.get('HumanId', None)
    FirstName = human_data.get('FirstName', None)
    MiddleName = human_data.get('MiddleName', None)
    LastName = human_data.get('LastName', None)
    StartYear = human_data.get('StartYear', None)
    EndYear = human_data.get('EndYear', None)
    Notes = human_data.get('Notes', None)

    # Call the save_human function from SaveHuman.py with the extracted data
    result = save_human(HumanId, FirstName, MiddleName, LastName, StartYear, EndYear, Notes)


    return result

@blueprint.route("/DeleteHuman", methods=['GET'])
@cross_origin()
def DeleteHuman():
    # Get the human data from the request
    human_data = request.args.to_dict()

    # Get the human ID from the request
    HumanId = human_data.get('HumanId')
    # Call the delete_human function from DeleteHuman.py
    result = delete_human(HumanId)
    return result

@blueprint.route("/GetHuman", methods=['GET'])
@cross_origin()
def GetHuman():
    # Get the human data from the request
    human_data = request.args.to_dict()

    # Get the human ID from the request
    HumanId = human_data.get('HumanId')
    # Call the get_human function from GetHuman.py
    result = get_human(HumanId)
    return result
