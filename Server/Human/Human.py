from _Lib import Database
from _Lib.Debugger import Debugger
from _Lib import History
from flask import Blueprint, request
from flask_cors import CORS, cross_origin
from .SaveHuman import save_human
from .DeleteHuman import delete_human
from .GetHuman import get_human
from .GetAKANames import get_aka
from .SaveAKANames import save_aka
from .DeleteAKAName import delete_aka
from .SaveFamily import save_Family
from .DeleteFamily import delete_Family
from .GetFamilies import get_Families
from .GetPossibleFamilies import get_possible_Families
from .GetRoles import get_roles
from .GetHumanRoles import get_humanRoles
from Role.SaveHumanRole import save_HumanRole
from .GetHumanTransactions import get_human_transactions
from .GetHumanVoyages import get_human_voyages
from .GetTimelines import get_timelines
from .SaveTimeline import save_timeline  # new import for saving timeline
from .DeleteTimeline import delete_timeline  # new import for deleting timeline

blueprint = Blueprint('Human', __name__)

@blueprint.route("/Human/SaveHuman", methods=['GET'])
@cross_origin()
def SaveHuman():
	try:
		human_data = request.args.to_dict()

		# Extract the fields from the request
		HumanId = human_data.get('HumanId', None)
		FirstName = human_data.get('FirstName', None)
		MiddleName = human_data.get('MiddleName', None)
		LastName = human_data.get('LastName', None)
		BirthDate = human_data.get('BirthDate', None)
		BirthDateAccuracy = human_data.get('BirthDateAccuracy', None)
		RacialDescriptor = human_data.get('RacialDescriptor', None)
		Sex = human_data.get('Sex', None)
		Height_cm = human_data.get('Height_cm', None)
		Notes = human_data.get('Notes', None)
		age_string = human_data.get('age_string', None)
		BirthPlace = human_data.get('BirthPlace', None)
		originCity = human_data.get('originCity', None)
		physical_features = human_data.get('physical_features', None)
		profession = human_data.get('profession', None)
		mergedHumanId = human_data.get('mergedHumanId', None)
		spouseHumanId = human_data.get('spouseHumanId', None)

		# Call the save_human function with the extracted data
		result = save_human(
			HumanId, FirstName, MiddleName, LastName, BirthDate, BirthDateAccuracy,
			RacialDescriptor, Sex, Height_cm, Notes, age_string, BirthPlace,
			originCity, physical_features, profession, mergedHumanId, spouseHumanId
		)
		HumanId = result['HumanId']
		History.SaveHistory(human_data, "humans", "HumanId", result["HumanId"])
		
		# New update: if TransactionId and RoleId are provided, then insert into transactionhumans.
		# If RoleId is missing, use the "Role" parameter instead.
		TransactionId = human_data.get('TransactionId', None)
		RoleId = human_data.get('RoleId', None)
		if not RoleId:
			RoleId = human_data.get('Role', None)
		if TransactionId and RoleId:
			cursor2, connection2 = Database.ConnectToDatabase()
			query2 = """
				INSERT INTO transactionhumans (TransactionId, HumanId, RoleId)
				VALUES (%s, %s, %s)
				ON DUPLICATE KEY UPDATE RoleId = VALUES(RoleId)
			"""
			cursor2.execute(query2, (TransactionId, HumanId, RoleId))
			connection2.commit()

		return result
	except Exception as e:
		return Debugger(e)

@blueprint.route("/Human/DeleteHuman", methods=['GET'])
@cross_origin()
def DeleteHuman():
	try:
		# Get the human data from the request
		human_data = request.args.to_dict()

		# Get the human ID from the request
		HumanId = human_data.get('HumanId')
		# Call the delete_human function from DeleteHuman.py
		result = delete_human(HumanId)
		History.SaveHistory(human_data, "humans", "HumanId", HumanId)

		return result
	except Exception as e:
		return Debugger(e)

