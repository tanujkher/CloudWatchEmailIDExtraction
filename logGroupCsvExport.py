import sys
import boto3
from datetime import datetime, timedelta
import time
import json

def logGroupResultForEmail(email, log_group):
    client = boto3.client('logs')

    query = "fields @message | sort @timestamp desc | filter @message like '" + str(email) + "' | limit 1"

    start_query_response = client.start_query(
        logGroupName=log_group,
        startTime=int((datetime.today() - timedelta(hours=5)).timestamp()),
        endTime=int(datetime.now().timestamp()),
        queryString=query,
    )

    query_id = start_query_response['queryId']

    response = None

    while response == None or response['status'] == 'Running':
        # print('Waiting for query to complete ...')
        time.sleep(1)
        response = client.get_query_results(
            queryId=query_id
        )
    
    if(len(response.get('results')) == 0):
        return 'Not Found'
    else:
        for field in response.get('results')[0]:
            if(field.get('field') == '@message'):
                response = json.loads(field.get('value')).get('body')

        return str(response).replace('\'', '"')
