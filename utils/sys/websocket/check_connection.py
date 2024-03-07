import asyncio
from utils.sys.sys_messages.logging import setup_custom_logging
from conf import *

async def create_connection(sio):
    while True:
        try:
            await sio.connect(SERVER_HOSTNAME, transports=['websocket'], namespaces=['/'])
            # After successful connection, send the authentication data
            await sio.emit('authenticate', {'bell_api': BELL_API, 'tunnel_id': TUNNEL_ID}, namespace='/')
            setup_custom_logging('info', 'Connection Status', 'Successfully connected and sent authentication data to the server.')
            break  # Exit the loop upon successful connection
        except Exception as e:
            setup_custom_logging('error', 'Connection Status', f'Connection attempt failed: {e}')
            setup_custom_logging('error', 'Connection Status', 'Attempting to reconnect in 6 seconds...')
            await asyncio.sleep(6)  # Wait before the next attempt