import os
import json
import logging

import boto3

from utils import rest_utils


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

after_request_dict = {
    "add_friend_request": {"POST": {"subject": "NEW FRIEND REQUEST ADDED"}},
    "accept_friend_request": {"POST": {"subject": "NEW FRIEND ADDED"}},
    "decline_friend_request": {"DELETE": {"subject": "A FRIEND REQUEST IS DECLINED"}},
    "cancel_friend_request": {"DELETE": {"subject": "A FRIEND REQUEST IS CANCELLED"}},
    "delete_friend": {"DELETE": {"subject": "A FRIEND IS DELETED"}}
}

def notify_sns(request):
    inputs = rest_utils.RESTContext(request)
    if inputs.endpoint in after_request_dict:
        if inputs.method in after_request_dict[inputs.endpoint]:
            try:
                user_id = inputs.path.split("/")[2]
                friend_id = inputs.data["friend_id"]
                message = {
                    "user_id": user_id,
                    "friend_id": friend_id,
                }
                
                client = boto3.client('sns', region_name="us-east-1")
                sns_response = client.publish(
                    TargetArn=os.environ.get("SNS_ARN", None),
                    Message=json.dumps({'default': json.dumps(message)}),
                    Subject=after_request_dict[request.endpoint][request.method]["subject"],
                    MessageStructure='json'
                )
            except Exception as e:
                logger.error("notify_sns, e = {}".format(e))