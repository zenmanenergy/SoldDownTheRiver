import uuid
from Lib import History

from Lib import Database
from Lib.Debugger import Debugger
from flask import Blueprint, request
from flask_cors import CORS, cross_origin

blueprint = Blueprint('Notary', __name__)


@blueprint.route("/Notary/TESTINGGetLastNotary", methods=['GET', 'POST'])
@cross_origin()
def TESTINGGetLastNotary():
	try:
		Cursor, Connection = Database.ConnectToDatabase()

		Query = "SELECT * FROM notary ORDER BY HumanId DESC LIMIT 1"
		Cursor.execute(Query)

		Response = {}
		Response['action'] = "select"
		Response['rowcount'] = Cursor.rowcount
		Response['data'] = Cursor.fetchall()

		Cursor.close()
		Connection.close()

		return Response
	except Exception as e:
		return Debugger(e)


@blueprint.route("/InsertNotary", methods=['GET'])
@cross_origin()
def InsertNotary():
	try:
		HumanId = request.args['HumanId']
		Language = request.args['Language']
		StartYear = request.args['StartYear']
		EndYear = request.args['EndYear']


		Cursor, Connection = Database.ConnectToDatabase()

		Query = "INSERT INTO notary (HumanId, Language, StartYear, EndYear) VALUES (%s,%s,%s,%s)"
		Values = (HumanId, Language, StartYear, EndYear)
		Cursor.execute(Query, Values)

		Response = {}
		Response['HumanId'] = HumanId
		Response['action'] = "insert"
		Response['rowcount'] = Cursor.rowcount

		Connection.commit()
		Cursor.close()
		Connection.close()

		return Response
	except Exception as e:
		return Debugger(e)


@blueprint.route("/UpdateNotary", methods=['GET'])
@cross_origin()
def UpdateNotary():
	try:
		HumanId = request.args['HumanId']
		Language = request.args['Language']
		StartYear = request.args['StartYear']
		EndYear = request.args['EndYear']

		Cursor, Connection = Database.ConnectToDatabase()

		Query = "UPDATE notary SET Language=%s, StartYear=%s, EndYear=%s WHERE HumanId=%s"
		Values = (Language, StartYear, EndYear, HumanId)

		Cursor.execute(Query, Values)

		Response = {}
		Response['HumanId'] = HumanId
		Response['action'] = "update"
		Response['rowcount'] = Cursor.rowcount

		Connection.commit()
		Cursor.close()
		Connection.close()

		return Response
	except Exception as e:
		return Debugger(e)


@blueprint.route("/DeleteNotary", methods=['GET'])
@cross_origin()
def DeleteNotary():
	try:
		HumanId = request.args['HumanId']

		Cursor, Connection = Database.ConnectToDatabase()

		Query = "DELETE FROM notary WHERE HumanId=%s"
		Values = (HumanId,)

		Cursor.execute(Query, Values)

		Response = {}
		Response['HumanId'] = HumanId
		Response['action'] = "delete"
		Response['rowcount'] = Cursor.rowcount

		Connection.commit()
		Cursor.close()
		Connection.close()

		return Response
	except Exception as e:
		return Debugger(e)
