from flask import Blueprint, send_from_directory, abort
from os import path
from src.config import Config

export_blueprint = Blueprint("export", __name__)

@export_blueprint.route("/export/<filename>")
def export(filename):
    file_path = path.join(Config.EXPORT_DIR, filename)
    if not path.exists(file_path):
        abort(404)
    return send_from_directory(Config.EXPORT_DIR, filename)