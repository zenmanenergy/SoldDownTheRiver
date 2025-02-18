from _Lib import Database
from _Lib.Debugger import Debugger
from _Lib import History
from flask import Blueprint, request
from flask_cors import CORS, cross_origin
from .SaveUser import save_user
from .DeleteUser import delete_user
from .GetUser import get_user

blueprint = Blueprint('User', __name__)

@blueprint.route("/User/SaveUser", methods=['GET'])
@cross_origin()
def SaveUser():
	try:
		user_data = request.args.to_dict()

		# Extract the UserId, FirstName, LastName, Email, Phone, Password, School, and SemesterYear from the user_data
		UserId = user_data.get('UserId', None)
		FirstName = user_data.get('FirstName', None)
		LastName = user_data.get('LastName', None)
		Email = user_data.get('Email', None)
		Phone = user_data.get('Phone', None)
		Password = user_data.get('Password', None)
		School = user_data.get('School', None)
		SemesterYear = user_data.get('SemesterYear', None)
		UserType = user_data.get('UserType', None)
		

		# Call the save_user function from SaveUser.py with the extracted data
		result = save_user(UserId, FirstName, LastName, Email, Phone, Password,School, SemesterYear,UserType)
		History.SaveHistory(user_data,"Users", "UserId", result["UserId"])

		return result
	except Exception as e:
		return Debugger(e)
	
	

@blueprint.route("/User/DeleteUser", methods=['GET'])
@cross_origin()
def DeleteUser():
	try:
		# Get the user data from the request
		user_data = request.args.to_dict()

		# Get the user ID from the request
		UserId = user_data.get('UserId')
		# Call the delete_user function from DeleteUser.py
		result = delete_user(UserId)
		History.SaveHistory(user_data,"Users", "UserId", UserId)
		return result
	except Exception as e:
		return Debugger(e)

@blueprint.route("/User/GetUser", methods=['GET'])
@cross_origin()
def GetUser():
	try:
		# Get the user data from the request
		user_data = request.args.to_dict()

		# Get the user ID from the request
		UserId = user_data.get('UserId')
		# Call the get_user function from GetUser.py
		result = get_user(UserId)
		return result
	except Exception as e:
		return Debugger(e)
