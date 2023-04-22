from Lib import Database
from flask import Blueprint, request
from flask_cors import CORS, cross_origin
from .GetTransactions import get_transactions

blueprint = Blueprint('Transactions', __name__)


@blueprint.route("/Transactions/GetTransactions", methods=['GET'])
@cross_origin()
def GetTransactions():
    # Get the transaction data from the request
    transaction_data = request.args.to_dict()

    # Call the get_transactions function from GetTransactions.py
    result = get_transactions()
    return result
