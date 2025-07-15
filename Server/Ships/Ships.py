from _Lib import Database
from _Lib.Debugger import Debugger
from flask import Blueprint, request
from flask_cors import CORS, cross_origin
from .GetShips import get_ships
from .GetShips import search_ships

blueprint = Blueprint('Ships', __name__)

@blueprint.route("/Ships/GetShips", methods=['GET'])
@cross_origin()
def GetShips():
	# Get the user data from the request
	user_data = request.args.to_dict()

	# Call the get_ships function from GetShips.py
	result = get_ships()
	return result

@blueprint.route("/Ships/Searchhips", methods=['GET'])
@cross_origin()
def Searchhips():
	# Get the user data from the request
	user_data = request.args.to_dict()

	# Call the get_ships function from Searchhips.py
	result = search_ships()
	return result
