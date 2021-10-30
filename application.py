from flask import Flask, Response, request
from flask_cors import CORS
import json
import uuid
import boto3
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

from application_services.FriendsResource.friends_service import FriendsResource
from utils import rest_utils

after_request_dict = {
    "add_friend_request": {"POST": {"subject": "NEW FRIEND REQUEST ADDED"}},
    "accept_friend_request": {"POST": {"subject": "NEW FRIEND ADDED"}},
    "decline_friend_request": {"DELETE": {"subject": "A FRIEND REQUEST IS DECLINED"}},
    "cancel_friend_request": {"DELETE": {"subject": "A FRIEND REQUEST IS CANCELLED"}},
    "delete_friend": {"DELETE": {"subject": "A FRIEND IS DELETED"}}
}

application = Flask(__name__)
CORS(application)

@application.route('/friends/<user>', methods=["GET"])
def get_friends(user):
    try:
        user = str(user)
        res = FriendsResource.get_friends(user)
        rsp = Response(json.dumps(res), status=200, content_type="application/json")
    except Exception as e:
        # HTTP status code.
        logging.error("/friends/<user>, e = {}".format(e))
        rsp = Response("INTERNAL ERROR", status=500, content_type="text/plain")

    return rsp

# Return list of pending friends that added you
@application.route('/friends/<user>/pending', methods=["GET"])
def get_pending_friends(user):
    try:
        user = str(user)
        res = FriendsResource.get_pending_friends(user)
        rsp = Response(json.dumps(res), status=200, content_type="application/json")
    except Exception as e:
        # HTTP status code.
        logging.error("/friends/<user>/pending, e = {}".format(e))
        rsp = Response("INTERNAL ERROR", status=500, content_type="text/plain")

    return rsp

# Return list of pending friends that you added
@application.route('/friends/<user>/pending_request', methods=["GET"])
def get_pending_friends_request(user):
    try:
        user = str(user)
        res = FriendsResource.get_pending_friends_request(user)
        rsp = Response(json.dumps(res), status=200, content_type="application/json")
    except Exception as e:
        # HTTP status code.
        logging.error("/friends/<user>/pending_request, e = {}".format(e))
        rsp = Response("INTERNAL ERROR", status=500, content_type="text/plain")

    return rsp

@application.route('/friends/<user>/accept', methods=["POST"])
def accept_friend_request(user):
    try:
        inputs = rest_utils.RESTContext(request)
        rest_utils.log_request("accept_friend_request", inputs)
        user = str(user)

        if inputs.method == "POST":
            friend = inputs.data["friend_id"]
            res = FriendsResource.accept_friend_request(user, friend)
            rsp = Response(json.dumps(res), status=200, content_type="application/json")
        else:
            rsp = Response("NOT IMPLEMENTED", status=501)
    except Exception as e:
        # HTTP status code.
        logging.error("/friends/<user>/accept, e = {}".format(e))
        rsp = Response("INTERNAL ERROR", status=500, content_type="text/plain")

    return rsp

@application.route('/friends/<user>/decline', methods=["DELETE"])
def decline_friend_request(user):
    try:
        inputs = rest_utils.RESTContext(request)
        rest_utils.log_request("decline_friend_request", inputs)
        user = str(user)

        if inputs.method == "DELETE":
            friend = inputs.data["friend_id"]
            res = FriendsResource.decline_friend_request(user, friend)
            rsp = Response(json.dumps(res), status=200, content_type="application/json")
        else:
            rsp = Response("NOT IMPLEMENTED", status=501)
    except Exception as e:
        # HTTP status code.
        logging.error("/friends/<user>/decline, e = {}".format(e))
        rsp = Response("INTERNAL ERROR", status=500, content_type="text/plain")

    return rsp

