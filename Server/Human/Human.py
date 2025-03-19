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
from .GetHumanLocations import get_humanlocations
from .GetHumanRoles import get_humanRoles
from Role.SaveHumanRole import save_HumanRole
from .GetHumanTransactions import get_human_transactions
from .GetHumanFirstParty import get_human_first_party
from .GetHumanSecondParty import get_human_second_party
from .GetNotaryTransactions import get_notary_transactions
from .GetEnslavedTransactions import get_enslaved_transactions
from .GetCaptains import get_captains



blueprint = Blueprint('Human', __name__)

@blueprint.route("/Human/SaveHuman", methods=['GET'])
@cross_origin()
def SaveHuman():
	try:
		human_data = request.args.to_dict()

		# Extract the HumanId and HumanName from the human_data
		HumanId = human_data.get('HumanId', None)
		FirstName = human_data.get('FirstName', None)
		MiddleName = human_data.get('MiddleName', None)
		LastName = human_data.get('LastName', None)
		Notes = human_data.get('Notes', None)
		RoleId = human_data.get('RoleId', None)

		# Call the save_human function from SaveHuman.py with the extracted data
		result = save_human(HumanId, FirstName, MiddleName, LastName, Notes )
		HumanId=result['HumanId']
		History.SaveHistory(human_data,"humans", "HumanId", result["HumanId"])

		print("RoleId",RoleId)
		if RoleId:
			save_HumanRole(HumanId,RoleId)

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
		History.SaveHistory(human_data,"humans", "HumanId", HumanId)

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
		History.SaveHistory(human_data,"humansaka", "AKAHumanId", result["AKAHumanId"])
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
		History.SaveHistory(human_data,"humansaka", "AKAHumanId", result["AKAHumanId"])
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
		History.SaveHistory(human_data,"families", "FamilyHumanId", FamilyHumanId)
		History.SaveHistory(human_data,"families", "HumanId", HumanId)
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
		History.SaveHistory(human_data,"families", "FamilyHumanId", FamilyHumanId)
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


		HistoryArray=[{"Table":"humans","KeyName":"HumanId", "KeyValue" : business_data.get('HumanId')},{"Table":"families", "KeyName":"HumanId", "KeyValue": business_data.get('HumanId')},{"Table":"humansaka", "KeyName":"HumanId", "KeyValue": business_data.get('HumanId')}]
		result=History.LastModifiedArray(HistoryArray)
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

		

@blueprint.route("/Human/GetHumanLocations", methods=['GET'])
@cross_origin()
def GetHumanLocations():
	try:
		# Get the role data from the request
		human_data = request.args.to_dict()

		HumanId = human_data.get('HumanId', None)
		# Call the get_role function from GetRoles.py
		result = get_humanlocations(HumanId)

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

@blueprint.route("/Human/GetHumanFirstParty", methods=['GET'])
@cross_origin()
def GetHumanFirstParty():
	try:
		# Get the human data from the request
		human_data = request.args.to_dict()

		# Get the human ID from the request
		HumanId = human_data.get('HumanId', None)
		# Call the get_human_first_party function from GetHumanFirstParty.py
		result = get_human_first_party(HumanId)
		return result
	except Exception as e:
		return Debugger(e)

@blueprint.route("/Human/GetHumanSecondParty", methods=['GET'])
@cross_origin()
def GetHumanSecondParty():
	try:
		# Get the human data from the request
		human_data = request.args.to_dict()

		# Get the human ID from the request
		HumanId = human_data.get('HumanId', None)
		# Call the get_human_second_party function from GetHumanSecondParty.py
		result = get_human_second_party(HumanId)
		return result
	except Exception as e:
		return Debugger(e)

@blueprint.route("/Human/GetNotaryTransactions", methods=['GET'])
@cross_origin()
def GetNotaryTransactions():
	try:
		# Get the human data from the request
		human_data = request.args.to_dict()

		# Get the human ID from the request
		HumanId = human_data.get('HumanId', None)
		# Call the get_notary_transactions function from GetNotaryTransactions.py
		result = get_notary_transactions(HumanId)
		return result
	except Exception as e:
		return Debugger(e)

@blueprint.route("/Human/GetEnslavedTransactions", methods=['GET'])
@cross_origin()
def GetEnslavedTransactions():
	try:
		# Get the human data from the request
		human_data = request.args.to_dict()

		# Get the human ID from the request
		HumanId = human_data.get('HumanId', None)
		# Call the get_enslaved_transactions function from GetEnslavedTransactions.py
		result = get_enslaved_transactions(HumanId)
		return result
	except Exception as e:
		return Debugger(e)

@blueprint.route("/Human/GetCaptains", methods=['GET'])
@cross_origin()
def GetCaptains():
	try:
		# Get the human data from the request
		human_data = request.args.to_dict()

		# Get the human ID from the request
		HumanId = human_data.get('HumanId', None)
		# Call the get_captains function from GetCaptains.py
		result = get_captains(HumanId)
		return result
	except Exception as e:
		return Debugger(e)