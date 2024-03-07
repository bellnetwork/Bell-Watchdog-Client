# Client config.py

import socketio, asyncio, os
from dotenv import load_dotenv

from utils.sys.sys_messages.logging import setup_custom_logging

def create_app():
    # Load environment variables from .env file
    load_dotenv()
    
    debug = os.getenv('DEBUG', 'False').lower() in ['true', '1', 't']
    engineio_logger = os.getenv('ENGINEIO_LOGGER', 'False').lower() in ['true', '1', 't']
    
    # Creating an instance of AsyncClient from socketio for asynchronous WebSocket communication
    # Enabling logging for better debugging and monitoring of WebSocket events
    sio = socketio.AsyncClient(logger=debug, engineio_logger=engineio_logger) 

    return {
        'sio': sio,
        'client_id': os.getenv('CLIENT_ID'),
        'client_name': os.getenv('CLIENT_NAME'),
        'server_hostname': os.getenv('SERVER_HOSTNAME'),
        'bell_api': os.getenv('BELL_API'),
        'tunnel_id': os.getenv('TUNNEL_ID')
        
    }
