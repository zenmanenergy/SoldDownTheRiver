from _Lib import Database
from _Lib.Debugger import Debugger
from flask import Blueprint, request
from flask_cors import CORS, cross_origin
from .GetRoles import get_roles
from .GetSellers import get_sellers
from .GetBuyers import get_buyers
from .GetShippingAgents import get_shippingagents
from .GetCollectorAgents import get_CollectorAgents


blueprint = Blueprint('Roles', __name__)


@blueprint.route("/Roles/GetRoles", methods=['GET'])
@cross_origin()
def GetRoles():
	try:
		# Get the role data from the request
		role_data = request.args.to_dict()

		# Call the get_roles function from GetRoles.py
		result = get_roles()
		return result
	except Exception as e:
		return Debugger(e)


@blueprint.route("/Roles/GetSellers", methods=['GET'])
@cross_origin()
def GetSellers():
	try:
		# Get the role data from the request
		role_data = request.args.to_dict()

		result = get_sellers()
		return result
	except Exception as e:
		return Debugger(e)


@blueprint.route("/Roles/GetShippingAgents", methods=['GET'])
@cross_origin()
def ShippingAgents():
	try:
		# Get the role data from the request
		role_data = request.args.to_dict()

		result = get_shippingagents()
		return result
	except Exception as e:
		return Debugger(e)

@blueprint.route("/Roles/GetCollectorAgents", methods=['GET'])
@cross_origin()
def CollectorAgents():
	try:
		# Get the role data from the request
		role_data = request.args.to_dict()

		result = get_CollectorAgents()
		return result
	except Exception as e:
		return Debugger(e)



@blueprint.route("/Roles/GetBuyers", methods=['GET'])
@cross_origin()
def Buyers():
	try:
		# Get the role data from the request
		role_data = request.args.to_dict()

		result = get_buyers()
		return result
	except Exception as e:
		return Debugger(e)
