from _Lib import Database
from _Lib.Debugger import Debugger
from flask import Blueprint, request
from flask_cors import CORS, cross_origin
from .GetHumans import get_humans
from .SetTimelines import set_timelines
from .GetRacialDescriptors import get_racial_descriptors
from .ImportOwners import import_owners
from .ImportOwners2 import import_owner2
from .ImportShippingAgents import import_shippingagents
from .ImportCollectorAgents import import_CollectorAgents
from .ImportEnslaved import import_enslaved
from .import_voyagehumans import import_voyagehumans
from .ImportEnslaved import resolve_duplicate_enslaved_humanid

blueprint = Blueprint('Humans', __name__ )

@blueprint.route("/Humans/GetHumans", methods=['GET'])
@cross_origin()
def GetHumans():
	try:
		# Get the human data from the request
		human_data = request.args.to_dict()
		Query = human_data.get('Query', None)
		LastFetchTime = human_data.get('LastFetchTime', None)  # Get LastFetchTime from the request
		print("LastFetchTime",LastFetchTime)
		if LastFetchTime == 'null':  # Handle 'null' string explicitly
			LastFetchTime = None

		# Call the get_humans function with Query and LastFetchTime
		result = get_humans(Query, LastFetchTime)
		return result
	except Exception as e:
		return Debugger(e)

@blueprint.route("/Humans/SetTimelines", methods=['GET'])
@cross_origin()
def SetTimelines():
	try:
		# Call the set_timelines function from SetTimelines.py
		result = set_timelines()
		return result
	except Exception as e:
		return Debugger(e)

@blueprint.route("/Humans/GetRacialDescriptors", methods=['GET'])
@cross_origin()
def GetRacialDescriptors():
	try:
		result = get_racial_descriptors()
		return result
	except Exception as e:
		return Debugger(e)

@blueprint.route("/Humans/importOwners", methods=['GET'])
@cross_origin()
def importowners():
	try:
		result = import_owners()
		return result
	except Exception as e:
		return Debugger(e)

@blueprint.route("/Humans/importOwners2", methods=['GET'])
@cross_origin()
def importowners2():
	try:
		result = import_owner2()
		return result
	except Exception as e:
		return Debugger(e)


@blueprint.route("/Humans/importShippingAgents", methods=['GET'])
@cross_origin()
def importshippingagents():
	try:
		result = import_shippingagents()
		return result
	except Exception as e:
		return Debugger(e)


@blueprint.route("/Humans/importCollectorAgents", methods=['GET'])
@cross_origin()
def importCollectorAgents():
	try:
		result = import_CollectorAgents()
		return result
	except Exception as e:
		return Debugger(e)

@blueprint.route("/Humans/importEnslaved", methods=['GET'])
@cross_origin()
def importenslaved():
	try:
		result = import_enslaved()
		return result
	except Exception as e:
		return Debugger(e)
	

@blueprint.route("/Humans/import_voyagehumans", methods=['GET'])
@cross_origin()
def importvoyagehumans():
	try:
		result = import_voyagehumans()
		return result
	except Exception as e:
		return Debugger(e)
	


@blueprint.route("/Humans/resolve_duplicate_enslaved_humanid", methods=['GET'])
@cross_origin()
def resolve_duplicate_enslaved_human():
	try:
		result = resolve_duplicate_enslaved_humanid()
		return result
	except Exception as e:
		return Debugger(e)
	
