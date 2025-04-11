from _Lib import Database
from _Lib.Debugger import Debugger
from _Lib import History
from flask import Blueprint, request
from flask_cors import CORS, cross_origin
from .SaveLocation import save_location
from .DeleteLocation import delete_location
from .GetLocation import get_location
from .GetTimelines import get_timelines

blueprint = Blueprint('Location', __name__)

@blueprint.route("/Location/SaveLocation", methods=['GET'])
@cross_origin()
def SaveLocation():
	try:
		location_data = request.args.to_dict()

		# Extract the location information from the location_data
		LocationId = location_data.get('LocationId', None)
		Name = location_data.get('Name', None)
		Address = location_data.get('Address', None)
		City = location_data.get('City', None)
		State = location_data.get('State', None)
		County = location_data.get('County', None)
		Country = location_data.get('Country', None)
		Latitude = location_data.get('Latitude', None)
		Longitude = location_data.get('Longitude', None)

		# Call the save_location function from SaveLocation.py with the extracted data
		result = save_location(LocationId, Name,Address,City, State, County, Country, Latitude, Longitude)
		

		return result
	except Exception as e:
		return Debugger(e)
	
	

@blueprint.route("/Location/DeleteLocation", methods=['GET'])
@cross_origin()
def DeleteLocation():
	try:
		# Get the location information from the request
		location_data = request.args.to_dict()

		# Get the location ID from the request
		LocationId = location_data.get('LocationId')
		# Call the delete_location function from DeleteLocation.py
		result = delete_location(LocationId)
		History.SaveHistory(location_data,"locations", "LocationId", LocationId)
		return result
	except Exception as e:
		return Debugger(e)

@blueprint.route("/Location/GetLocation", methods=['GET'])
@cross_origin()
def GetLocation():
	try:
		# Get the location information from the request
		location_data = request.args.to_dict()

		# Get the location ID from the request
		LocationId = location_data.get('LocationId')
		# Call the get_location function from GetLocation.py
		result = get_location(LocationId)
		return result
	except Exception as e:
		return Debugger(e)

@blueprint.route("/Location/GetTimelines", methods=['GET'])
@cross_origin()
def GetTimelines():
	try:
		LoginData = request.args.to_dict()
		LocationId = LoginData.get('LocationId', None)
		# Call the get_locations function to retrieve location data
		result = get_timelines(LocationId)
		return result
	except Exception as e:
		return Debugger(e)