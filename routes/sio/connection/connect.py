# Connect.py

import logging

def accept_connect(sio):
    @sio.event
    async def connect():
        logging.error("I'm connected!")
        sio.emit('message', 'Hello, this is the server x3nwcbr3')

def accept_reconnect(sio): 
    @sio.event
    async def reconnect():
        print("Reconnected to the server.")