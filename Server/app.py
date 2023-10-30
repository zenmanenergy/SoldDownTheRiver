
# save this as app.py
from flask import Flask, request
from flask_cors import CORS, cross_origin
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
import json

from Businesses import Businesses
from Business import Business
from Humans import Humans
from Human import Human
from Locations import Locations
from Location import Location
from Notary import Notary
from Transactions import Transactions
from Users import Users
from User import User
from Roles import Roles
from Role import Role
from Transactions import Transactions
from Transaction import Transaction
from Login import Login
from Search import Search
from Ships import Ships
from Ship import Ship
from Voyages import Voyages
from Voyage import Voyage
from Voyage.EnslavedPerson import EnslavedPerson
from Import import Import
from Human.ShipAgent import ShipAgent
from Human.ShipCaptain import ShipCaptain



app.register_blueprint(Businesses.blueprint)
app.register_blueprint(Business.blueprint)
app.register_blueprint(Humans.blueprint)
app.register_blueprint(Human.blueprint)
app.register_blueprint(Locations.blueprint)
app.register_blueprint(Location.blueprint)
app.register_blueprint(Users.blueprint)
app.register_blueprint(User.blueprint)
app.register_blueprint(Roles.blueprint)
app.register_blueprint(Role.blueprint)
app.register_blueprint(Transactions.blueprint)
app.register_blueprint(Transaction.blueprint)
app.register_blueprint(Login.blueprint)
app.register_blueprint(Search.blueprint)
app.register_blueprint(Ships.blueprint)
app.register_blueprint(Ship.blueprint)
app.register_blueprint(Voyages.blueprint)
app.register_blueprint(Voyage.blueprint)
app.register_blueprint(Import.blueprint)
app.register_blueprint(ShipAgent.blueprint)
app.register_blueprint(ShipCaptain.blueprint)
app.register_blueprint(EnslavedPerson.blueprint)


@app.route("/")
@cross_origin()
def index():
    return "it works"
