# /usr/bin/env python
# Download the twilio-python library from twilio.com/docs/libraries/python
from flask import current_app
from twilio.rest import Client

# Find these values at https://twilio.com/user/account
# account_sid = current_app.config['TWILIO_ACCOUNT_SID']
# auth_token = current_app.config['TWILIO_AUTH_TOKEN']

TWILIO_ACCOUNT_SID = 'AC483808afaac154ec873a226270053661'

def SendSMS(customer_phone_number, body, auth):
    client = Client(TWILIO_ACCOUNT_SID, auth)

    message = client.api.account.messages.create(
        to=customer_phone_number,
        from_="+12087470336",
        body=body)

    return message.sid