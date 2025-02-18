from _Lib import Database
from _Lib.Debugger import Debugger
from flask import Blueprint, request
from flask_cors import CORS, cross_origin
from .GetRoles import get_roles

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
