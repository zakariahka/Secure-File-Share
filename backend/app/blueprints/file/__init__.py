from flask import Blueprint

file_bp = Blueprint("file_bp", __name__)

from . import file_routes