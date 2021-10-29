from flask import Flask, Response, request
from flask_cors import CORS
from flask_restful import Resource, Api
from apispec import APISpec
from marshmallow import Schema, fields
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, doc, use_kwargs
import json
import uuid

import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

from application_services.FriendsResource.friends_service import FriendsResource
from utils import rest_utils

application = Flask(__name__)
api = Api(application)  # Flask restful wraps Flask app around it.
application.config.update({
    'APISPEC_SPEC': APISpec(
        title='Friend Service',
        version='v1',
        plugins=[MarshmallowPlugin()],
        openapi_version='2.0.0'
    ),
    'APISPEC_SWAGGER_URL': '/swagger/',  # URI to access API Doc JSON
    'APISPEC_SWAGGER_UI_URL': '/swagger-ui/'  # URI to access UI of API Doc
})

CORS(application)
docs = FlaskApiSpec(application)


class GetFriendResponseSchema(Schema):
    message = fields.Str(default='Success')

class PostResponseSchema(Schema):
    status = fields.Bool(default=True)

class FriendRequestSchema(Schema):
    friend_id = fields.String(required=True, description="user_id of the friend")


#  Restful way of creating APIs through Flask Restful
class GetFriendAPI(MethodResource, Resource):
    @doc(description='Get list of all friends of <user_id>.', tags=['GetFriend'])
    @marshal_with(GetFriendResponseSchema)  # marshalling
    def get(self, user):
        '''
        Get method represents a GET API method
        '''
        try:
            user = str(user)
            res = FriendsResource.get_friends(user)
            rsp = Response(json.dumps(res), status=200, content_type="application/json")
        except Exception as e:
            # HTTP status code.
            logging.error("/friends/<user>, e = {}".format(e))
            rsp = Response("INTERNAL ERROR", status=500, content_type="text/plain")

        return rsp

    # @doc(description='My First GET GetFriend API.', tags=['Awesome'])
    # @use_kwargs(GetFriendRequestSchema, location=('json'))
    # @marshal_with(GetFriendResponseSchema)  # marshalling
    # def post(self, **kwargs):
    #     '''
    #     Get method represents a GET API method
    #     '''
    #     return {'message': 'My First GetFriend API'}

#  Restful way of creating APIs through Flask Restful
class GetPendingFriendAPI(MethodResource, Resource):
    @doc(description='Get list of all pending friends that added <user_id>.', tags=['GetPendingFriend'])
    @marshal_with(GetFriendResponseSchema)  # marshalling
    def get(self, user):
        '''
        Get method represents a GET API method
        '''
        try:
            user = str(user)
            res = FriendsResource.get_pending_friends(user)
            rsp = Response(json.dumps(res), status=200, content_type="application/json")
        except Exception as e:
            # HTTP status code.
            logging.error("/friends/<user>/pending, e = {}".format(e))
            rsp = Response("INTERNAL ERROR", status=500, content_type="text/plain")

        return rsp

#  Restful way of creating APIs through Flask Restful
class GetRequestFriendAPI(MethodResource, Resource):
    @doc(description='Get list of all pending friends <user_id> added.', tags=['GetRequestFriend'])
    @marshal_with(GetFriendResponseSchema)  # marshalling
    def get(self, user):
        '''
        Get method represents a GET API method
        '''
        try:
            user = str(user)
            res = FriendsResource.get_pending_friends_request(user)
            rsp = Response(json.dumps(res), status=200, content_type="application/json")
        except Exception as e:
            # HTTP status code.
            logging.error("/friends/<user>/pending_request, e = {}".format(e))
            rsp = Response("INTERNAL ERROR", status=500, content_type="text/plain")

        return rsp

#  Restful way of creating APIs through Flask Restful
class AcceptFriendAPI(MethodResource, Resource):
    @doc(description='Accept pending friend <friend_id> to be a friend of <user_id>.', tags=['AcceptFriend'])
    @use_kwargs(FriendRequestSchema, location=('json'))
    @marshal_with(PostResponseSchema)  # marshalling
    def post(self, user, **kwargs):
        '''
        Post method represents a POST API method
        '''
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

api.add_resource(GetFriendAPI, '/friends/<user>')
api.add_resource(GetPendingFriendAPI, '/friends/<user>/pending')
api.add_resource(GetRequestFriendAPI, '/friends/<user>/pending_request')
api.add_resource(AcceptFriendAPI, '/friends/<user>/accept')
docs.register(GetFriendAPI)
docs.register(GetPendingFriendAPI)
docs.register(GetRequestFriendAPI)
docs.register(AcceptFriendAPI)

# @application.route('/friends/<user>', methods=["GET"])
# def get_friends(user):
#     try:
#         user = str(user)
#         res = FriendsResource.get_friends(user)
#         rsp = Response(json.dumps(res), status=200, content_type="application/json")
#     except Exception as e:
#         # HTTP status code.
#         logging.error("/friends/<user>, e = {}".format(e))
#         rsp = Response("INTERNAL ERROR", status=500, content_type="text/plain")
#
#     return rsp

# Return list of pending friends that added you
# @application.route('/friends/<user>/pending', methods=["GET"])
# def get_pending_friends(user):
#     try:
#         user = str(user)
#         res = FriendsResource.get_pending_friends(user)
#         rsp = Response(json.dumps(res), status=200, content_type="application/json")
#     except Exception as e:
#         # HTTP status code.
#         logging.error("/friends/<user>/pending, e = {}".format(e))
#         rsp = Response("INTERNAL ERROR", status=500, content_type="text/plain")
#
#     return rsp

# Return list of pending friends that you added
# @application.route('/friends/<user>/pending_request', methods=["GET"])
# def get_pending_friends_request(user):
#     try:
#         user = str(user)
#         res = FriendsResource.get_pending_friends_request(user)
#         rsp = Response(json.dumps(res), status=200, content_type="application/json")
#     except Exception as e:
#         # HTTP status code.
#         logging.error("/friends/<user>/pending_request, e = {}".format(e))
#         rsp = Response("INTERNAL ERROR", status=500, content_type="text/plain")
#
#     return rsp

# @application.route('/friends/<user>/accept', methods=["POST"])
# def accept_friend_request(user):
#     try:
#         inputs = rest_utils.RESTContext(request)
#         rest_utils.log_request("accept_friend_request", inputs)
#         user = str(user)
#
#         if inputs.method == "POST":
#             friend = inputs.data["friend_id"]
#             res = FriendsResource.accept_friend_request(user, friend)
#             rsp = Response(json.dumps(res), status=200, content_type="application/json")
#         else:
#             rsp = Response("NOT IMPLEMENTED", status=501)
#     except Exception as e:
#         # HTTP status code.
#         logging.error("/friends/<user>/accept, e = {}".format(e))
#         rsp = Response("INTERNAL ERROR", status=500, content_type="text/plain")
#
#     return rsp

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

if __name__ == '__main__':
    application.run(host="0.0.0.0", port=5000)
