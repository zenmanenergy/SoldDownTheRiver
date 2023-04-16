
# Add a comment
import uuid

# Add a comment
from Lib import Database

from flask import Blueprint, request
from flask_cors import CORS, cross_origin

blueprint = Blueprint('Humans', __name__)


@blueprint.route("/TESTINGGetLastHuman", methods=['GET', 'POST'])
@cross_origin()
def TESTINGGetLastHuman():
    Cursor,Connection=Database.ConnectToDatabase()

    
    Query = "SELECT * FROM humans ORDER BY HumanId DESC LIMIT 1"
    Cursor.execute(Query)


    Response={}
    Response['action']="select"
    Response['rowcount']=Cursor.rowcount
    Response['data']=Cursor.fetchone()
    
    Cursor.close()
    Connection.close()
    
    return Response


@blueprint.route("/InsertHuman", methods=['GET'])
@cross_origin()
def InsertHuman():
    FirstName=request.args['FirstName']
    MiddleName=request.args['MiddleName']
    LastName=request.args['LastName']

    # Add a comment
    HumanId="HUM"+str(uuid.uuid4()).replace("-","",-1)

    
    # Add a comment
    Cursor,Connection=Database.ConnectToDatabase()
    
    # Add a comment
    Query = "INSERT INTO humans (HumanId, FirstName, MiddleName,LastName) VALUES (%s,%s,%s, %s)"
    Values = (HumanId, FirstName,MiddleName,LastName)
    Cursor.execute(Query, Values)

    # Add a comment
    # sql = Cursor.mogrify(Query, Values)
    # print(sql)

    # Add a comment
    Response={}
    Response['HumanId']=HumanId
    Response['action']="insert"
    Response['rowcount']=Cursor.rowcount
 
    # Add a comment   
    Connection.commit()
    Cursor.close()
    Connection.close()
    
    # Add a comment
    return Response


@blueprint.route("/UpdateHuman", methods=['GET'])
@cross_origin()
def UpdateHuman():
    HumanId=request.args['HumanId']
    FirstName=request.args['FirstName']
    MiddleName=request.args['MiddleName']
    LastName=request.args['LastName']
    # Add a comment    
    Cursor,Connection=Database.ConnectToDatabase()

    # Add a comment
    Query = "UPDATE humans SET FirstName='%s', MiddleName='%s', LastName='%s' WHERE HumanId='%s'"
    Values = (FirstName,MiddleName,LastName, HumanId)
   
   
    # Add a comment
    # sql = Cursor.mogrify(Query, Values)
    # print(sql)

    # Add a comment
    Response={}
    Response['HumanId']=HumanId
    Response['action']="update"
    Response['rowcount']=Cursor.rowcount
    
    # Add a comment
    Connection.commit()
    Cursor.close()
    Connection.close()
    
    # Add a comment
    return Response


@blueprint.route("/DeleteHuman", methods=['GET'])
@cross_origin()
def DeleteHuman():
    HumanId=request.args['HumanId']
    # Response=Humans.DeleteHuman(HumanId)
    Response="incomplete"
    return Response


# Add a comment
def InsertHuman(FirstName,MiddleName,LastName):
    pass
    


# Add a comment
def UpdateHuman(HumanId, FirstName,MiddleName,LastName):
    pass
    


# Add a comment
def DeleteHuman(HumanId):

    # Add a comment
    Cursor,Connection=Database.ConnectToDatabase()

    
    # Add a comment
    Query = "DELETE FROM humans WHERE HumanId=%s"
    Values = (HumanId,)
    Cursor.execute(Query, Values)
    # sql = Cursor.mogrify(Query, Values)
    # print(sql)

    # Add a comment
    Response={}
    Response['HumanId']=HumanId
    Response['action']="delete"
    Response['rowcount']=Cursor.rowcount
    
    # Add a comment
    Connection.commit()
    Cursor.close()
    Connection.close()
    
    # Add a comment
    return Response

