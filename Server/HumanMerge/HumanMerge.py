from _Lib import Database
from _Lib.Debugger import Debugger
from _Lib import History
from flask import Blueprint, request, jsonify
from flask_cors import CORS, cross_origin
from .SaveMergeHumans import save_mergehumans

blueprint = Blueprint('MergeHumans', __name__)

@blueprint.route("/HumanMerge/Save", methods=['GET'])
@cross_origin()
def Save():
	try:
		human_data = request.args.to_dict()

		# Extract the HumanId and MergeHumanId from the human_data
		HumanId = human_data.get('HumanId', None)
		MergeHumanId = human_data.get('MergeHumanId', None)

		# Call the save_mergehumans function with the extracted data
		result = save_mergehumans(HumanId, MergeHumanId)
		
		return jsonify(result)
	except Exception as e:
		return jsonify(Debugger(e))