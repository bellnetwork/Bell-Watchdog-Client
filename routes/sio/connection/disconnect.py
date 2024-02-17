# Disconnect.py

def accept_disconnect(sio):
    @sio.event
    async def disconnect():
        print("I'm disconnected!")
       
def connection_error(sio):
    @sio.event
    async def connect_error(data):
        print("Connection failed:", data)