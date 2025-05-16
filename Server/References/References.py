from _Lib import Database
from _Lib.Debugger import Debugger
from flask import Blueprint, request
from flask_cors import cross_origin
from .GetReferences import get_references
from .GetReference import get_reference
from .SaveReference import save_reference
from .DeleteReference import delete_reference

blueprint = Blueprint('References', __name__)

@blueprint.route("/References/GetReferences", methods=['GET'])
@cross_origin()
def GetReferences():
	try:
		SessionId = request.args.get('SessionId', '')
		result = get_references(SessionId)
		return result
	except Exception as e:
		return Debugger(e)

@blueprint.route("/References/GetReference", methods=['GET'])
@cross_origin()
def GetReference():
	try:
		SessionId = request.args.get('SessionId', '')
		ReferenceId = request.args.get('ReferenceId', '')
		result = get_reference(SessionId, ReferenceId)
		return result
	except Exception as e:
		return Debugger(e)

@blueprint.route("/References/SaveReference", methods=['GET'])
@cross_origin()
def SaveReference():
	try:
		SessionId = request.args.get('SessionId', '')
		ReferenceId = request.args.get('ReferenceId', '')
		URL = request.args.get('URL', '')
		Notes = request.args.get('Notes', '')
		result = save_reference(SessionId, ReferenceId, URL, Notes)
		return result
	except Exception as e:
		return Debugger(e)

@blueprint.route("/References/DeleteReference", methods=['GET'])
@cross_origin()
def DeleteReference():
	try:
		SessionId = request.args.get('SessionId', '')
		ReferenceId = request.args.get('ReferenceId', '')
		result = delete_reference(SessionId, ReferenceId)
		return result
	except Exception as e:
		return Debugger(e)
