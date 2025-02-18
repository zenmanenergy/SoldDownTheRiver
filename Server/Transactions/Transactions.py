from _Lib import Database
from _Lib.Debugger import Debugger
from flask import Blueprint, request
from flask_cors import CORS, cross_origin
from .GetTransactions import get_transactions

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