@application.route('/friends/<user>/add', methods=["POST"])
def add_friend_request(user):
    try:
        inputs = rest_utils.RESTContext(request)
        rest_utils.log_request("add_friend_request", inputs)
        user = str(user)

        if inputs.method == "POST":
            friend = inputs.data["friend_id"]
            res = FriendsResource.add_friend_request(user, friend)
            rsp = Response(json.dumps(res), status=200, content_type="application/json")
        else:
            rsp = Response("NOT IMPLEMENTED", status=501)
    except Exception as e:
        # HTTP status code.
        logging.error("/friends/<user>/add, e = {}".format(e))
        rsp = Response("INTERNAL ERROR", status=500, content_type="text/plain")

    return rsp

@application.route('/friends/<user>/cancel', methods=["DELETE"])
def cancel_friend_request(user):
    try:
        inputs = rest_utils.RESTContext(request)
        rest_utils.log_request("cancel_friend_request", inputs)
        user = str(user)

        if inputs.method == "DELETE":
            friend = inputs.data["friend_id"]
            res = FriendsResource.cancel_friend_request(user, friend)
            rsp = Response(json.dumps(res), status=200, content_type="application/json")
        else:
            rsp = Response("NOT IMPLEMENTED", status=501)
    except Exception as e:
        # HTTP status code.
        logging.error("/friends/<user>/cancel, e = {}".format(e))
        rsp = Response("INTERNAL ERROR", status=500, content_type="text/plain")

    return rsp

@application.route('/friends/<user>/delete', methods=["DELETE"])
def delete_friend(user):
    try:
        inputs = rest_utils.RESTContext(request)
        rest_utils.log_request("delete_friend", inputs)
        user = str(user)

        if inputs.method == "DELETE":
            friend = inputs.data["friend_id"]
            res = FriendsResource.delete_friend(user, friend)
            rsp = Response(json.dumps(res), status=200, content_type="application/json")
        else:
            rsp = Response("NOT IMPLEMENTED", status=501)
    except Exception as e:
        # HTTP status code.
        logging.error("/friends/<user>/remove, e = {}".format(e))
        rsp = Response("INTERNAL ERROR", status=500, content_type="text/plain")

    return rsp

@application.route('/friends/insert', methods=["POST"])
def insert_user():
    try:
        inputs = rest_utils.RESTContext(request)
        rest_utils.log_request("insert_user", inputs)

        if inputs.method == "POST":
            user = inputs.data["user_id"]
            res = FriendsResource.insert_user(user)
            rsp = Response(json.dumps(res), status=200, content_type="application/json")
        else:
            rsp = Response("NOT IMPLEMENTED", status=501)
    except Exception as e:
        # HTTP status code.
        logging.error("/friends/insert, e = {}".format(e))
        rsp = Response("INTERNAL ERROR", status=500, content_type="text/plain")

    return rsp

@application.route('/friends/delete', methods=["DELETE"])
def delete_user():
    try:
        inputs = rest_utils.RESTContext(request)
        rest_utils.log_request("delete_user", inputs)

        if inputs.method == "DELETE":
            user = inputs.data["user_id"]
            res = FriendsResource.delete_user(user)
            rsp = Response(json.dumps(res), status=200, content_type="application/json")
        else:
            rsp = Response("NOT IMPLEMENTED", status=501)
    except Exception as e:
        # HTTP status code.
        logging.error("/friends/delete, e = {}".format(e))
        rsp = Response("INTERNAL ERROR", status=500, content_type="text/plain")

    return rsp

@application.after_request
def after_request(response):
    inputs = rest_utils.RESTContext(request)
    print(after_request_dict)
    print(inputs.endpoint in after_request_dict)
    if inputs.endpoint in after_request_dict:
        if inputs.method in after_request_dict[inputs.endpoint]:
            user_id = inputs.path.split("/")[2]
            friend_id = inputs.data["friend_id"]
            message = {
                "user_id": user_id,
                "friend_id": friend_id,
            }
            
            client = boto3.client('sns', region_name="us-east-1")
            sns_response = client.publish(
                TargetArn="arn:aws:sns:us-east-1:593444383578:test",
                Message=json.dumps({'default': json.dumps(message)}),
                Subject=after_request_dict[request.endpoint][request.method]["subject"],
                MessageStructure='json'
            )
    
    return response

if __name__ == '__main__':
    application.run(host="0.0.0.0", port=5000)
