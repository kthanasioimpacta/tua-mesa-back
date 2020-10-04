# /usr/bin/env python
# Download the twilio-python library from twilio.com/docs/libraries/python
from flask import current_app
from twilio.rest import Client

# Find these values at https://twilio.com/user/account
account_sid = current_app.config['TWILIO_ACCOUNT_SID']
auth_token = current_app.config['TWILIO_AUTH_TOKEN']

# def SendSMS(lineUpId):
client = Client(account_sid, auth_token)

client.api.account.messages.create(
    to="+5511991920414",
    from_="+12087470336",
    body="TUA MESA: ")