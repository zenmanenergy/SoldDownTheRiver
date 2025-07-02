from _Lib import Database
from flask import jsonify

def get_reference_link(LinkId, TargetType):
	try:
		sql = """
			SELECT r.ReferenceId, r.URL, r.Notes, r.dateUpdated
			FROM referencelinks rl
			JOIN reference r ON rl.ReferenceId = r.ReferenceId
			WHERE rl.LinkId = %s AND rl.TargetType = %s
		"""
		params = (LinkId, TargetType)
		result = Database.Query(sql, params)
		return jsonify(result)
	except Exception as e:
		return jsonify({'error': str(e)})
