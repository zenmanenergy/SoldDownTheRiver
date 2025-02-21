from _Lib import Database
from _Lib.Debugger import Debugger
from flask import Blueprint, request
from flask_cors import CORS, cross_origin
from .GetBusinesses import get_businesses

blueprint = Blueprint('Businesses', __name__)


@blueprint.route("/Businesses/GetBusinesses", methods=['GET'])
@cross_origin()
def GetBusinesses():
	try:
		# Get the business data from the request
		business_data = request.args.to_dict()

		# Call the get_business function from GetBusinesses.py
		result = get_businesses()
		return result
	except Exception as e:
		return Debugger(e)

@blueprint.route("/Businesses/LastModified", methods=['GET'])
@cross_origin()
def LastModified():
	try:

		# Get the business ID from the request
		# result = History.LastModified("business", "BusinessId")
		# return result
		return "unknown"
	except Exception as e:
		return Debugger(e)