from flask import Flask, Response, request
import database_services.RDBService as d_service
from flask_cors import CORS
import json
import uuid

import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

from application_services.FriendsResource.friends_service import FriendsResource
from utils import rest_utils

app = Flask(__name__)
CORS(app)


@app.route('/friends/<user>', methods=["GET"])
def get_friends(user):
    try:
        res = FriendsResource.get_friends(user)
        rsp = Response(json.dumps(res), status=200, content_type="application/json")
    except Exception as e:
        # HTTP status code.
        print("/friends/<user>, e = ", e)
        rsp = Response("INTERNAL ERROR", status=500, content_type="text/plain")

    return rsp

# Return list of pending friends that added you
@app.route('/friends/<user>/pending', methods=["GET"])
def get_pending_friends(user):
    try:
        res = FriendsResource.get_pending_friends(user)
        rsp = Response(json.dumps(res), status=200, content_type="application/json")
    except Exception as e:
        # HTTP status code.
        print("/friends/<user>/pending, e = ", e)
        rsp = Response("INTERNAL ERROR", status=500, content_type="text/plain")

    return rsp

# Return list of pending friends that you added
@app.route('/friends/<user>/pending_request', methods=["GET"])
def get_pending_friends_request(user):
    try:
        res = FriendsResource.get_pending_friends_request(user)
        rsp = Response(json.dumps(res), status=200, content_type="application/json")
    except Exception as e:
        # HTTP status code.
        print("/friends/<user>/pending_request, e = ", e)
        rsp = Response("INTERNAL ERROR", status=500, content_type="text/plain")

    return rsp

@app.route('/friends/<user>/accept', methods=["POST"])
def accept_friend_request(user):
    try:
        inputs = rest_utils.RESTContext(request)
        rest_utils.log_request("accept_friend_request", inputs)

        if inputs.method == "POST":
            friend = inputs.data["friend_id"]
            res = FriendsResource.accept_friend_request(user, friend)
            rsp = Response(json.dumps(res), status=200, content_type="application/json")
        else:
            rsp = Response("NOT IMPLEMENTED", status=501)
    except Exception as e:
        # HTTP status code.
        print("/friends/<user>/accept, e = ", e)
        rsp = Response("INTERNAL ERROR", status=500, content_type="text/plain")

    return rsp

@app.route('/friends/<user>/decline', methods=["DELETE"])
def decline_friend_request(user):
    try:
        inputs = rest_utils.RESTContext(request)
        rest_utils.log_request("decline_friend_request", inputs)

        if inputs.method == "DELETE":
            friend = inputs.data["friend_id"]
            res = FriendsResource.decline_friend_request(user, friend)
            rsp = Response(json.dumps(res), status=200, content_type="application/json")
        else:
            rsp = Response("NOT IMPLEMENTED", status=501)
    except Exception as e:
        # HTTP status code.
        print("/friends/<user>/decline, e = ", e)
        rsp = Response("INTERNAL ERROR", status=500, content_type="text/plain")

    return rsp

@app.route('/friends/<user>/add', methods=["POST"])
def add_friend_request(user):
    try:
        inputs = rest_utils.RESTContext(request)
        rest_utils.log_request("add_friend_request", inputs)

        if inputs.method == "POST":
            friend = inputs.data["friend_id"]
            res = FriendsResource.add_friend_request(user, friend)
            rsp = Response(json.dumps(res), status=200, content_type="application/json")
        else:
            rsp = Response("NOT IMPLEMENTED", status=501)
    except Exception as e:
        # HTTP status code.
        print("/friends/<user>/add, e = ", e)
        rsp = Response("INTERNAL ERROR", status=500, content_type="text/plain")

    return rsp


@app.route('/friends/<user>/cancel', methods=["DELETE"])
def cancel_friend_request(user):
    try:
        inputs = rest_utils.RESTContext(request)
        rest_utils.log_request("cancel_friend_request", inputs)

        if inputs.method == "DELETE":
            friend = inputs.data["friend_id"]
            res = FriendsResource.cancel_friend_request(user, friend)
            rsp = Response(json.dumps(res), status=200, content_type="application/json")
        else:
            rsp = Response("NOT IMPLEMENTED", status=501)
    except Exception as e:
        # HTTP status code.
        print("/friends/<user>/cancel, e = ", e)
        rsp = Response("INTERNAL ERROR", status=500, content_type="text/plain")

    return rsp

@app.route('/friends/<user>/remove', methods=["DELETE"])
def delete_friend(user):
    try:
        inputs = rest_utils.RESTContext(request)
        rest_utils.log_request("delete_friend", inputs)

        if inputs.method == "DELETE":
            friend = inputs.data["friend_id"]
            res = FriendsResource.delete_friend(user, friend)
            rsp = Response(json.dumps(res), status=200, content_type="application/json")
        else:
            rsp = Response("NOT IMPLEMENTED", status=501)
    except Exception as e:
        # HTTP status code.
        print("/friends/<user>/remove, e = ", e)
        rsp = Response("INTERNAL ERROR", status=500, content_type="text/plain")

    return rsp

@app.route('/friends/insert', methods=["POST"])
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
        print("/friends/insert, e = ", e)
        rsp = Response("INTERNAL ERROR", status=500, content_type="text/plain")

    return rsp

@app.route('/friends/delete', methods=["POST"])
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
        print("/friends/delete, e = ", e)
        rsp = Response("INTERNAL ERROR", status=500, content_type="text/plain")

    return rsp

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
