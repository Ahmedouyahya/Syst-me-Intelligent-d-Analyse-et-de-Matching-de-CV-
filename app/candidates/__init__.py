from flask import Blueprint

bp = Blueprint('candidates', __name__)

from app.candidates import routes
