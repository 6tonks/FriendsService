import json
import requests
import boto3

def lambda_handler(event, context):
    message = "not interested subject, do nothing"
    print("Event: {}".format(event))
    if event['Records'][0]['Sns']['Subject'] == 'NEW USER':
        user_id = json.loads(event['Records'][0]['Sns']['Message'])['user_id']
        r = requests.post('http://fs-env-1.eba-jtts5wvb.us-east-1.elasticbeanstalk.com/friends/insert', json={"user_id": user_id})
        if r.status_code != 200:
            client = boto3.client('sns')
            response = client.publish(
                TargetArn="arn:aws:sns:us-east-1:593444383578:test",
                Message=json.dumps({'default': json.dumps({"user_id": user_id})}),
                Subject="ADD USER FAILURE",
                MessageStructure='json'
            )
        print("Response code: {}".format(r.status_code))
        print("Response body: {}".format(r.content))
        message = r.content

    return message