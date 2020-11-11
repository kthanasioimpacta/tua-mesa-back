# /usr/bin/env python
# Download the twilio-python library from twilio.com/docs/libraries/python
from flask import current_app
from twilio.rest import Client

# Find these values at https://twilio.com/user/account
# account_sid = current_app.config['TWILIO_ACCOUNT_SID']
# auth_token = current_app.config['TWILIO_AUTH_TOKEN']

TWILIO_ACCOUNT_SID = 'AC483808afaac154ec873a226270053661'
TWILIO_AUTH_TOKEN = 'bf40deff0fcc9bc8f03dc0019f4d02d7'

def SendSMS(customer_phone_number, body):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    message = client.api.account.messages.create(
        to="+5511981677677",
        from_="+12087470336",
        body=body)


    return message.sid