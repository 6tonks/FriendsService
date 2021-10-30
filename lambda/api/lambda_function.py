import json

def lambda_handler(event, context):
    urls = [
        '/friends/<user>',
        '/friends/<user>/pending',
        '/friends/<user>/pending_request',
        '/friends/<user>/accept',
        '/friends/<user>/decline',
        '/friends/<user>/add',
        '/friends/<user>/cancel',
        '/friends/<user>/delete',
        '/friends/insert',
        '/friends/delete',
    ]
    return {
        'statusCode': 200,
        'body': json.dumps(urls)
    }
