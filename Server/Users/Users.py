from Lib import Database
from Lib.Debugger import Debugger
from flask import Blueprint, request
from flask_cors import CORS, cross_origin
from .GetUsers import get_users

blueprint = Blueprint('Users', __name__)


@blueprint.route("/Users/GetUsers", methods=['GET'])
@cross_origin()
def GetUsers():
	try:
		# Get the user data from the request
		user_data = request.args.to_dict()

		# Call the get_Users function from GetUsers.py
		result = get_users()
		return result
	except Exception as e:
		return Debugger(e)
