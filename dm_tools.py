from flask import Flask, render_template, Blueprint
from encounterweb import encounter_bp

dm_tools_bp = Blueprint('dm-tools', __name__)

@dm_tools_bp.route('/')
def start():
    return render_template('dm-tools.html')

dm_tools_bp.register_blueprint(encounter_bp, url_prefix='/encounter/')