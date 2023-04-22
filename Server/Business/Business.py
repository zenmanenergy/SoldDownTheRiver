
from Lib import Database
from flask import Blueprint, request
from flask_cors import CORS, cross_origin
from .SaveBusiness import save_business
from .DeleteBusiness import delete_business
from .GetBusiness import get_business

blueprint = Blueprint('Business', __name__)

@blueprint.route("/Business/SaveBusiness", methods=['GET'])
@cross_origin()
def SaveBusiness():
    business_data = request.args.to_dict()

    # Extract the BusinessId and BusinessName from the business_data
    BusinessId = business_data.get('BusinessId', None)
    BusinessName = business_data.get('BusinessName', None)

    # Call the save_business function from SaveBusiness.py with the extracted data
    result = save_business(BusinessId, BusinessName)

    return result
    
    

@blueprint.route("/Business/DeleteBusiness", methods=['GET'])
@cross_origin()
def DeleteBusiness():
    # Get the business data from the request
    business_data = request.args.to_dict()

    # Get the business ID from the request
    BusinessId = business_data.get('BusinessId')
    # Call the delete_business function from DeleteBusiness.py
    result = delete_business(BusinessId)
    return result

@blueprint.route("/Business/GetBusiness", methods=['GET'])
@cross_origin()
def GetBusiness():
    # Get the business data from the request
    business_data = request.args.to_dict()

    # Get the business ID from the request
    BusinessId = business_data.get('BusinessId')
    # Call the get_business function from GetBusiness.py
    result = get_business(BusinessId)
    return result