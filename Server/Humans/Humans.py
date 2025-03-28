from _Lib import Database
from _Lib.Debugger import Debugger
from flask import Blueprint, request
from flask_cors import CORS, cross_origin
from .GetHumans import get_humans
from .SetTimelines import set_timelines

blueprint = Blueprint('Humans', __name__ )

@blueprint.route("/Humans/GetHumans", methods=['GET'])
@cross_origin()
def GetHumans():
	try:
		# Get the human data from the request
		human_data = request.args.to_dict()
		Query = human_data.get('Query', None)

		# Call the get_humans function from GetHumans.py
		result = get_humans(Query)
		return result
	except Exception as e:
		return Debugger(e)

@blueprint.route("/Humans/SetTimelines", methods=['GET'])
@cross_origin()
def SetTimelines():
	try:
		

		# Call the set_timelines function from SetTimelines.py
		result = set_timelines()
		return result
	except Exception as e:
		return Debugger(e)

