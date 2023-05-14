from Lib import Database
from flask import Blueprint, request
from flask_cors import CORS, cross_origin
from .GetVoyages import get_voyages

blueprint = Blueprint('Voyages', __name__)  # Update the blueprint name

@blueprint.route("/Voyages/GetVoyages", methods=['GET'])  # Update the route path
@cross_origin()
def GetVoyages():  # Update the function name
    # Get the user data from the request
    user_data = request.args.to_dict()

    # Call the get_voyages function from GetVoyages.py
    result = get_voyages()  # Update the function call
    return result
