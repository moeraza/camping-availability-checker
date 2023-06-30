from __future__ import annotations

from src.notification import TwilioManager


def test_twilio():
    tm = TwilioManager()
    resp = tm.send_message(message='Camp is ready!', to='+16478337641')
    assert resp.error_code is None
