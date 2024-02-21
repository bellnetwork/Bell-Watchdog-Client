# To run, follow these steps:
# Start debug mode:
# cd /etc/bell_sys_monitor_client && python3 -m app
# systemctl start bell_sys_monitor_client
# systemctl restart bell_sys_monitor_client
# systemctl stop bell_sys_monitor_client
# systemctl status bell_sys_monitor_client

# Importing necessary libraries for WebSocket communication and system operations
import asyncio

# Importing utility functions and classes for script configuration and reload functionality
from utils.sys.websocket.connect import main
from utils.sys.config.client_config import create_app

config = create_app()

# This function is designed to encapsulate the standard Python entry point check.
# It initiates the WebSocket client connection and starts the asynchronous event loop.
# This separation of concerns enhances code readability and maintainability.
if __name__ == "__main__":
    try:
        asyncio.run(main(config['sio']))
    except KeyboardInterrupt:
        observer.stop()
        observer.join()