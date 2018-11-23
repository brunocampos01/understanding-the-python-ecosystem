from flask_pymongo import PyMongo
from flask_api import FlaskAPI

# contrução de uma instancia da class Flask
app = FlaskAPI(__name__)

# MongoDB
app.config['MONGO_DBNAME'] = 'chaordicdb'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/chaordicdb'
mongo = PyMongo(app)