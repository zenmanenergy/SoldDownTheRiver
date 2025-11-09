from _Lib import Database
from _Lib.Debugger import Debugger
from flask import Blueprint, request
from flask_cors import CORS, cross_origin
from .GetTransactions import get_transactions
from .GetTransactionsByLocationId import get_transactions_by_location_id
from .GetSearchTransactions import get_searchtransactions

blueprint = Blueprint('Transactions', __name__)


@blueprint.route("/Transactions/GetTransactions", methods=['GET'])
@cross_origin()
def GetTransactions():
	try:
		# Get the transaction data from the request
		transaction_data = request.args.to_dict()

		# Call the get_transactions function from GetTransactions.py
		result = get_transactions()
		return result
	except Exception as e:
		return Debugger(e)
@blueprint.route("/Transactions/GetSearchTransactions", methods=['GET'])
@cross_origin()
def GetSearchTransactions():
	try:
		# Get the transaction data from the request
		transaction_data = request.args.to_dict()

		# Call the get_transactions function from GetTransactions.py
		result = get_searchtransactions()
		return result
	except Exception as e:
		return Debugger(e)

@blueprint.route("/Transactions/GetTransactionsByLocationId", methods=['GET'])
@cross_origin()
def GetTransactionsByLocationId():
	try:
		# Get the LocationId from the request
		location_id = request.args.get('LocationId')
		
		if not location_id:
			return {"error": "LocationId parameter is required"}

		# Call the get_transactions_by_location_id function from GetTransactionsByLocationId.py
		result = get_transactions_by_location_id(location_id)
		return result
	except Exception as e:
		return Debugger(e)
