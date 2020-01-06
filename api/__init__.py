from flask import Flask
from flask_cors import CORS
from api.database import create_db

app = Flask(__name__)
CORS(app)

create_db(app)

import api.controllers.farmers
import api.controllers.products
import api.controllers.errors
import api.controllers.orders
