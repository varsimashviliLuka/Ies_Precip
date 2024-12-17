from flask import render_template, Blueprint
from os import path
from datetime import datetime

from src.config import Config

TEMPLATES_FOLDER = path.join(Config.BASE_DIR, Config.TEMPLATES_FOLDERS, "filter")
filter_blueprint = Blueprint("filter", __name__, template_folder=TEMPLATES_FOLDER)

@filter_blueprint.route("/filter")
def filter():
    today_date = datetime.today().strftime('%Y-%m-%d')
    return render_template("filter.html", today_date=today_date)