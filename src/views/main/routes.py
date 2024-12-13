from flask import render_template, Blueprint
from os import path

from src.config import Config

TEMPLATES_FOLDER = path.join(Config.BASE_DIR, Config.TEMPLATES_FOLDERS, "main")
main_blueprint = Blueprint("main", __name__, template_folder=TEMPLATES_FOLDER)

@main_blueprint.route("/filter")
def filter_data():
    return render_template("filter_data.html")