@blueprint.route("/Human/GetHuman", methods=['GET'])
@cross_origin()
def GetHuman():
	try:
		# Get the human data from the request
		human_data = request.args.to_dict()

		# Get the human ID from the request
		HumanId = human_data.get('HumanId')
		# Call the get_human function from GetHuman.py
		result = get_human(HumanId)
		return result
	except Exception as e:
		return Debugger(e)

@blueprint.route("/Human/GetAkaNames", methods=['GET'])
@cross_origin()
def GetAkaNames():
	try:
		# Get the human data from the request
		human_data = request.args.to_dict()

		# Get the human ID from the request
		HumanId = human_data.get('HumanId')
		# Call the get_human function from GetHuman.py
		result = get_aka(HumanId)
		return result
	except Exception as e:
		return Debugger(e)

@blueprint.route("/Human/SaveHumanAKA", methods=['GET'])
@cross_origin()
def SaveHumanAKA():
	try:
		# Get the human data from the request
		human_data = request.args.to_dict()

		# Get the human ID from the request
		AKAHumanId = human_data.get('AKAHumanId', None)
		HumanId = human_data.get('HumanId', None)
		AKAFirstName = human_data.get('AKAFirstName', None)
		AKAMiddleName = human_data.get('AKAMiddleName', None)
		AKALastName = human_data.get('AKALastName', None)
		
		# Call the get_human function from GetHuman.py
		result = save_aka(AKAHumanId, HumanId, AKAFirstName, AKAMiddleName, AKALastName)
		History.SaveHistory(human_data, "humansaka", "AKAHumanId", result["AKAHumanId"])
		return result
	except Exception as e:
		return Debugger(e)

@blueprint.route("/Human/DeleteAKAName", methods=['GET'])
@cross_origin()
def DeleteAKAName():
	try:
		# Get the human data from the request
		human_data = request.args.to_dict()

		# Get the human ID from the request
		AKAHumanId = human_data.get('AKAHumanId', None)
		
		# Call the get_human function from GetHuman.py
		result = delete_aka(AKAHumanId)
		print(result)
		History.SaveHistory(human_data, "humansaka", "AKAHumanId", result["AKAHumanId"])
		return result
	except Exception as e:
		return Debugger(e)

@blueprint.route("/Human/SaveFamily", methods=['GET'])
@cross_origin()
def SaveFamily():
	try:
		# Get the human data from the request
		human_data = request.args.to_dict()

		print(human_data)
		# Get the human ID from the request
		HumanId = human_data.get('HumanId', None)
		FamilyHumanId = human_data.get('FamilyHumanId', None)
		Relationship = human_data.get('Relationship', None)
		
		# Call the get_human function from GetHuman.py
		result = save_Family(HumanId, FamilyHumanId, Relationship)
		History.SaveHistory(human_data, "families", "FamilyHumanId", FamilyHumanId)
		History.SaveHistory(human_data, "families", "HumanId", HumanId)
		return result
	except Exception as e:
		return Debugger(e)

@blueprint.route("/Human/GetFamilies", methods=['GET'])
@cross_origin()
def getFamilies():
	try:
		# Get the human data from the request
		human_data = request.args.to_dict()

		# Get the human ID from the request
		HumanId = human_data.get('HumanId', None)
		
		# # Call the get_human function from GetHuman.py
		result = get_Families(HumanId)
		return result
	except Exception as e:
		return Debugger(e)

@blueprint.route("/Human/GetPossibleFamilies", methods=['GET'])
@cross_origin()
def GetPossibleFamilies():
	try:
		# Get the human data from the request
		human_data = request.args.to_dict()

		# Get the human ID from the request
		HumanId = human_data.get('HumanId', None)
		
		# Call the get_human function from GetHuman.py
		result = get_possible_Families(HumanId)
		return result
	except Exception as e:
		return Debugger(e)

