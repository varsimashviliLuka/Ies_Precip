from flask_restx import Resource
from flask import request
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from src.api.nsmodels import email_ns, email_parser
from src.config import TestConfig

# API Keys (Only these can send emails)
API_KEYS = {
    "127.0.0.1": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9",
    "10.0.0.116": "test"
}


def send_mail(emails, subject, message, email_type='plain', email_address=TestConfig.MAIL_USERNAME, email_password=TestConfig.MAIL_PASSWORD):
    msg = MIMEMultipart()
    msg['From'] = email_address
    msg['To'] = ','.join(map(str, emails))
    msg['Subject'] = subject
    msg.attach(MIMEText(message, email_type))

    # set up the SMTP server
    server = smtplib.SMTP(host=TestConfig.MAIL_SERVER, port=TestConfig.MAIL_PORT)
    server.ehlo()
    server.starttls()
    # server.ehlo()
    server.login(email_address, email_password)
    server.sendmail("", emails, msg.as_string())
    del msg
    server.quit()

@email_ns.route("/send")
class SendEmail(Resource):
    @email_ns.doc(parser=email_parser)
    def post(self):
        client_ip = request.remote_addr
        data = email_parser.parse_args()

        api_key = data.get("api_key")

        # Validate API key and IP address
        server_ip = next((ip for ip, key in API_KEYS.items() if key == api_key and client_ip == ip), None)
        if not server_ip:
            return {"error": "Unauthorized access: Invalid API key or Server IP"}, 403

        # Get email data
        recipient = data.get("recipient")
        subject = data.get("subject")
        message = data.get("message")

        try:
            # Send the email
            send_mail(emails=[recipient], subject=subject, message=message)
            return {"message": "Email sent successfully", "ip": server_ip}, 200
        except Exception as e:
            return {"error": f"Failed to send email: {str(e)}"}, 500