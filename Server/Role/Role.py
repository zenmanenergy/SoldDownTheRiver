from Lib import Database
from Lib.Debugger import Debugger
from Lib import History
from flask import Blueprint, request
from flask_cors import CORS, cross_origin
from .SaveRole import save_role
from .DeleteRole import delete_role
from .GetRole import get_role
from .GetRoleHumans import get_roleHumans
from .GetHumans import get_Humans
from .SaveHumanRole import save_HumanRole
from .DeleteHumanRole import delete_HumanRole

from Lib import History

blueprint = Blueprint('Role', __name__)

@blueprint.route("/Role/SaveRole", methods=['GET'])
@cross_origin()
def SaveRole():
	try:
		role_data = request.args.to_dict()

		# Extract the role from the role_data
		RoleId = role_data.get('RoleId', None)
		Role = role_data.get('Role', None)

		# Call the save_role function from SaveRole.py with the extracted data
		result = save_role(RoleId,Role)
		print(result)
		History.SaveHistory(role_data,"Roles", "RoleId", result["RoleId"])

		return result
	except Exception as e:
		return Debugger(e)
	
	

@blueprint.route("/Role/DeleteRole", methods=['GET'])
@cross_origin()
def DeleteRole():
	try:
		# Get the role data from the request
		role_data = request.args.to_dict()

		# Get the role name from the request
		RoleId = role_data.get('RoleId')
		# Call the delete_role function from DeleteRole.py
		result = delete_role(RoleId)
		History.SaveHistory(role_data,"Roles", "RoleId", RoleId)
		return result
	except Exception as e:
		return Debugger(e)

@blueprint.route("/Role/GetRole", methods=['GET'])
@cross_origin()
def GetRole():
	try:
		# Get the role data from the request
		role_data = request.args.to_dict()

		# Get the role from the request
		RoleId = role_data.get('RoleId')
		
		# Call the get_role function from GetRoles.py
		result = get_role(RoleId)

		return result
	except Exception as e:
		return Debugger(e)

@blueprint.route("/Role/GetRoleHumans", methods=['GET'])
@cross_origin()
def GetRoleHumans():
	try:
		# Get the role data from the request
		role_data = request.args.to_dict()

		# Get the role from the request
		RoleId = role_data.get('RoleId')
		
		# Call the get_role function from GetRoles.py
		result = get_roleHumans(RoleId)

		return result
	except Exception as e:
		return Debugger(e)


@blueprint.route("/Role/GetHumans", methods=['GET'])
@cross_origin()
def GetHumans():
	try:
		# Get the role data from the request
		role_data = request.args.to_dict()
		RoleId = role_data.get('RoleId')
		
		Query = role_data.get('Query')
		
		
		# Call the get_role function from GetRoles.py
		result = get_Humans(RoleId,Query)

		return result
	except Exception as e:
		return Debugger(e)

@blueprint.route("/Role/SaveHumanRole", methods=['GET'])
@cross_origin()
def SaveHumanRole():
	try:
		role_data = request.args.to_dict()
		RoleId = role_data.get('RoleId')
		HumanId = role_data.get('HumanId')
		
		
		# Call the get_role function from GetRoles.py
		result = save_HumanRole(HumanId,RoleId)

		return result
	except Exception as e:
		return Debugger(e)

@blueprint.route("/Role/DeleteHumanRole", methods=['GET'])
@cross_origin()
def DeleteHumanRole():
	try:
		role_data = request.args.to_dict()
		RoleId = role_data.get('RoleId')
		HumanId = role_data.get('HumanId')
		
		
		# Call the get_role function from GetRoles.py
		result = delete_HumanRole(HumanId,RoleId)

		return result
	except Exception as e:
		return Debugger(e)

		