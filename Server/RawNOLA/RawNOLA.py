from _Lib import Database
from _Lib.Debugger import Debugger
from flask import Blueprint, request
from flask_cors import CORS, cross_origin
from .GetRawNOLA import get_RawNOLA

blueprint = Blueprint('RawNOLA', __name__)


@blueprint.route("/RawNOLA/GetRawNOLA", methods=['GET'])
@cross_origin()
def GetRawNOLA():
	try:
		# Get the transaction data from the request
		transaction_data = request.args.to_dict()

		# Call the get_transactions function from GetRawNOLA.py
		result = get_RawNOLA()
		return result
	except Exception as e:
		return Debugger(e)
