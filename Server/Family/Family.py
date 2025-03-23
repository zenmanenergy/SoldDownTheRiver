from _Lib import Database
from _Lib.Debugger import Debugger
from _Lib import History
from flask import Blueprint, request
from flask_cors import CORS, cross_origin
from .GetFamily import get_family
from .AddFamilyMember import add_family_member
from .RemoveFamilyMember import remove_family_member   # new import

blueprint = Blueprint('Family', __name__)

@blueprint.route("/Family/GetFamily", methods=['GET'])
@cross_origin()
def GetFamily():
	try:
		human_data = request.args.to_dict()

		# Extract the HumanId and HumanName from the human_data
		HumanId = human_data.get('HumanId', None)

		# Call the save_human function from SaveHuman.py with the extracted data
		result = get_family(HumanId)
		
		return result
	except Exception as e:
		return Debugger(e)


@blueprint.route("/Family/AddFamilyMember", methods=['GET'])  # Updated route name
@cross_origin()
def AddFamilyMember():  # Updated function name
	try:
		data = request.args.to_dict()  # Changed to use query parameters
		SessionId = data.get('SessionId')
		HumanId = data.get('HumanId')
		RelatedHumanId = data.get('RelatedHumanId')
		RelationshipType = data.get('RelationshipType')

		result = add_family_member(HumanId, RelatedHumanId, RelationshipType)
		return result
	except Exception as e:
		return Debugger(e)


@blueprint.route("/Family/RemoveFamilyMember", methods=['GET'])
@cross_origin()
def RemoveFamilyMember():
	try:
		data = request.args.to_dict()
		SessionId = data.get('SessionId')
		HumanId = data.get('HumanId')
		RelatedHumanId = data.get('RelatedHumanId')
		result = remove_family_member(HumanId, RelatedHumanId)
		return result
	except Exception as e:
		return Debugger(e)
