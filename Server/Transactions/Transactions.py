
# Add a comment
import uuid

# Add a comment
from Lib import Database

from flask import Blueprint, request
from flask_cors import CORS, cross_origin

blueprint = Blueprint('Transactions', __name__)

@blueprint.route("/TESTINGGetLastTransaction", methods=['GET','POST'])
@cross_origin()
def TESTINGGetLastTransaction():
    Response=TESTINGGetLastTransaction()
    return Response

@blueprint.route("/InsertTransaction", methods=['GET','POST'])
@cross_origin()
def InsertTransaction():
    TransactionDate=request.args['TransactionDate']
    FromHumanId=request.args['FromHumanId']
    ToHumanId=request.args['ToHumanId']
    TransactionType=request.args['TransactionType']
    Notes=request.args['Notes']
    Act=request.args['Act']
    Page=request.args['Page']
    NotaryHumanId=request.args['NotaryHumanId']
    Volume=request.args['Volume']
    URL=request.args['URL']
    TranscriberId=request.args['TranscriberId']
    Response=InsertTransaction(TransactionDate,FromHumanId,ToHumanId,TransactionType,Notes,Act,Page,NotaryHumanId,Volume,URL,TranscriberId)
    return Response


@blueprint.route("/UpdateTransaction", methods=['GET','POST'])
@cross_origin()
def UpdateTransaction():
    TransactionId=request.args['TransactionId']
    TransactionDate=request.args['TransactionDate']
    FromHumanId=request.args['FromHumanId']
    ToHumanId=request.args['ToHumanId']
    TransactionType=request.args['TransactionType']
    Notes=request.args['Notes']
    Act=request.args['Act']
    Page=request.args['Page']
    NotaryHumanId=request.args['NotaryHumanId']
    Volume=request.args['Volume']
    URL=request.args['URL']
    TranscriberId=request.args['TranscriberId']

    
    Response=UpdateTransaction(TransactionId, TransactionDate,FromHumanId,ToHumanId,TransactionType,Notes,Act,Page,NotaryHumanId,Volume,URL,TranscriberId)
    return Response


@blueprint.route("/DeleteTransaction", methods=['GET','POST'])
@cross_origin()
def DeleteTransaction():
    TransactionId=request.args['TransactionId']
    Response=DeleteTransaction(TransactionId)
    return Response


def TESTINGGetLastTransaction():
    Cursor,Connection=Database.ConnectToDatabase()

    
    Query = "SELECT * FROM transactions ORDER BY TransactionId DESC LIMIT 1"
    Cursor.execute(Query)


    Response={}
    Response['action']="select"
    Response['rowcount']=Cursor.rowcount
    Response['data']=Cursor.fetchone()
    
    Cursor.close()
    Connection.close()
    return Response

# Add a comment
def InsertTransaction(TransactionDate,FromHumanId,ToHumanId,TransactionType,Notes,Act,Page,NotaryHumanId,Volume,URL,TranscriberId):

    # Add a comment
    TransactionId="TRA"+str(uuid.uuid4()).replace("-","",-1)


    # Add a comment
    Cursor,Connection=Database.ConnectToDatabase()

    # Add a comment
    Query = """
    INSERT INTO transactions (TransactionId, TransactionDate, FromHumanId, ToHumanId, TransactionType, Notes, Act, Page, NotaryHumanId, Volume, URL,TranscriberId)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    # Add a comment
    Values = (TransactionId, TransactionDate, FromHumanId, ToHumanId, TransactionType, Notes, Act, Page, NotaryHumanId, Volume, URL,TranscriberId)

    # Add a comment
    Cursor.execute(Query, Values)
    Connection.commit()

    # Add a comment
    # sql = Cursor.mogrify(Query, Values)
    # print(sql)

    # Add a comment
    Response={}
    Response['TransactionId']=TransactionId
    Response['action']="insert"
    Response['rowcount']=Cursor.rowcount
    
    # Add a comment
    Cursor.close()
    Connection.close()
    
    # Add a comment
    return Response


# Add a comment
def UpdateTransaction(TransactionId, TransactionDate,FromHumanId,ToHumanId,TransactionType,Notes,act,Page,NotaryHumanId,Volume,URL,TranscriberId):
    
    # Add a comment
    Cursor,Connection=Database.ConnectToDatabase()

    # Add a comment
    Query = """
        UPDATE transactions
        SET TransactionDate=%s, 
            FromHumanId=%s, 
            ToHumanId=%s, 
            TransactionType=%s, 
            Notes=%s, 
            act=%s, 
            Page=%s, 
            NotaryHumanId=%s, 
            Volume=%s, 
            URL=%s
        WHERE TransactionId=%s;

    """

    # Add a comment
    Values = ( TransactionDate, FromHumanId, ToHumanId, TransactionType, Notes, act, Page, NotaryHumanId, Volume, URL,TranscriberId)

    # Add a comment
    Cursor.execute(Query, Values)
    Connection.commit()

    # Add a comment
    # sql = Cursor.mogrify(Query, Values)
    # print(sql)

    # Add a comment
    Response={}
    Response['TransactionId']=TransactionId
    Response['action']="update"
    Response['rowcount']=Cursor.rowcount
    
    # Add a comment
    Cursor.close()
    Connection.close()
    
    # Add a comment
    return Response


# Add a comment
def DeleteTransaction(TransactionId):

    # Add a comment
    Cursor,Connection=Database.ConnectToDatabase()

    
    # Add a comment
    Query = "DELETE FROM transactions WHERE TransactionId=%s"
    Values = (TransactionId,)
    
    # Add a comment
    Cursor.execute(Query, Values)
    Connection.commit()

    
    # Add a comment
    # sql = Cursor.mogrify(Query, Values)
    # print(sql)

    # Add a comment
    Response={}
    Response['TransactionId']=TransactionId
    Response['action']="delete"
    Response['rowcount']=Cursor.rowcount
    
    
    # Add a comment
    Cursor.close()
    Connection.close()
    
    # Add a comment
    return Response