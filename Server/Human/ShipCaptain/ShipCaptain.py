from _Lib import Database
from _Lib.Debugger import Debugger
from _Lib import History
from flask import Blueprint, request
from flask_cors import CORS, cross_origin
from .GetShips import get_ships


blueprint = Blueprint('ShipCaptain', __name__)

		

@blueprint.route("/Human/ShipCaptain/GetShips", methods=['GET'])
@cross_origin()
def GetShips():
	try:
		# Get the role data from the request
		human_data = request.args.to_dict()

		HumanId = human_data.get('HumanId', None)
		# Call the get_role function from GetRoles.py
		result = get_ships(HumanId)

		return result
	except Exception as e:
		return Debugger(e)