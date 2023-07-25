from Lib import Database
from Lib.Debugger import Debugger
from flask import Blueprint, request
from flask_cors import CORS, cross_origin
from .GetHumans import get_humans

blueprint = Blueprint('Humans', __name__ )

@blueprint.route("/Humans/GetHumans", methods=['GET'])
@cross_origin()
def GetHumans():
	try:
		# Get the human data from the request
		human_data = request.args.to_dict()

		# Call the get_humans function from GetHumans.py
		result = get_humans()
		return result
	except Exception as e:
		return Debugger(e)