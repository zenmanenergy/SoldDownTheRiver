from _Lib import Database
from _Lib.Debugger import Debugger
from flask import Blueprint, request, jsonify
from flask_cors import CORS, cross_origin
from .GetRawNOLA import get_RawNOLA
from .GetRawNOLAs import get_RawNOLAs
from .SaveRawNOLA import save_RawNOLA
from .DeleteRawNOLA import delete_RawNOLA

blueprint = Blueprint('RawNOLA', __name__)


@blueprint.route("/RawNOLA/GetNOLA", methods=['GET'])
@cross_origin()
def GetNOLA():
	try:
		# Get the NOLA_ID from the request
		NOLA_ID = request.args.get("NOLA_ID", "")

		# Fetch the NOLA record
		result = get_RawNOLAs([NOLA_ID])
		return jsonify(result)
	except Exception as e:
		return Debugger(e)


@blueprint.route("/RawNOLA/GetRawNOLAs", methods=['GET'])
@cross_origin()
def GetRawNOLAs():
	try:
		# Get the request parameters
		transaction_data = request.args.to_dict()

		# Extract list of NOLA IDs from request
		NOLA_IDs = transaction_data.get("NOLAId", "")

		# Convert comma-separated IDs into a list
		NOLA_ID_list = [nid.strip() for nid in NOLA_IDs.split(",") if nid.strip()]

		# Fetch NOLA records
		result = get_RawNOLAs(NOLA_ID_list)
		return jsonify(result)
	except Exception as e:
		return Debugger(e)


@blueprint.route("/RawNOLA/SaveRawNOLA", methods=['GET'])
@cross_origin()
def SaveRawNOLA():
	try:
		# Get the request parameters from the URL
		SessionId = request.args.get("SessionId", "")
		NOLA_ID = request.args.get("NOLA_ID", "")
		FirstParty = request.args.get("FirstParty", "")
		LocationFirstParty = request.args.get("LocationFirstParty", "")
		SecondParty = request.args.get("SecondParty", "")
		LocationSecondParty = request.args.get("LocationSecondParty", "")
		TypeOfTransaction = request.args.get("TypeOfTransaction", "")
		DateOfTransaction = request.args.get("DateOfTransaction", "")
		Act = request.args.get("Act", "")
		Page = request.args.get("Page", "")
		NotaryPublic = request.args.get("NotaryPublic", "")
		Volume = request.args.get("Volume", "")
		NameOfTranscriber = request.args.get("NameOfTranscriber", "")
		ReferenceURL = request.args.get("ReferenceURL", "")

		# Create a dictionary to mimic the previous NOLA object
		NOLA = {
			"NOLA_ID": NOLA_ID,
			"FirstParty": FirstParty,
			"LocationFirstParty": LocationFirstParty,
			"SecondParty": SecondParty,
			"LocationSecondParty": LocationSecondParty,
			"TypeOfTransaction": TypeOfTransaction,
			"DateOfTransaction": DateOfTransaction,
			"Act": Act,
			"Page": Page,
			"NotaryPublic": NotaryPublic,
			"Volume": Volume,
			"NameOfTranscriber": NameOfTranscriber,
			"ReferenceURL": ReferenceURL
		}

		# Save the NOLA record
		result = save_RawNOLA(SessionId, NOLA)
		return jsonify({"message": "NOLA record saved successfully", "result": result})
	except Exception as e:
		return Debugger(e)


@blueprint.route("/RawNOLA/DeleteRawNOLA", methods=['GET'])
@cross_origin()
def DeleteRawNOLA():
	try:
		# Get the request parameters from the URL
		SessionId = request.args.get("SessionId", "")
		NOLA_ID = request.args.get("NOLA_ID", "")

		# Delete the NOLA record
		result = delete_RawNOLA(SessionId, NOLA_ID)
		return jsonify({"message": "NOLA record deleted successfully", "result": result})
	except Exception as e:
		return Debugger(e)
