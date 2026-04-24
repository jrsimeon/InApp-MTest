from flask import Blueprint, render_template

auth = Blueprint('auth', __name__,
    template_folder='templates',
    static_folder='static')

from . import routes