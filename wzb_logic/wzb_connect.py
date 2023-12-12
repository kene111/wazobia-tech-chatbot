from flask import Blueprint
wzb_endpoints = Blueprint('wzb_endpoints', __name__)
import json
from flask_cors import cross_origin
from .config.wzb_config import WZBConfig
from flask import jsonify, request, Response


@wzb_endpoints.route("/customer_service", methods=['POST'])
@cross_origin()
def customer_service():
    user_request = request.json["user_query"]
    WZBConfig.bot.set_user_request_info(user_request)
    response = WZBConfig.bot.answer_question()
    message = {"response":response.strip()}
    return Response(response=json.dumps(message), status=200, mimetype='application/json')