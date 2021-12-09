import json
import logging

import uuid
from flask_cors import CORS
from flask import Flask, Response, request

from utils import rest_utils
from middleware.notification import notify_sns
from application_services.FriendsResource.friends_service import FriendsResource


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

application = Flask(__name__)
CORS(application)

@application.route('/friends/<user>', methods=["GET"])
def get_friends(user):
    try:
        user = str(user)
        inputs = rest_utils.RESTContext(request)
        rest_utils.log_request("get_friends", inputs)

        wc, lim, offs, links = FriendsResource.get_links(inputs)

        friend_list = FriendsResource.get_friends(user, lim, offs, wc)
        
        res = {}
        res['friend_list'] = friend_list
        
        # links
        res['links'] = links

        # remove next if empty friend_list or result less than limit
        if not friend_list or len(friend_list)<int(lim):
            res['links'] = res['links'][:-1]
        
        rsp = Response(json.dumps(res), status=200, content_type="application/json")
    except Exception as e:
        # HTTP status code.
        logger.error("/friends/<user>, e = {}".format(e))
        rsp = Response("INTERNAL ERROR", status=500, content_type="text/plain")

    return rsp

# Return list of pending friends that added you
@application.route('/friends/<user>/pending', methods=["GET"])
def get_pending_friends(user):
    try:
        user = str(user)
        # res = FriendsResource.get_pending_friends(user)
        inputs = rest_utils.RESTContext(request)
        rest_utils.log_request("get_pending_friends", inputs)

        wc, lim, offs, links = FriendsResource.get_links(inputs)

        friend_list = FriendsResource.get_pending_friends(user, lim, offs, wc)
        
        res = {}
        res['friend_list'] = friend_list

        # links
        res['links'] = links

        # remove next if empty friend_list or result less than limit
        if not friend_list or len(friend_list)<int(lim):
            res['links'] = res['links'][:-1]

        rsp = Response(json.dumps(res), status=200, content_type="application/json")
    except Exception as e:
        # HTTP status code.
        logger.error("/friends/<user>/pending, e = {}".format(e))
        rsp = Response("INTERNAL ERROR", status=500, content_type="text/plain")

    return rsp

# Return list of pending friends that you added
@application.route('/friends/<user>/pending_request', methods=["GET"])
def get_pending_friends_request(user):
    try:
        user = str(user)
        # res = FriendsResource.get_pending_friends_request(user)
        inputs = rest_utils.RESTContext(request)
        rest_utils.log_request("get_pending_friends_request", inputs)

        wc, lim, offs, links = FriendsResource.get_links(inputs)

        friend_list = FriendsResource.get_pending_friends_request(user, lim, offs, wc)
        
        res = {}
        res['friend_list'] = friend_list

        # links
        res['links'] = links

        # remove next if empty friend_list or result less than limit
        if not friend_list or len(friend_list)<int(lim):
            res['links'] = res['links'][:-1]

        rsp = Response(json.dumps(res), status=200, content_type="application/json")
    except Exception as e:
        # HTTP status code.
        logger.error("/friends/<user>/pending_request, e = {}".format(e))
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
            # Response 201 for POST -- CREATED
            rsp = Response(json.dumps(res), status=201, content_type="application/json")
        else:
            rsp = Response("NOT IMPLEMENTED", status=501)
    except Exception as e:
        # HTTP status code.
        logger.error("/friends/<user>/accept, e = {}".format(e))
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
            # Response 204 for DELETE
            rsp = Response(json.dumps(res), status=204, content_type="application/json")
        else:
            rsp = Response("NOT IMPLEMENTED", status=501)
    except Exception as e:
        # HTTP status code.
        logger.error("/friends/<user>/decline, e = {}".format(e))
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
            # Response 201 for POST -- CREATED
            rsp = Response(json.dumps(res), status=201, content_type="application/json")
        else:
            rsp = Response("NOT IMPLEMENTED", status=501)
    except Exception as e:
        # HTTP status code.
        logger.error("/friends/<user>/add, e = {}".format(e))
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
            # Response 204 for DELETE
            rsp = Response(json.dumps(res), status=204, content_type="application/json")
        else:
            rsp = Response("NOT IMPLEMENTED", status=501)
    except Exception as e:
        # HTTP status code.
        logger.error("/friends/<user>/cancel, e = {}".format(e))
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
            # Response 204 for DELETE
            rsp = Response(json.dumps(res), status=204, content_type="application/json")
        else:
            rsp = Response("NOT IMPLEMENTED", status=501)
    except Exception as e:
        # HTTP status code.
        logger.error("/friends/<user>/remove, e = {}".format(e))
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
            # add url location for reference
            res['location'] = f'/friends/{res["user_id"]}'
            # Response 201 for POST -- CREATED
            rsp = Response(json.dumps(res), status=201, content_type="application/json")
        else:
            rsp = Response("NOT IMPLEMENTED", status=501)
    except Exception as e:
        # HTTP status code.
        logger.error("/friends/insert, e = {}".format(e))
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
            # Response 204 for DELETE
            rsp = Response(json.dumps(res), status=204, content_type="application/json")
        else:
            rsp = Response("NOT IMPLEMENTED", status=501)
    except Exception as e:
        # HTTP status code.
        logger.error("/friends/delete, e = {}".format(e))
        rsp = Response("INTERNAL ERROR", status=500, content_type="text/plain")

    return rsp

@application.after_request
def after_request(response):
    notify_sns(request)
    return response

if __name__ == '__main__':
    application.run(host="0.0.0.0", port=5000)
