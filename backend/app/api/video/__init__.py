from flask import Blueprint

video_bp = Blueprint('video', __name__, url_prefix='/video')

from . import videos