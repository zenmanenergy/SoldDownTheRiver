from flask import Blueprint, request
from flask_cors import cross_origin
from _Lib.Debugger import Debugger
from .GetFamilies import get_families

blueprint = Blueprint('Families', __name__)

@blueprint.route("/Families/GetFamilies", methods=['GET'])
@cross_origin()
def GetFamilies():
	try:
		# Extract query parameters if needed
		query_params = request.args.to_dict()

		# Call the get_families function to fetch data
		result = get_families()

		return result
	except Exception as e:
		return Debugger(e)
