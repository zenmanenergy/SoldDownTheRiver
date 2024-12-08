
from Lib import Database
from flask import Blueprint, request, jsonify
import json
from flask_cors import CORS, cross_origin
from .ExtractShipManifest import Extract_ShipManifest
from .ExtractNotary import extract_Notary
from .OLDImportNotary import import_Notary
from .ImportNOLA import import_NOLA, Get_LastNOLA, ProcessNOLA, Fix_Locations, GPTNotes, GPTBatch, GPTSave, SaveParsedNotes,replace_string_in_json
from .ImportShipManifest import import_Manifest, Get_LastManifest, ProcessManifest

blueprint = Blueprint('Import', __name__)

@blueprint.route("/Import/ImportData", methods=['POST'])
@cross_origin()
def ImportData():
	sessionData={}
	import_data = request.get_json()
	spreadsheet_name = import_data['SpreadsheetName']
	spreadsheet_data = json.loads(import_data['SpreadsheetData'])
	SessionId="ImportData"
	if spreadsheet_name=="NOLA":
		import_NOLA(spreadsheet_data,SessionId)
	elif spreadsheet_name=="Manifest":
		import_Manifest(spreadsheet_data,SessionId)

	print("IMPORT COMPLETED")
	result = {"message": "Data imported successfully"}
	return result
	
	
@blueprint.route("/Import/GetLastNOLA", methods=['GET'])
@cross_origin()
def GetLastNOLA():
	LastNola=Get_LastNOLA()
	
	return LastNola
	

	
@blueprint.route("/Import/GetLastManifest", methods=['GET'])
@cross_origin()
def GetLastManifest():
	LastNola=Get_LastManifest()
	
	return LastNola

@blueprint.route("/Import/ProcessNola", methods=['GET'])
@cross_origin()
def Process_Nola():
	ProcessResults=ProcessNOLA()
	return ProcessResults

@blueprint.route("/Import/ProcessManifest", methods=['GET'])
@cross_origin()
def Process_Manifest():
	ProcessResults=ProcessManifest()
	return ProcessResults
	
@blueprint.route("/Import/", methods=['GET'])
@cross_origin()
def importroot():
	return "it works!"

@blueprint.route("/Import/GPTNotes", methods=['GET'])
@cross_origin()
def GPT_Notes():
	JSONNotes=GPTNotes()
	return JSONNotes

@blueprint.route("/Import/GPTBatch", methods=['GET'])
@cross_origin()
def GPT_Batch():
	JSONNotes=GPTBatch()

	# print(create_request_json("request-1", "John sold 3 slaves to Mary, a free woman of color, for $500 at the New Orleans market."))
	# print(create_request_json("request-2", "Sarah, a slave, was sold for 400 dollars in Virginia."))
	return JSONNotes
@blueprint.route("/Import/GPTSave", methods=['GET'])
@cross_origin()
def GPT_Save():
	JSONNotes=GPTSave()

	# print(create_request_json("request-1", "John sold 3 slaves to Mary, a free woman of color, for $500 at the New Orleans market."))
	# print(create_request_json("request-2", "Sarah, a slave, was sold for 400 dollars in Virginia."))
	return JSONNotes

@blueprint.route("/Import/SaveParsedNotes", methods=['GET'])
@cross_origin()
def Save_ParsedNotes():
	res=SaveParsedNotes()

	return res
@blueprint.route("/Import/replace_string_in_json", methods=['GET'])
@cross_origin()
def Save_replace_string_in_json():
	res=replace_string_in_json()

	return res

@blueprint.route("/Import/FixLocations", methods=['GET'])
@cross_origin()
def FixLocations():
	response=Fix_Locations()
	return response
	