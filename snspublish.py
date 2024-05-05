#!/usr/bin/python3
import boto3
import inspect
import os
import socket

# -------------------------------------
# CONSTANT VARIABLES
# -------------------------------------
__version__ = '0.0.1'
scriptname = os.path.basename(__file__)
base_directory = "/usr/local/scripts"

# -----------------------
# return_session function
# -----------------------
def return_session(iam_user_account):
  function_name = inspect.currentframe().f_code.co_name
  try:
    session = boto3.Session(profile_name=f"{iam_user_account}")
  except Exception as exception:
    message = f"The '{function_name}' function in {base_directory}/{scriptname} on {socket.gethostname()} got the following exception when attempting boto3.Session(profile_name='{iam_user_account}') - {exception}"
    return { "result": "failed", "message": message }
  else:
    return { "result": "success", "session": session }

# -----------------------
# return_sts_client function
# -----------------------
def return_sts_client(session):
  function_name = inspect.currentframe().f_code.co_name
  try:
    sts_client = session.client('sts')
  except Exception as exception:
    message = f"The '{function_name}' function in {base_directory}/{scriptname} on {socket.gethostname()} got the following exception when trying session.client('sts') - {exception}"
    return { "result": "failed", "message": message }
  else:
    return { "result": "success", "sts_client": sts_client }

# -----------------------
# assume_role function
# -----------------------
def assume_role(sts_client, iam_role):
  function_name = inspect.currentframe().f_code.co_name
  try:
    assume_role_response = sts_client.assume_role(
      RoleArn=f"arn:aws:iam::713542074252:role/{iam_role}",
      RoleSessionName=f"AssumeRoleSession1"
    )
  except Exception as exception:
    message = f"The '{function_name}' function in {base_directory}/{scriptname} on {socket.gethostname()} got the following exception when attempting to assume_role arn:aws:iam::713542074252:role/{iam_role} - {exception}"
    return { "result": "failed", "message": message }
  else:
    return { "result": "success", "assume_role_response": assume_role_response }

# -------------------------------------
# Publish message to SNS topic function
# -------------------------------------
def sns_publish(subject, message, topic):
  function_name = inspect.currentframe().f_code.co_name

  return_session_response = return_session('automation')

  try:
    session = return_session_response['session']
  except Exception:
    return return_session_response

  try:
    return_sts_client_response = return_sts_client(session)
  except Exception:
    return return_sts_client
  else:
    sts_client = return_sts_client_response['sts_client']

  try:
    assume_role_response = assume_role(sts_client, 'SNSPublish')
  except Exception:
    return assume_role
  else:
    sts = assume_role_response['assume_role_response']

  try:
    client = session.client(
            'sns',
            aws_access_key_id=sts['Credentials']['AccessKeyId'],
            aws_secret_access_key=sts['Credentials']['SecretAccessKey'],
            aws_session_token=sts['Credentials']['SessionToken'])
  except Exception as exception:
    return f"The '{function_name}' function in {base_directory}/{scriptname} on {socket.gethostname()} got the following exception when attempting to initialize the boto3 sns client - {exception}"
  else:
    try:
      client.publish(
        TopicArn=f"arn:aws:sns:us-east-1:713542074252:{topic}",
        Subject=subject,
        Message=message
      )
    except Exception as exception:
      return f"The '{function_name}' function in {base_directory}/{scriptname} on {socket.gethostname()} got the following exception when attempting to publish message to arn:aws:sns:us-east-1:713542074252:my-topic - {exception}"
    else:
      return_message = f"Successfully published the following message to SNS Topic {topic}\n"
      return_message += f"  Subject -> {subject}\n"
      return_message += f"  Message -> {message}\n"
      return return_message
