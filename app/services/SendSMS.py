# /usr/bin/env python
# Download the twilio-python library from twilio.com/docs/libraries/python
from twilio.rest import Client

# Find these values at https://twilio.com/user/account
account_sid = "AC483808afaac154ec873a226270053661"
auth_token = "aed5229a82745d9fcc9c33a94d31da70"


# def SendSMS(lineUpId):
client = Client(account_sid, auth_token)

client.api.account.messages.create(
    to="+5511991920414",
    from_="+12087470336",
    body="OI MORRRR!")