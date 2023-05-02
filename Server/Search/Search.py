
from Lib import Database
from Lib import History
from flask import Blueprint, request
from flask_cors import CORS, cross_origin
from .GetBusiness import get_business

blueprint = Blueprint('Search', __name__)

@blueprint.route("/Search/Business", methods=['GET'])
@cross_origin()
def SearchBusiness():
    business_data = request.args.to_dict()

    # Extract the BusinessId and BusinessName from the business_data
    BusinessName = business_data.get('BusinessName', None)

    # Call the save_business function from SaveBusiness.py with the extracted data
    result = get_business(BusinessName)


    return result