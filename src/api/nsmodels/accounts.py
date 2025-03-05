from flask_restx import reqparse, fields, inputs
from src.extensions import api


accounts_ns = api.namespace('Accounts', description='API მომხმარებლის ექაუნთების შესახებ', path='/api')

user_model = accounts_ns.model('User', {
    'email': fields.String(required=True, type=inputs.email(check=True), description='მომხმარებლის ელ.ფოსტა'),
    'role': fields.String(required=True, type=str, description='როლის სახელი'),
    'uuid': fields.String(required=True, type=str, description='მომხმარებლის uuid')
})

user_parser = reqparse.RequestParser()
user_parser.add_argument("role_name", required=True, type=str, help="გთხოვთ შეიყვანეთ სასურველი როლი (Admin/User)", default='User')
user_parser.add_argument("email", required=True, type=str, help="გთხოვთ შეიყვანეთ ახალი ელ.ფოსტა", default='satesto@example.com')

request_password_reset_parser = reqparse.RequestParser()
request_password_reset_parser.add_argument("modalEmail", required=True, type=str, help="გთხოვთ შეიყვანეთ ახალი ელ.ფოსტა", default='satesto@example.com')

password_reset_parser = reqparse.RequestParser()
password_reset_parser.add_argument("token", required=True, type=str, help="გთხოვთ შეიყვანოთ ტოკენი", default='RmYTkyNTQxZjljMSI.Z8bhDw.1YCel4ik_BUzPqPpMZDvP8TaPMM.....')
password_reset_parser.add_argument("password", required=True, type=str, help="გთხოვთ შეიყვანეთ ახალი პაროლი", default='PAROLIparoli123')
password_reset_parser.add_argument("retype_password", required=True, type=str, help="გთხოვთ გაიმეოროთ პაროლი", default='PAROLIparoli123')