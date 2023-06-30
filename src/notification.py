"""
Example usage of class:

from src.notification import TwilioManager
tm = TwilioManager()
resp = tm.send_message(message='Camp is ready!', to='+16478337641')

"""
from __future__ import annotations

import os

from dotenv import load_dotenv
from twilio.rest import Client


class TwilioManager:
    def __init__(self):
        load_dotenv()
        self.account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        self.auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        self.from_number = os.getenv('TWILIO_NUMBER')
        self.client = Client(self.account_sid, self.auth_token)

    def send_message(self, message: str, to: str):
        """Send a text message using twilio

        Parameters
        ----------
        message : str
            the message that you would like to send
        to : str
            the phone number you would like to send it to
        """
        response = self.client.messages.create(
            from_=self.from_number,
            body=message,
            to=to,
        )
        print(f'Message sent! Message SID: {response.sid}')
        return response
