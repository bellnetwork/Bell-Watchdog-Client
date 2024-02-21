# Connect.py

from utils.sys.sys_messages.logging import setup_custom_logging

def accept_connect(sio):
    @sio.event
    async def connect():
        setup_custom_logging('info', 'Connection Status', 'Connected to the websocket server.')

def accept_reconnect(sio): 
    @sio.event
    async def reconnect():
        setup_custom_logging('info', 'Connection Status', 'Reconnected to the server.')