import boto3
import datetime
import random
import string
import logging
import json
import os

class FormatterJSON(logging.Formatter):
    def format(self, record):
        record.message = record.getMessage()
        if self.usesTime():
            record.asctime = self.formatTime(record, self.datefmt)
        j = {
            'levelname': record.levelname,
            'time': '%(asctime)s.%(msecs)dZ' % dict(asctime=record.asctime, msecs=record.msecs),
            'aws_request_id': getattr(record, 'aws_request_id', '00000000-0000-0000-0000-000000000000'),
            'message': record.message,
            'module': record.module,
            'extra_data': record.__dict__.get('data', {}),
        }
        return json.dumps(j)


logger = logging.getLogger()
logger.setLevel('INFO')

formatter = FormatterJSON(
    '[%(levelname)s]\t%(asctime)s.%(msecs)dZ\t%(levelno)s\t%(message)s\n',
    '%Y-%m-%dT%H:%M:%S'
)
# Replace the LambdaLoggerHandler formatter :
logger.handlers[0].setFormatter(formatter)

client = boto3.client('dynamodb')

def lambda_handler(event, context):
    
  logger.info('Process Info: %s', extra=dict(data=event))
  
  val = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
  print('Event ID is ' + val)
  
  age = datetime.date.today().year - int(event.get('YearOfBirth'))
  print('Age of ' + event.get('FirstName') + ' ' + event.get('LastName') + ' is ' + str(age))
  
  data = client.put_item(
    TableName='UserData',
    Item={
        'UserID': {
            'S' : val
        },
        'FirstName': {
            'S' : event.get('FirstName')
        },
        'LastName': {
            'S' : event.get('LastName')
        },
        'YearOfBirth': {
            'N' : event.get('YearOfBirth')
        },
        'Age': {
            'N' : str(age)
        }
    }
  )

  response = {
      'statusCode': 200,
      'body': 'successfully created item!',
      'headers': {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
      },
  }
  
  return response