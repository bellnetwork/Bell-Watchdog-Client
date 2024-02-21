import asyncio, os
from utils.sys.sys_messages.logging import setup_custom_logging

async def create_connection(sio, socketio):
    while True:
        try:
            await sio.connect(os.getenv('SERVER_HOSTNAME'), transports=['websocket'],  namespaces=['/'])
            setup_custom_logging('info', 'Connection Status', 'Successfully connected to the server.')
            break  # Exit the loop upon successful connection
        except socketio.exceptions.ConnectionError as e:
            setup_custom_logging('error', 'Connection Status', f'Connection attempt failed: {e}')
            setup_custom_logging('error', 'Connection Status', 'Attempting to reconnect in 6 seconds...')
            await asyncio.sleep(6)  # Wait before the next attempt
