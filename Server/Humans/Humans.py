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
		LastFetchTime = human_data.get('LastFetchTime', None)  # Get LastFetchTime from the request
		print("LastFetchTime",LastFetchTime)
		if LastFetchTime == 'null':  # Handle 'null' string explicitly
			LastFetchTime = None

		# Call the get_humans function with Query and LastFetchTime
		result = get_humans(Query, LastFetchTime)
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

