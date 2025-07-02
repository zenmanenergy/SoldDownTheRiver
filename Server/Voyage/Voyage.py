from flask import Blueprint, request
from flask_cors import CORS, cross_origin
from .SaveVoyage import save_Voyage
from .DeleteVoyage import delete_Voyage
from .GetVoyage import get_Voyage
from _Lib import Database
from _Lib.Debugger import Debugger
from _Lib import History
from .GetShips import get_Ships
from .GetHumans import get_Humans
from .SaveVoyageHuman import save_VoyageHuman
from .GetVoyageHumans import get_VoyageHumans
from .DeleteVoyageHuman import delete_VoyageHuman
from .GetRoles import get_roles
from .GetLocations import get_locations
from .GetCaptains import get_Captains
from .GetSlaveTraders import get_SlaveTraders
from .GetSlaveShippingAgents import get_SlaveShippingAgents
from .GetSlaveCollectorAgents import get_SlaveCollectorAgents

blueprint = Blueprint('Voyage', __name__)

@blueprint.route("/Voyage/SaveVoyage", methods=['GET'])
@cross_origin()
def SaveVoyage():
	try:
		Voyage_data = request.args.to_dict()

		# Extract the VoyageId, ShipId, StartLocationId, EndLocationId, StartDate, EndDate, and Notes from the Voyage_data
		VoyageId = Voyage_data.get('VoyageId', None)
		ShipId = Voyage_data.get('ShipId', None)
		CaptainHumanId = Voyage_data.get('CaptainHumanId', None)
		StartLocationId = Voyage_data.get('StartLocationId', None)
		EndLocationId = Voyage_data.get('EndLocationId', None)
		StartDate = Voyage_data.get('StartDate', None)
		EndDate = Voyage_data.get('EndDate', None)
		Notes = Voyage_data.get('Notes', None)

		# Call the save_Voyage function from SaveVoyage.py with the extracted data
		result = save_Voyage(VoyageId, ShipId, CaptainHumanId,StartLocationId, EndLocationId, StartDate, EndDate, Notes)
		
		
		return result
	except Exception as e:
		return Debugger(e)

@blueprint.route("/Voyage/DeleteVoyage", methods=['GET'])
@cross_origin()
def DeleteVoyage():
	try:
		Voyage_data = request.args.to_dict()

		# Get the VoyageId from the request data
		VoyageId = Voyage_data.get('VoyageId')

		# Call the delete_Voyage function from DeleteVoyage.py
		result = delete_Voyage(VoyageId)
		History.SaveHistory(Voyage_data, "voyages", "VoyageId", VoyageId)

		return result
	except Exception as e:
		return Debugger(e)

@blueprint.route("/Voyage/GetVoyage", methods=['GET'])
@cross_origin()
def GetVoyage():
	try:
		Voyage_data = request.args.to_dict()

		# Get the VoyageId from the request data
		VoyageId = Voyage_data.get('VoyageId')

		# Call the get_Voyage function from GetVoyage.py
		result = get_Voyage(VoyageId)

		return result
	except Exception as e:
		return Debugger(e)

@blueprint.route("/Voyage/GetShips", methods=['GET'])
@cross_origin()
def GetShips():
	try:
		# Get the user data from the request
		Voyage_data = request.args.to_dict()

		# Call the get_Ships function from GetShips.py
		result = get_Ships()
		return result
	except Exception as e:
		return Debugger(e)

@blueprint.route("/Voyage/GetHumans", methods=['GET'])
@cross_origin()
def GetHumans():
	try:
		# Get the user data from the request
		Voyage_data = request.args.to_dict()
		VoyageId = Voyage_data.get('VoyageId')

		# Call the get_Ships function from GetShips.py
		result = get_Humans(VoyageId)
		return result
	except Exception as e:
		return Debugger(e)

	
