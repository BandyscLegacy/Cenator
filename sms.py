import requests
import datetime
from twilio.rest import Client

class SMS(object):

    def __init__(self, account_sid, auth_token):
        self.__account_sid = account_sid
        self.__auth_token = auth_token

    def send(self, from_, to, message):
        client = Client(self.__account_sid, self.__auth_token)

        message = client.messages \
                        .create(
                            body=message,
                            from_=from_,
                            to=to
                        )

        print(message.sid)