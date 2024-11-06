from flask import Blueprint, request, jsonify

api_auth = Blueprint('api_auth', __name__)

@api_auth.route('/prueba', methods=['Post'])
def prueba():

    return "1234"