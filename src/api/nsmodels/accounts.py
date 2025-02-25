from flask_restx import reqparse, fields, inputs
from src.extensions import api


accounts_ns = api.namespace('Accounts', description='API მომხმარებლის ექაუნთების შესახებ', path='/api')

user_model = accounts_ns.model('User', {
    'email': fields.String(required=True, type=inputs.email(check=True), description='The email of the user'),
    'role': fields.String(required=True, type=str, description='The role ID associated with the user')
})