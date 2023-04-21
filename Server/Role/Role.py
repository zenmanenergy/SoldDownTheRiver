from Lib import Database
from flask import Blueprint, request
from flask_cors import CORS, cross_origin
from .SaveRole import save_role
from .DeleteRole import delete_role
from .GetRole import get_role

blueprint = Blueprint('Role', __name__)

@blueprint.route("/SaveRole", methods=['GET'])
@cross_origin()
def SaveRole():
    role_data = request.args.to_dict()

    # Extract the role from the role_data
    RoleId = role_data.get('RoleId', None)
    Role = role_data.get('Role', None)

    # Call the save_role function from SaveRole.py with the extracted data
    result = save_role(RoleId,Role)

    return result
    
    

@blueprint.route("/DeleteRole", methods=['GET'])
@cross_origin()
def DeleteRole():
    # Get the role data from the request
    role_data = request.args.to_dict()

    # Get the role name from the request
    RoleId = role_data.get('RoleId')
    # Call the delete_role function from DeleteRole.py
    result = delete_role(RoleId)
    return result

@blueprint.route("/GetRole", methods=['GET'])
@cross_origin()
def GetRole():
    # Get the role data from the request
    role_data = request.args.to_dict()

    # Get the role from the request
    RoleId = role_data.get('RoleId')
    
    # Call the get_role function from GetRoles.py
    result = get_role(RoleId)

    return result

