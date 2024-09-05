from flask import Blueprint, jsonify

bp = Blueprint('members', __name__)

@bp.route('/members', methods=['GET'])
def members():
    return jsonify({'members': ['member1', 'member2', 'member34']})
