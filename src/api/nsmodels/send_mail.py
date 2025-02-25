from flask_restx import reqparse, fields
from src.extensions import api


# Define API Namespace
email_ns = api.namespace('Email', description='Email Sending API', path='/api')

# Define Email Request Model (Flask-RESTx Schema)
email_parser = reqparse.RequestParser()

email_parser.add_argument("api_key", required=True, type=str, help="Recipient email address")
email_parser.add_argument("recipient", required=True, type=str, help="Recipient email address")
email_parser.add_argument("subject", required=True, type=str, help="Recipient email address")
email_parser.add_argument("message", required=True, type=str, help="Recipient email address")
