
from Lib import Database
from Lib.Debugger import Debugger
from Lib import History
from flask import Blueprint, request
from flask_cors import CORS, cross_origin
from .GetBusinesses import get_businesses
from .GetHumans import get_humans
from .GetLocations import get_locations
from .GetRoles import get_roles
from .GetTransactions import get_transactions

blueprint = Blueprint('Search', __name__)

@blueprint.route("/Search/Businesses", methods=['GET'])
@cross_origin()
def SearchBusinesses():
	try:
		business_data = request.args.to_dict()

		# Extract the BusinessId and BusinessName from the business_data
		BusinessName = business_data.get('BusinessName', None)

		# Call the save_business function from SaveBusiness.py with the extracted data
		result = get_businesses(BusinessName)


		return result
	except Exception as e:
		return Debugger(e)
@blueprint.route("/Search/Humans", methods=['GET'])
@cross_origin()
def SearchHumans():
	try:
		human_data = request.args.to_dict()


		FirstName = human_data.get('FirstName', None)
		LastName = human_data.get('LastName', None)
		MiddleName = human_data.get('MiddleName', None)


		result = get_humans(FirstName, MiddleName, LastName)


		return result
	except Exception as e:
		return Debugger(e)

@blueprint.route("/Search/Locations", methods=['GET'])
@cross_origin()
def SearchLocations():
	try:
		location_data = request.args.to_dict()

		
		City = location_data.get('City', None)
		State = location_data.get('State', None)
		Country = location_data.get('Country', None)


		result = get_locations(City, State, Country)


		return result
	except Exception as e:
		return Debugger(e)

@blueprint.route("/Search/Roles", methods=['GET'])
@cross_origin()
def SearchRoles():
	try:
		roles_data = request.args.to_dict()

		
		Role = roles_data.get('Role', None)


		result = get_roles(Role)


		return result
	except Exception as e:
		return Debugger(e)

@blueprint.route("/Search/Transactions", methods=['GET'])
@cross_origin()
def SearchTransactions():
	try:
		transactions_data = request.args.to_dict()

		
		TransactionId = transactions_data.get('TransactionId', None)
		TransactionDate = transactions_data.get('TransactionDate', None)


		result = get_transactions(TransactionId, TransactionDate)


		return result
	except Exception as e:
		return Debugger(e)