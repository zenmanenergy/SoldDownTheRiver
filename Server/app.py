
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
from Partners import Partners
from Transactions import Transactions
from Users import Users


app = Flask(__name__)

app.register_blueprint(Businesses.blueprint)
app.register_blueprint(Business.blueprint)
app.register_blueprint(Humans.blueprint)
app.register_blueprint(Human.blueprint)
app.register_blueprint(Locations.blueprint)
app.register_blueprint(Location.blueprint)

@app.route("/")
@cross_origin()
def index():
    return "404"
