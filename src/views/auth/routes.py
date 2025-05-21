from flask import render_template, Blueprint, request
from os import path

from src.config import Config

TEMPLATES_FOLDER = path.join(Config.BASE_DIR, Config.TEMPLATES_FOLDERS, "auth")
auth_blueprint = Blueprint("auth", __name__, template_folder=TEMPLATES_FOLDER)

@auth_blueprint.route("/login")
def login():
    message = request.args.get('message')
    return render_template("login.html", message=message)