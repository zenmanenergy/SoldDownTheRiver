from _Lib import Database
from _Lib.Debugger import Debugger
from flask import Blueprint, request
from flask_cors import CORS, cross_origin
from .GetVoyages import get_voyages

blueprint = Blueprint('Voyages', __name__)  # Update the blueprint name

@blueprint.route("/Voyages/GetVoyages", methods=['GET'])  # Update the route path
@cross_origin()
def GetVoyages():
	try:
		# Update the function name
		# Get the user data from the request
		user_data = request.args.to_dict()

		# Call the get_voyages function from GetVoyages.py
		result = get_voyages()  # Update the function call
		return result
	
	except Exception as e:
		return Debugger(e)
