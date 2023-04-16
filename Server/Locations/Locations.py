import uuid
from Lib import Database
from flask import Blueprint, request
from flask_cors import CORS, cross_origin

blueprint = Blueprint('Locations', __name__)

@blueprint.route("/GetLastLocation", methods=['GET', 'POST'])
@cross_origin()
def GetLastLocation():
    Cursor, Connection = Database.ConnectToDatabase()

    Query = "SELECT * FROM locations ORDER BY LocationId DESC LIMIT 1"
    Cursor.execute(Query)

    Response = {}
    Response['action'] = "select"
    Response['rowcount'] = Cursor.rowcount
    Response['data'] = Cursor.fetchone()

    Cursor.close()
    Connection.close()

    return Response


@blueprint.route("/InsertLocation", methods=['GET'])
@cross_origin()
def InsertLocation():
    City = request.args['City']
    State = request.args['State']
    Country = request.args['Country']
    Latitude = request.args['Latitude']
    Longitude = request.args['Longitude']

    LocationId = "LOC" + str(uuid.uuid4()).replace("-", "", -1)

    Cursor, Connection = Database.ConnectToDatabase()

    Query = "INSERT INTO locations (LocationId, City, State, Country, Latitude, Longitude) VALUES (%s,%s,%s,%s,%s,%s)"
    Values = (LocationId, City, State, Country, Latitude, Longitude)
    Cursor.execute(Query, Values)

    Response = {}
    Response['LocationId'] = LocationId
    Response['action'] = "insert"
    Response['rowcount'] = Cursor.rowcount

    Connection.commit()
    Cursor.close()
    Connection.close()

    return Response


@blueprint.route("/UpdateLocation", methods=['GET'])
@cross_origin()
def UpdateLocation():
    LocationId = request.args['LocationId']
    City = request.args['City']
    State = request.args['State']
    Country = request.args['Country']
    Latitude = request.args['Latitude']
    Longitude = request.args['Longitude']

    Cursor, Connection = Database.ConnectToDatabase()

    Query = "UPDATE locations SET City=%s, State=%s, Country=%s, Latitude=%s, Longitude=%s WHERE LocationId=%s"
    Values = (City, State, Country, Latitude, Longitude, LocationId)

    Cursor.execute(Query, Values)

    Response = {}
    Response['LocationId'] = LocationId
    Response['action'] = "update"
    Response['rowcount'] = Cursor.rowcount

    Connection.commit()
    Cursor.close()
    Connection.close()

    return Response


@blueprint.route("/DeleteLocation", methods=['GET'])
@cross_origin()
def DeleteLocation():
    LocationId = request.args['LocationId']
    Response = Locations.DeleteLocation(LocationId)
    return Response


def DeleteLocation(LocationId):
    Cursor, Connection = Database.ConnectToDatabase()

    Query = "DELETE FROM locations WHERE LocationId=%s"
    Values = (LocationId,)
    Cursor.execute(Query, Values)

    Response = {}
    Response['LocationId'] = LocationId
    Response['action'] = "delete"
    Response['rowcount'] = Cursor.rowcount

    Connection.commit()
    Cursor.close()
    Connection.close()

    return Response
