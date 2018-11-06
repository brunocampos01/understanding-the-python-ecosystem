# init indica que cada diretório é um módulo
# arquivo somente com a declaração da aplicação
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# create the flask object
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///storage.db'
db = SQLAlchemy(app) # instacia do data-base

# tem que ser declarado depois da declaração da var app
from app.controllers import default