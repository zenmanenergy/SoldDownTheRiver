from _Lib import Database
from _Lib.Debugger import Debugger
from _Lib import History
from flask import Blueprint, request
from flask_cors import CORS, cross_origin
from .SaveShip import save_ship
from .DeleteShip import delete_ship
from .GetShip import get_ship
from .GetCaptains import get_Captains
from .GetAgents import get_Agents
from .GetShipVoyages import get_ShipVoyages
from .GetLocations import get_locations
from .GetTransactions import get_Transactions

blueprint = Blueprint('Ship', __name__)

@blueprint.route("/Ship/SaveShip", methods=['GET'])
@cross_origin()
def SaveShip():
	try:
		ship_data = request.args.to_dict()

		# Extract the ShipId, BuildDate, Notes, ShipType, and Size from the ship_data
		ShipId = ship_data.get('ShipId', None)
		ShipName = ship_data.get('ShipName', None)
		BuildDate = ship_data.get('BuildDate', None)
		Notes = ship_data.get('Notes', None)
		ShipType = ship_data.get('ShipType', None)
		Size = ship_data.get('Size', None)
		HomePortLocationId = ship_data.get('HomePortLocationId', None)

		# Call the save_ship function from SaveShip.py with the extracted data
		result = save_ship(ShipId, ShipName, BuildDate, Notes, ShipType, Size, HomePortLocationId)
		History.SaveHistory(ship_data, "ships", "ShipId", result["ShipId"])

		return result
	except Exception as e:
		return Debugger(e)
	

@blueprint.route("/Ship/DeleteShip", methods=['GET'])
@cross_origin()
def DeleteShip():
	try:
		# Get the ship data from the request
		ship_data = request.args.to_dict()

		# Get the ship ID from the request
		ShipId = ship_data.get('ShipId')
		# Call the delete_ship function from DeleteShip.py
		result = delete_ship(ShipId)
		History.SaveHistory(ship_data, "ships", "ShipId", ShipId)
		return result
	except Exception as e:
		return Debugger(e)

@blueprint.route("/Ship/GetShip", methods=['GET'])
@cross_origin()
def GetShip():
	try:
		# Get the ship data from the request
		ship_data = request.args.to_dict()

		# Get the ship ID from the request
		ShipId = ship_data.get('ShipId')
		# Call the get_ship function from GetShip.py
		result = get_ship(ShipId)
		return result
	except Exception as e:
		return Debugger(e)


@blueprint.route("/Ship/GetCaptains", methods=['GET'])
@cross_origin()
def GetCaptains():
	try:
		# Get the ship data from the request
		ship_data = request.args.to_dict()

		# Get the ship ID from the request
		Query = ship_data.get('Query')
		# Call the get_ship function from GetCaptains.py
		result = get_Captains(Query)
		return result
	except Exception as e:
		return Debugger(e)

@blueprint.route("/Ship/GetAgents", methods=['GET'])
@cross_origin()
def GetAgents():
	try:
		# Get the ship data from the request
		ship_data = request.args.to_dict()

		# Get the ship ID from the request
		Query = ship_data.get('Query')
		# Call the get_ship function from GetAgents.py
		result = get_Agents(Query)
		return result
	except Exception as e:
		return Debugger(e)



@blueprint.route("/Ship/GetShipVoyages", methods=['GET'])
@cross_origin()
def GetShipVoyages():
	try:
		# Get the ship data from the request
		ship_data = request.args.to_dict()

		# Get the ship ID from the request
		ShipId = ship_data.get('ShipId')
		# Call the get_ship function from GetShipVoyages.py
		result = get_ShipVoyages(ShipId)
		return result
	except Exception as e:
		return Debugger(e)

@blueprint.route("/Ship/GetLocations", methods=['GET'])
@cross_origin()
def GetLocations():
	try:
		# Call the get_locations function to retrieve location data
		result = get_locations()
		return result
	except Exception as e:
		return Debugger(e)

@blueprint.route("/Ship/GetTransactions", methods=['GET'])
@cross_origin()
def GetTransactions():
	try:
		ship_data = request.args.to_dict()
		ShipId = ship_data.get('ShipId')
		# Call the get_Transactions function to retrieve Transaction data
		result = get_Transactions(ShipId)
		return result
	except Exception as e:
		return Debugger(e)