@blueprint.route("/Human/DeleteFamily", methods=['GET'])
@cross_origin()
def DeleteFamily():
	try:
		# Get the human data from the request
		human_data = request.args.to_dict()

		# Get the human ID from the request
		HumanId = human_data.get('HumanId', None)
		FamilyHumanId = human_data.get('FamilyHumanId', None)
		
		# Call the get_human function from GetHuman.py
		result = delete_Family(HumanId, FamilyHumanId)
		History.SaveHistory(human_data, "families", "FamilyHumanId", FamilyHumanId)
		return result
	except Exception as e:
		return Debugger(e)

@blueprint.route("/Human/GetRoles", methods=['GET'])
@cross_origin()
def GetRoles():
	try:
		# Get the role data from the request
		role_data = request.args.to_dict()

		# Call the get_role function from GetRoles.py
		result = get_roles()

		return result
	except Exception as e:
		return Debugger(e)

@blueprint.route("/Human/LastModified", methods=['GET'])
@cross_origin()
def LastModified():
	try:
		# Get the business data from the request
		business_data = request.args.to_dict()

		HistoryArray = [{"Table": "humans", "KeyName": "HumanId", "KeyValue": business_data.get('HumanId')}, {"Table": "families", "KeyName": "HumanId", "KeyValue": business_data.get('HumanId')}, {"Table": "humansaka", "KeyName": "HumanId", "KeyValue": business_data.get('HumanId')}]
		result = History.LastModifiedArray(HistoryArray)
		return result
	except Exception as e:
		return Debugger(e)

@blueprint.route("/Human/GetBusinesses", methods=['GET'])
@cross_origin()
def GetBusinesses():
	try:
		# Get the role data from the request
		role_data = request.args.to_dict()

		# Call the get_role function from GetRoles.py
		result = get_roles()

		return result
	except Exception as e:
		return Debugger(e)

@blueprint.route("/Human/GetHumanRoles", methods=['GET'])
@cross_origin()
def GetHumanRoles():
	try:
		# Get the role data from the request
		human_data = request.args.to_dict()

		HumanId = human_data.get('HumanId', None)
		# Call the get_role function from GetRoles.py
		result = get_humanRoles(HumanId)

		return result
	except Exception as e:
		return Debugger(e)

@blueprint.route("/Human/GetHumanTransactions", methods=['GET'])
@cross_origin()
def GetHumanTransactions():
	try:
		# Get the human data from the request
		human_data = request.args.to_dict()

		# Get the human ID from the request
		HumanId = human_data.get('HumanId', None)
		# Call the get_human_transactions function from GetHumanTransactions.py
		result = get_human_transactions(HumanId)
		return result
	except Exception as e:
		return Debugger(e)


@blueprint.route("/Human/GetVoyages", methods=['GET'])
@cross_origin()
def GetVoyages():
	try:
		# Get the human data from the request
		human_data = request.args.to_dict()

		# Get the human ID from the request
		HumanId = human_data.get('HumanId', None)
		# Call the get_human_voyages function
		result = get_human_voyages(HumanId)
		return result
	except Exception as e:
		return Debugger(e)

@blueprint.route("/Human/GetTimelines", methods=['GET'])
@cross_origin()
def GetTimelines():
	try:
		# Get the human data from the request
		human_data = request.args.to_dict()

		# Get the human ID from the request
		HumanId = human_data.get('HumanId', None)
		# Call the get_timelines function from GetTimelines.py
		result = get_timelines(HumanId)
		return result
	except Exception as e:
		return Debugger(e)

@blueprint.route("/Human/SaveTimeline", methods=['GET'])
@cross_origin()
def SaveTimeline():
	try:
		# Get timeline data from the request
		timeline_data = request.args.to_dict()
		# Call the save_timeline function with the timeline data (adjust parameters as needed)
		result = save_timeline(timeline_data)
		return result
	except Exception as e:
		return Debugger(e)

@blueprint.route("/Human/DeleteTimeline", methods=['GET'])
@cross_origin()
def DeleteTimeline():
	try:
		# Get timeline data from the request
		timeline_data = request.args.to_dict()
		# Call the delete_timeline function with the timeline data
		result = delete_timeline(timeline_data)
		return result
	except Exception as e:
		return Debugger(e)

