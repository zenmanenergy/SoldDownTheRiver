from flask import Blueprint, request
from flask_cors import CORS, cross_origin
from _Lib import Database
from _Lib.Debugger import Debugger
from _Lib import History
from .GetVoyageHuman import get_VoyageHuman
from Human.SaveHuman import save_human
from ..SaveVoyageHuman import save_VoyageHuman

blueprint = Blueprint('VoyageEnslavedPerson', __name__)



	
@blueprint.route("/Voyage/EnslavedPerson/GetVoyageHuman", methods=['GET'])
@cross_origin()
def GetVoyageHuman():
	try:
		# Get the user data from the request
		Voyage_data = request.args.to_dict()
		VoyageId = Voyage_data.get('VoyageId')
		HumanId = Voyage_data.get('HumanId')

		# Call the get_Ships function from GetShips.py
		result = get_VoyageHuman(VoyageId,HumanId)
		return result
	except Exception as e:
		return Debugger(e)
	
@blueprint.route("/Voyage/EnslavedPerson/SaveEnslavedPerson", methods=['GET'])
@cross_origin()
def SaveEnslavedPerson():
	try:
		# Get the user data from the request
		Voyage_data = request.args.to_dict()
		VoyageId = Voyage_data.get('VoyageId', None)
		HumanId = Voyage_data.get('HumanId', None)
		
		RoleId = Voyage_data.get('RoleId', None)
		FirstName = Voyage_data.get('FirstName', None)
		MiddleName = Voyage_data.get('MiddleName', None)
		LastName = Voyage_data.get('LastName', None)
		SellingSlaveTraderHumanId = Voyage_data.get('SellingSlaveTraderHumanId', None)
		BuyingSlaveTraderHumanId = Voyage_data.get('BuyingSlaveTraderHumanId', None)
		ShippingAgentHumanId = Voyage_data.get('ShippingAgentHumanId', None)
		CollectingAgentHumanId = Voyage_data.get('CollectingAgentHumanId', None)
		Notes = Voyage_data.get('Notes', None)

		# Call the get_Ships function from GetShips.py
		result = save_human(HumanId, FirstName, MiddleName, LastName, Notes)
		HumanId=result['HumanId']
		result = save_VoyageHuman(VoyageId, HumanId, RoleId, SellingSlaveTraderHumanId,BuyingSlaveTraderHumanId,ShippingAgentHumanId,CollectingAgentHumanId,Notes)
		History.SaveHistory(Voyage_data, "voyagehumans", "VoyageId:HumanId", VoyageId+": "+HumanId)
		return result
	except Exception as e:
		return Debugger(e)

