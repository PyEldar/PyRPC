from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restplus import Api, fields

__version__ = 'v0.0.0'

app = Flask(__name__)
app.config.from_object('rpcconfig')

api = Api(app)

call = api.model(
   'call_method', {
       "jsonrpc": fields.String('rpc version'),
       'method': fields.String,
       'params': fields.Raw(example={}),
       'id': fields.Integer,
   }
)

db = SQLAlchemy(app)

from rpc.routes.hello import Hello