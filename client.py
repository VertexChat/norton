import asyncio
import ssl
from pathlib import Path

import websockets

session_ids = ['60a9af55-ecc4-4250-9d99-9ee7c75da6fd',
               'bfdee4a6-7f26-4a20-a15f-90e23f2a0405',
               '32fa829b-652c-49b2-8fad-fdeb9689a61b',
               '3bf832eb-c1fe-4430-bd02-95b02c8e0c3d'
               ]

SESSION_ID = '7036c1a9-a294-488f-bbd3-0f68f110d84a'
certs = Path(*Path(__file__).parts[:-1] + ('certs',))

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.load_verify_locations(capath=certs)
ssl_context.load_cert_chain(certs / 'fullchain.pem', certs / 'privkey.pem')


async def updater():
    uri = "wss://localhost:8765"
    async with websockets.connect(
        uri, ssl=ssl_context
    ) as websocket:
        await websocket.send(SESSION_ID)
        print(f"> Sending id: {SESSION_ID}")

        updates = await websocket.recv()
        print(f"< Updates: {updates}")


asyncio.get_event_loop().run_until_complete(updater())
