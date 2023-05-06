from Lib import Database
from Lib import History
import datetime
from flask import Blueprint, request
from flask_cors import CORS, cross_origin
from .SaveTransaction import save_transaction
from .DeleteTransaction import delete_transaction
from .GetTransaction import get_transaction
from .GetFromHumans import get_from_humans
from .GetToHumans import get_to_humans
from .GetNotaryHumans import get_notary_humans
from .GetBusinesses import get_businesses

blueprint = Blueprint('Transaction', __name__)

@blueprint.route("/Transaction/SaveTransaction", methods=['GET'])
@cross_origin()
def SaveTransaction():
    transaction_data = request.args.to_dict()
    print(transaction_data)

    # Extract the transaction data from the request
    TransactionId = transaction_data.get('TransactionId', None)
    TransactionDate = transaction_data.get('TransactionDate', None)
    TransactionDate = datetime.datetime.strptime(TransactionDate, '%Y-%m-%d')
    
    FromBusinessId = transaction_data.get('FromBusinessId', None)
    ToBusinessId = transaction_data.get('ToBusinessId', None)
    TransactionType = transaction_data.get('TransactionType', None)
    Notes = transaction_data.get('Notes', None)
    Act = transaction_data.get('Act', None)
    Page = transaction_data.get('Page', None)
    NotaryBusinessId = transaction_data.get('NotaryBusinessId', None)
    Volume = transaction_data.get('Volume', None)
    URL = transaction_data.get('URL', None)

    # Call the save_transaction function from SaveTransaction.py with the extracted data
    result = save_transaction(TransactionId, TransactionDate, FromBusinessId, ToBusinessId, TransactionType, Notes, Act, Page, NotaryBusinessId, Volume, URL)
    History.SaveHistory(transaction_data,"Transactions", "TransactionId", result["TransactionId"])

    return result
    
    

@blueprint.route("/Transaction/DeleteTransaction", methods=['GET'])
@cross_origin()
def DeleteTransaction():
    # Get the transaction data from the request
    transaction_data = request.args.to_dict()

    # Get the transaction ID from the request
    TransactionId = transaction_data.get('TransactionId')
    # Call the delete_transaction function from DeleteTransaction.py
    result = delete_transaction(TransactionId)
    return result

@blueprint.route("/Transaction/GetTransaction", methods=['GET'])
@cross_origin()
def GetTransaction():
    # Get the transaction data from the request
    transaction_data = request.args.to_dict()

    # Get the transaction ID from the request
    TransactionId = transaction_data.get('TransactionId')
    # Call the get_transaction function from GetTransaction.py
    result = get_transaction(TransactionId)
    return result


@blueprint.route("/Transaction/GetFromHumans", methods=['GET'])
@cross_origin()
def GetFromHumans():
    # Get the transaction data to the request
    transaction_data = request.args.to_dict()

    # Call the get_transaction function to GetTransaction.py
    result = get_from_humans()
    return result

@blueprint.route("/Transaction/GetToHumans", methods=['GET'])
@cross_origin()
def GetToHumans():
    # Get the transaction data to the request
    transaction_data = request.args.to_dict()

    # Call the get_transaction function to GetTransaction.py
    result = get_to_humans()
    return result


@blueprint.route("/Transaction/GetNotaryHumans", methods=['GET'])
@cross_origin()
def GetNotaryHumans():
    # Get the transaction data to the request
    transaction_data = request.args.to_dict()

    # Call the get_transaction function to GetTransaction.py
    result = get_notary_humans()
    return result



@blueprint.route("/Transaction/GetBusinesses", methods=['GET'])
@cross_origin()
def GetBusinesses():
    # Get the transaction data to the request
    transaction_data = request.args.to_dict()

    # Call the get_transaction function to GetTransaction.py
    result = get_businesses()
    return result