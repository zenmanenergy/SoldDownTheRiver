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
		print(transaction_data)  # Debugging output

		# Extract variables, ensuring correct handling of null values
		TransactionId = transaction_data.get('transactionId', None)
		if TransactionId == "null" or not TransactionId:
			TransactionId = None  # Ensure NULL value is handled correctly

		# Handle date_circa safely
		date_circa = transaction_data.get('date_circa', None)
		if isinstance(date_circa, str) and date_circa.lower() != "null" and date_circa.strip():
			try:
				date_circa = datetime.datetime.strptime(date_circa, '%Y-%m-%d').date()
			except ValueError:
				raise ValueError(f"Invalid date format for date_circa: {date_circa}")
		else:
			date_circa = None  # Ensures None is assigned instead of passing an invalid value

		# Extract additional fields
		date_accuracy = transaction_data.get('date_accuracy', None)
		TransactionType = transaction_data.get('TransactionType', None)
		NotaryHumanId = transaction_data.get('NotaryHumanId', None)
		LocationId = transaction_data.get('LocationId', None)
		TotalPrice = transaction_data.get('TotalPrice', None)
		URL = transaction_data.get('URL', None)
		Notes = transaction_data.get('Notes', None)
		Act = transaction_data.get('Act', None)
		Page = transaction_data.get('Page', None)
		Volume = transaction_data.get('Volume', None)
		Transcriber = transaction_data.get('Transcriber', None)
		isApproved = transaction_data.get('isApproved', '0')
		DataQuestions = transaction_data.get('DataQuestions', None)

		# Convert isApproved to boolean (ensure it's either 0 or 1)
		isApproved = 1 if str(isApproved).lower() in ["true", "1", "yes"] else 0

		# Handle FirstParties and SecondParties safely
		FirstParties = transaction_data.get('FirstParties', '[]')
		SecondParties = transaction_data.get('SecondParties', '[]')

		# Convert from JSON-encoded string to actual list
		import json
		try:
			FirstParties = json.loads(FirstParties) if FirstParties else []
			SecondParties = json.loads(SecondParties) if SecondParties else []
		except json.JSONDecodeError:
			raise ValueError("Invalid JSON format in FirstParties or SecondParties")

		# Call the save_transaction function with the extracted data
		result = save_transaction(
			TransactionId, date_circa, date_accuracy, TransactionType,
			NotaryHumanId, FirstParties, SecondParties, LocationId, TotalPrice,
			URL, Notes, Act, Page, Volume, Transcriber, isApproved, DataQuestions
		)

		# Save history for transactions
		History.SaveHistory(transaction_data, "Transactions", "TransactionId", result["TransactionId"])

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
		
		History.SaveHistory(transaction_data,"transactionhumans", "TransactionId:HumanId", TransactionId+":"+HumanId)
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
		
		History.SaveHistory(transaction_data,"transactionhumans", "TransactionId:HumanId", TransactionId+":"+HumanId)
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
