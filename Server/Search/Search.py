
from Lib import Database
from Lib import History
from flask import Blueprint, request
from flask_cors import CORS, cross_origin
from .GetBusinesses import get_businesses
from .GetHumans import get_humans

blueprint = Blueprint('Search', __name__)

@blueprint.route("/Search/Businesses", methods=['GET'])
@cross_origin()
def SearchBusinesses():
    business_data = request.args.to_dict()

    # Extract the BusinessId and BusinessName from the business_data
    BusinessName = business_data.get('BusinessName', None)

    # Call the save_business function from SaveBusiness.py with the extracted data
    result = get_businesses(BusinessName)


    return result
@blueprint.route("/Search/Humans", methods=['GET'])
@cross_origin()
def SearchHumans():
    human_data = request.args.to_dict()

    # Extract the BusinessId and BusinessName from the business_data
    FirstName = human_data.get('FirstName', None)
    LastName = human_data.get('LastName', None)

    # Call the save_business function from SaveBusiness.py with the extracted data
    result = get_humans(FirstName, LastName)


    return result