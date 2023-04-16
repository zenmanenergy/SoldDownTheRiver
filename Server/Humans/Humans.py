from Lib import Database
from flask import Blueprint, request
from flask_cors import CORS, cross_origin
from .GetHumans import get_humans

blueprint = Blueprint('Humans', __name__ )

@blueprint.route("/GetHumans", methods=['GET'])
@cross_origin()
def GetHumans():
    # Get the human data from the request
    human_data = request.args.to_dict()

    # Call the get_humans function from GetHumans.py
    result = get_humans()
    return result