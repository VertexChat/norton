import asyncio
import json
import pathlib
import ssl
import threading
import time
from multiprocessing.connection import Listener
import websockets

from sqlalchemy import create_engine

from config import Config

engine = create_engine(Config.DEFAULT_URI)
notifications = {}


async def updater(websocket, path):
    session_id = await websocket.recv()
    print(f"< Received session id: {session_id}")

    with engine.connect() as connection:
        query_result = connection.execute("select user, expire_after from session where id=%(session)s", {"session": session_id}).fetchone()
        if query_result is not None:
            user, expire_after = query_result

            if expire_after > time.time():
                print(f'Updater Notifications: {notifications}')
                await websocket.send(json.dumps(notifications.pop(user, [])))
                return

    await websocket.send(json.dumps([]))


def notification_listener():
    listener = Listener(('localhost', 6000), authkey=Config.NOTIFICATION_SERVICE_AUTHKEY)

    while True:
        conn = listener.accept()
        print('connection accepted from', listener.last_accepted)
        msg = conn.recv()
        print(f"Message: {msg}")

        if msg['target'] not in notifications:
            notifications[msg['target']] = []

        if msg not in notifications[msg['target']]:
            notifications[msg['target']].append(msg)


if __name__ == '__main__':
    n = threading.Thread(target=notification_listener)
    n.daemon = True
    n.start()

    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain('/home/daithi/Documents/College/Fourth Year/Final Year Project/norton/certs/fullchain.pem', '/home/daithi/Documents/College/Fourth Year/Final Year Project/norton/certs/privkey.pem')
    # localhost_pem = '/home/daithi/Documents/College/Fourth Year/Final Year Project/norton/certs/fullchain.pem' #pathlib.Path(__file__) / 'ca' / 'privkey.pem'
    # ssl_context.load_cert_chain(localhost_pem)

    start_server = websockets.serve(updater, "localhost", 8765, ssl=ssl_context)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
