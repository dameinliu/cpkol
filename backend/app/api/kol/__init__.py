from flask import Blueprint

kol_bp = Blueprint('kol', __name__, url_prefix='/kol')

from . import kol