import logging, asyncio

async def create_connection(sio, socketio):
    while True:
        try:
            await sio.connect('wss://your_socket_address.com', transports=['websocket'],  namespaces=['/'])
            logging.error("Successfully connected to the server.")
            break  # Exit the loop upon successful connection
        except socketio.exceptions.ConnectionError as e:
            logging.error(f"Connection attempt failed: {e}")
            logging.error("Attempting to reconnect in 6 seconds...")
            await asyncio.sleep(6)  # Wait before the next attempt
