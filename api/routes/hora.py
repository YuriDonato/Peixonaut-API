from flask import Blueprint, jsonify
from datetime import datetime

bp = Blueprint('hora', __name__)

@bp.route('/hora', methods=['GET'])
def hora():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return jsonify({'hora': current_time})
