from __future__ import annotations

import asyncio

from notifciation import TwilioManager
from scraper import DataCollector


async def main():
    dc = DataCollector(start_date='2023-08-22', end_date='2023-08-23')
    await dc.initialize()

    data = await dc.extract_data()

    if len(data) > 0:
        tm = TwilioManager()
        tm.send_message(message='Camp is ready!', to='+16478337641')

    print(data)


if __name__ == '__main__':
    asyncio.run(main())
