import logging, subprocess

async def network_connections(sio):
    try:
        network_connections = subprocess.check_output("ss -tuln | wc -l", shell=True)
        network_connections = network_connections.strip().decode('utf-8')  # Remove leading/trailing spaces and convert to string
        logging.debug(f"Network Connections: {network_connections}")
        await sio.emit('live_network_connections_check', {'network_connections': network_connections})
    except subprocess.CalledProcessError as e:
        logging.error(f'got error in network_connections: {network_connections}')
        #jerror_message = f"Error: {str(e)}"
        #global_error_message(random_token, error_message)