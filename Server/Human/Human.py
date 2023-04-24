from Lib import Database
from Lib import History
from flask import Blueprint, request
from flask_cors import CORS, cross_origin
from .SaveHuman import save_human
from .DeleteHuman import delete_human
from .GetHuman import get_human
from .GetAKANames import get_aka
from .SaveAKANames import save_aka
from .DeleteAKAName import delete_aka
from .SavePartner import save_partner
from .DeletePartner import delete_partner
from .GetPartners import get_partners
from .GetPossiblePartners import get_possible_partners
from .GetRoles import get_roles

blueprint = Blueprint('Human', __name__)

@blueprint.route("/Human/SaveHuman", methods=['GET'])
@cross_origin()
def SaveHuman():
    human_data = request.args.to_dict()

    # Extract the HumanId and HumanName from the human_data
    HumanId = human_data.get('HumanId', None)
    FirstName = human_data.get('FirstName', None)
    MiddleName = human_data.get('MiddleName', None)
    LastName = human_data.get('LastName', None)
    StartYear = human_data.get('StartYear', None)
    EndYear = human_data.get('EndYear', None)
    Notes = human_data.get('Notes', None)
    RoleId = human_data.get('RoleId', None)

    # Call the save_human function from SaveHuman.py with the extracted data
    result = save_human(HumanId, FirstName, MiddleName, LastName, StartYear, EndYear, Notes,RoleId )
    History.SaveHistory(human_data,"Humans", "HumanId", result["HumanId"])


    return result

@blueprint.route("/Human/DeleteHuman", methods=['GET'])
@cross_origin()
def DeleteHuman():
    # Get the human data from the request
    human_data = request.args.to_dict()

    # Get the human ID from the request
    HumanId = human_data.get('HumanId')
    # Call the delete_human function from DeleteHuman.py
    result = delete_human(HumanId)
    History.SaveHistory(human_data,"Humans", "HumanId")
    return result

@blueprint.route("/Human/GetHuman", methods=['GET'])
@cross_origin()
def GetHuman():
    # Get the human data from the request
    human_data = request.args.to_dict()

    # Get the human ID from the request
    HumanId = human_data.get('HumanId')
    # Call the get_human function from GetHuman.py
    result = get_human(HumanId)
    return result


@blueprint.route("/Human/GetAkaNames", methods=['GET'])
@cross_origin()
def GetAkaNames():
    # Get the human data from the request
    human_data = request.args.to_dict()

    # Get the human ID from the request
    HumanId = human_data.get('HumanId')
    # Call the get_human function from GetHuman.py
    result = get_aka(HumanId)
    return result


@blueprint.route("/Human/SaveHumanAKA", methods=['GET'])
@cross_origin()
def SaveHumanAKA():
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


@blueprint.route("/Human/DeleteAKAName", methods=['GET'])
@cross_origin()
def DeleteAKAName():
    # Get the human data from the request
    human_data = request.args.to_dict()

    # Get the human ID from the request
    AKAHumanId = human_data.get('AKAHumanId', None)
    
    # Call the get_human function from GetHuman.py
    result = delete_aka(AKAHumanId)
    print(result)
    History.SaveHistory(human_data,"humansaka", "AKAHumanId", result["AKAHumanId"])
    return result



@blueprint.route("/Human/SavePartner", methods=['GET'])
@cross_origin()
def SavePartner():
    # Get the human data from the request
    human_data = request.args.to_dict()

    # Get the human ID from the request
    HumanId = human_data.get('HumanId', None)
    PartnerHumanId = human_data.get('PartnerHumanId', None)
    
    # Call the get_human function from GetHuman.py
    result = save_partner(HumanId, PartnerHumanId)
    History.SaveHistory(human_data,"Partners", "PartnerHumanId", PartnerHumanId)
    return result


@blueprint.route("/Human/GetPartners", methods=['GET'])
@cross_origin()
def getPartners():
    # Get the human data from the request
    human_data = request.args.to_dict()

    # Get the human ID from the request
    HumanId = human_data.get('HumanId', None)
    
    # Call the get_human function from GetHuman.py
    result = get_partners(HumanId)
    return result


@blueprint.route("/Human/GetPossiblePartners", methods=['GET'])
@cross_origin()
def GetPossiblePartners():
    # Get the human data from the request
    human_data = request.args.to_dict()

    # Get the human ID from the request
    HumanId = human_data.get('HumanId', None)
    
    # Call the get_human function from GetHuman.py
    result = get_possible_partners(HumanId)
    return result

@blueprint.route("/Human/DeletePartner", methods=['GET'])
@cross_origin()
def DeletePartner():
    # Get the human data from the request
    human_data = request.args.to_dict()

    # Get the human ID from the request
    HumanId = human_data.get('HumanId', None)
    PartnerHumanId = human_data.get('PartnerHumanId', None)
    
    # Call the get_human function from GetHuman.py
    result = delete_partner(HumanId, PartnerHumanId)
    History.SaveHistory(human_data,"Partners", "PartnerHumanId", PartnerHumanId)
    return result

@blueprint.route("/Human/GetRoles", methods=['GET'])
@cross_origin()
def GetRoles():
    # Get the role data from the request
    role_data = request.args.to_dict()

    # Call the get_role function from GetRoles.py
    result = get_roles()

    return result