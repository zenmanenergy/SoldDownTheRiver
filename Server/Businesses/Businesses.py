
from Lib import Database
from flask import Blueprint, request
from flask_cors import CORS, cross_origin
from .GetBusinesses import get_businesses

blueprint = Blueprint('Businesses', __name__)


@blueprint.route("/Businesses/GetBusinesses", methods=['GET'])
@cross_origin()
def GetBusinesses():
    # Get the business data from the request
    business_data = request.args.to_dict()

    # Call the get_business function from GetBusinesses.py
    result = get_businesses()
    return result