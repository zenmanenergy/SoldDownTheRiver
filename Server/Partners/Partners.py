import uuid
from Lib import Database

from flask import Blueprint, request
from flask_cors import CORS, cross_origin

blueprint = Blueprint('Partners', __name__)

@blueprint.route("/Partners/GetLastPartner", methods=['GET', 'POST'])
@cross_origin()
def GetLastPartner():
    Cursor, Connection = Database.ConnectToDatabase()

    Query = "SELECT * FROM partners ORDER BY HumanId DESC LIMIT 1"
    Cursor.execute(Query)

    Response = {}
    Response['action'] = "select"
    Response['rowcount'] = Cursor.rowcount
    Response['data'] = Cursor.fetchone()

    Cursor.close()
    Connection.close()

    return Response

@blueprint.route("/Partners/InsertPartner", methods=['GET'])
@cross_origin()
def InsertPartner():
    HumanId = request.args['HumanId']
    PartnerHumanId = request.args['PartnerHumanId']

    PartnerId = "PAR" + str(uuid.uuid4()).replace("-", "", -1)

    Cursor, Connection = Database.ConnectToDatabase()

    Query = "INSERT INTO partners (HumanId, PartnerHumanId) VALUES (%s, %s)"
    Values = (HumanId, PartnerHumanId)
    Cursor.execute(Query, Values)

    Response = {}
    Response['PartnerId'] = PartnerId
    Response['action'] = "insert"
    Response['rowcount'] = Cursor.rowcount

    Connection.commit()
    Cursor.close()
    Connection.close()

    return Response

@blueprint.route("/Partners/UpdatePartner", methods=['GET'])
@cross_origin()
def UpdatePartner():
    PartnerId = request.args['PartnerId']
    HumanId = request.args['HumanId']
    PartnerHumanId = request.args['PartnerHumanId']

    Cursor, Connection = Database.ConnectToDatabase()

    Query = "UPDATE partners SET HumanId='%s', PartnerHumanId='%s' WHERE PartnerId='%s'"
    Values = (HumanId, PartnerHumanId, PartnerId)

    Cursor.execute(Query, Values)

    Response = {}
    Response['PartnerId'] = PartnerId
    Response['action'] = "update"
    Response['rowcount'] = Cursor.rowcount

    Connection.commit()
    Cursor.close()
    Connection.close()

    return Response

@blueprint.route("/Partners/DeletePartner", methods=['GET'])
@cross_origin()
def DeletePartner():
    PartnerId = request.args['PartnerId']

    Cursor, Connection = Database.ConnectToDatabase()

    Query = "DELETE FROM partners WHERE PartnerId=%s"
    Values = (PartnerId,)
    Cursor.execute(Query, Values)

    Response = {}
    Response['PartnerId'] = PartnerId
    Response['action'] = "delete"
    Response['rowcount'] = Cursor.rowcount

    Connection.commit()
    Cursor.close()
    Connection.close()

    return Response
