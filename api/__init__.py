from flask import Flask
from api.database import create_db

app = Flask(__name__)

create_db(app)

import api.controllers.farmers
import api.controllers.products
import api.controllers.errors
import api.controllers.orders
