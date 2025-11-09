from _Lib.Debugger import Debugger
from flask import Blueprint, jsonify, request
from flask_cors import CORS, cross_origin
from .GetLocations import get_locations
from .GetSearchLocations import get_search_locations

blueprint = Blueprint('Locations', __name__)


@blueprint.route("/Locations/GetLocations", methods=['GET'])
@cross_origin()
def GetLocations():
	try:
		# Call the get_locations function to retrieve location data
		result = get_locations()
		return result
	except Exception as e:
		return Debugger(e)
	
@blueprint.route("/Locations/GetSearchLocations", methods=['GET'])
@cross_origin()
def GetSearchLocations():
	try:
		# Call the get_locations function to retrieve location data
		result = get_search_locations()
		return result
	except Exception as e:
		return Debugger(e)
	
	
