from flask import Blueprint, request
from flask_cors import CORS, cross_origin
from Lib import Database
from Lib.Debugger import Debugger
from Lib import History
from .GetVoyageHuman import get_VoyageHuman

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

