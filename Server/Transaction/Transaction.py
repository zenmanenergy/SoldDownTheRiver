from _Lib import Database
from _Lib.Debugger import Debugger
from _Lib import History
import datetime
from flask import Blueprint, request
from flask_cors import CORS, cross_origin
from .SaveTransaction import save_transaction
from .DeleteTransaction import delete_transaction
from .GetTransaction import get_transaction
from .GetNotaryHumans import get_notary_humans
from .GetBusinesses import get_businesses
from .GetTransactionHumans import get_transactionHumans
from .SaveTransactionHuman import save_transactionhuman
from .DeleteTransactionHuman import delete_transactionhuman
from .GetHumans import get_Humans

blueprint = Blueprint('Transaction', __name__)

@blueprint.route("/Transaction/SaveTransaction", methods=['GET'])
@cross_origin()
def SaveTransaction():
	try:
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
	except Exception as e:
		return Debugger(e)
	
	

@blueprint.route("/Transaction/DeleteTransaction", methods=['GET'])
@cross_origin()
def DeleteTransaction():
	try:
		# Get the transaction data from the request
		transaction_data = request.args.to_dict()

		# Get the transaction ID from the request
		TransactionId = transaction_data.get('TransactionId')
		# Call the delete_transaction function from DeleteTransaction.py
		result = delete_transaction(TransactionId)
		return result
	except Exception as e:
		return Debugger(e)

@blueprint.route("/Transaction/GetTransaction", methods=['GET'])
@cross_origin()
def GetTransaction():
	try:
		# Get the transaction data from the request
		transaction_data = request.args.to_dict()

		# Get the transaction ID from the request
		TransactionId = transaction_data.get('TransactionId')
		# Call the get_transaction function from GetTransaction.py
		result = get_transaction(TransactionId)
		return result
	except Exception as e:
		return Debugger(e)




@blueprint.route("/Transaction/GetNotaryHumans", methods=['GET'])
@cross_origin()
def GetNotaryHumans():
	try:
		# Get the transaction data to the request
		transaction_data = request.args.to_dict()

		# Call the get_transaction function to GetTransaction.py
		result = get_notary_humans()
		return result
	except Exception as e:
		return Debugger(e)



@blueprint.route("/Transaction/GetBusinesses", methods=['GET'])
@cross_origin()
def GetBusinesses():
	try:
		# Get the transaction data to the request
		transaction_data = request.args.to_dict()

		# Call the get_transaction function to GetTransaction.py
		result = get_businesses()
		return result
	except Exception as e:
		return Debugger(e)

@blueprint.route("/Transaction/GetTransactionHumans", methods=['GET'])
@cross_origin()
def GetTransactionHumans():
	try:
		# Get the transaction data from the request
		transaction_data = request.args.to_dict()

		# Get the transaction ID from the request
		TransactionId = transaction_data.get('TransactionId')
		# Call the get_transaction function from GetTransaction.py
		result = get_transactionHumans(TransactionId)
		return result
	except Exception as e:
		return Debugger(e)


@blueprint.route("/Transaction/SaveTransactionHuman", methods=['GET'])
@cross_origin()
def SaveTransactionHuman():
	try:
		transaction_data = request.args.to_dict()
		print(transaction_data)

		# Extract the transaction data from the request
		HumanId = transaction_data.get('HumanId', None)
		TransactionId = transaction_data.get('TransactionId', None)
		Price = transaction_data.get('Price', None)
		Notes = transaction_data.get('Notes', None)

		# Call the save_transaction function from SaveTransaction.py with the extracted data
		saveresult = save_transactionhuman(TransactionId, HumanId, Price, Notes)
		
		History.SaveHistory(transaction_data,"TransactionHumans", "TransactionId:HumanId", TransactionId+":"+HumanId)
		result = get_transactionHumans(TransactionId)

		return result
	except Exception as e:
		return Debugger(e)


@blueprint.route("/Transaction/DeleteTransactionHuman", methods=['GET'])
@cross_origin()
def DeleteTransactionHuman():
	try:
		transaction_data = request.args.to_dict()
		print(transaction_data)

		# Extract the transaction data from the request
		HumanId = transaction_data.get('HumanId', None)
		TransactionId = transaction_data.get('TransactionId', None)

		# Call the save_transaction function from SaveTransaction.py with the extracted data
		deleteresult = delete_transactionhuman(TransactionId, HumanId)
		
		History.SaveHistory(transaction_data,"TransactionHumans", "TransactionId:HumanId", TransactionId+":"+HumanId)
		result = get_transactionHumans(TransactionId)

		return result
	except Exception as e:
		return Debugger(e)

@blueprint.route("/Transaction/GetHumans", methods=['GET'])
@cross_origin()
def GetHumans():
	try:
		transaction_data = request.args.to_dict()

		# Get the transaction ID from the request
		TransactionId = transaction_data.get('TransactionId')
		
		result = get_Humans(TransactionId)
		return result
	except Exception as e:
		return Debugger(e)