@blueprint.route("/Voyage/SaveVoyageHuman", methods=['GET'])
@cross_origin()
def SaveVoyageHuman():
	try:
		Voyage_data = request.args.to_dict()

		# Extract the VoyageId, ShipId, StartLocationId, EndLocationId, StartDate, EndDate, and Notes from the Voyage_data
		VoyageId = Voyage_data.get('VoyageId', None)
		HumanId = Voyage_data.get('HumanId', None)
		RoleId = Voyage_data.get('RoleId', None)
		owner_humanid = Voyage_data.get('owner_humanid', None)
		owner2_humanid = Voyage_data.get('owner2_humanid', None)
		shippingagent_humanid = Voyage_data.get('shippingagent_humanid', None)
		collectoragent_HumanId = Voyage_data.get('collectoragent_HumanId', None)
		Notes = Voyage_data.get('Notes', None)
		
		
		
		
		
		
		
		

		# Call the save_Voyage function from SaveVoyage.py with the extracted data
		result = save_VoyageHuman(VoyageId, HumanId, RoleId, owner_humanid,owner2_humanid,shippingagent_humanid,collectoragent_HumanId,Notes)
		
		return result
	except Exception as e:
		return Debugger(e)


	
@blueprint.route("/Voyage/GetVoyageHumans", methods=['GET'])
@cross_origin()
def GetVoyageHumans():
	try:
		# Get the user data from the request
		Voyage_data = request.args.to_dict()
		VoyageId = Voyage_data.get('VoyageId')

		# Call the get_Ships function from GetShips.py
		result = get_VoyageHumans(VoyageId)
		return result
	except Exception as e:
		return Debugger(e)


	
@blueprint.route("/Voyage/DeleteVoyageHuman", methods=['GET'])
@cross_origin()
def DeleteVoyageHumans():
	try:
		# Get the user data from the request
		Voyage_data = request.args.to_dict()
		VoyageId = Voyage_data.get('VoyageId')
		HumanId = Voyage_data.get('HumanId')

		# Call the get_Ships function from GetShips.py
		result = delete_VoyageHuman(VoyageId, HumanId)
		History.SaveHistory(Voyage_data, "voyagehumans", "VoyageId:HumanId", VoyageId+": "+HumanId)
		return result
	except Exception as e:
		return Debugger(e)


@blueprint.route("/Voyage/GetRoles", methods=['GET'])
@cross_origin()
def GetRoles():
	try:
		# Get the user data from the request
		Voyage_data = request.args.to_dict()
		VoyageId = Voyage_data.get('VoyageId')

		# Call the get_Ships function from GetShips.py
		result = get_roles(VoyageId)
		return result
	except Exception as e:
		return Debugger(e)

@blueprint.route("/Voyage/GetLocations", methods=['GET'])
@cross_origin()
def GetLocations():
	try:
		# Call the get_locations function to retrieve location data
		result = get_locations()
		return result
	except Exception as e:
		return Debugger(e)


@blueprint.route("/Voyage/GetCaptains", methods=['GET'])
@cross_origin()
def GetCaptains():
	try:
		# Call the get_Captains function to retrieve location data
		result = get_Captains()
		return result
	except Exception as e:
		return Debugger(e)

@blueprint.route("/Voyage/GetSlaveTraders", methods=['GET'])
@cross_origin()
def GetSlaveTraders():
	try:
		result = get_SlaveTraders()
		return result
	except Exception as e:
		return Debugger(e)
@blueprint.route("/Voyage/GetSlaveShippingAgents", methods=['GET'])
@cross_origin()
def GetSlaveShippingAgents():
	try:
		result = get_SlaveShippingAgents()
		return result
	except Exception as e:
		return Debugger(e)
@blueprint.route("/Voyage/GetSlaveCollectorAgents", methods=['GET'])
@cross_origin()
def GetSlaveCollectorAgents():
	try:
		result = get_SlaveCollectorAgents()
		return result
	except Exception as e:
		return Debugger(e)

