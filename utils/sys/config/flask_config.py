import socketio
from celery import Celery
from dotenv import load_dotenv
import os, random

def create_app():
    # Load environment variables from .env file
    #load_dotenv()

    socketio = SocketIO(app, async_mode='threading')
    sio = socketio.Client()

    server_ip = 'Enter your server ip for verification'
    server_id = 'Enter your server id for verification'

    celery = Celery(app.import_name, broker=os.environ.get('CELERY_BROKER_URL'))

    return app, socketio, sio, celery, server_ip, server_id, debug_status, engineio_logger
